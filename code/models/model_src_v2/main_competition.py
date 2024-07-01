import argparse
import datetime
import os
import time
from argparse import Namespace
from pathlib import Path
from typing import Any, AnyStr, Dict, List, Tuple

import debug_functions as db
import numpy as np
import torch
import torch.nn.functional as F
import wandb
from datasets.competition_dataset import (CompetitionCollator,
                                          CompetitionDataset, CompetitionVocab)
from models.attention import locationAttention as Attention
from models.decoder import Decoder
from models.encoder_vgg import Encoder
from models.seq2seq import Seq2Seq
from torch import nn, optim
from torch.autograd import Variable
from torch.utils import data as D
from tqdm.auto import tqdm
from utils import visualisation as viz


class Logger:
    def __init__(self, expname: str, log_path: Path) -> None:
        log_path.mkdir(exist_ok=True, parents=True)

        self._log_path = log_path / expname
        self._expname = expname
        self._time = time.time()
        self._lastlog = time.time()

        # FIXME careful to disable this when disabling sweeps
        self._log_path.mkdir(exist_ok=True, parents=False)

        self._loss_files = {
            partition: self._log_path / f"{partition}_loss.log"
            for partition in ["train", "test", "valid"]
        }
        self._ser_files = {
            partition: self._log_path / f"{partition}_ser.log"
            for partition in ["train", "test", "valid"]
        }

        self._best_weight_path = self._log_path / "weights_BEST.pth"
        self._last_weight_path = self._log_path / "weights_LAST_EPOCH.pth"
        self._best_weight_id_path = self._log_path / "best_epoch.log"
        self._best_weight_epoch = -1

        print(
            "Experiment <"
            + self._expname
            + ">: Start @ "
            + str(datetime.datetime.now()).split(".")[0]
            + "\n"
            + ("=" * 60)
        )

    def log(self, msg: str) -> None:
        curr = int(time.time() - self._time)
        hh = curr // 3600
        rest = curr % 3600
        mm = rest // 60
        ss = rest % 60
        print(f"[+ {hh:05}:{mm:02}:{ss:02}] {msg}")

        self._lastlog = time.time()

    def log_loss(self, loss_value: float, partition: str) -> None:
        self.log(f"\t\t{partition} loss: {loss_value}")
        with open(self._loss_files[partition], "a", encoding="utf8") as log_file:
            log_file.write(f"{loss_value}\n")

    def log_ser(self, metric_value: float, partition: str) -> None:
        self.log(f"\t\t{partition} SER: {metric_value:3.4%}")
        with open(self._ser_files[partition], "a", encoding="utf8") as log_file:
            log_file.write(f"{metric_value}\n")

    def write_output(self, output: List[str], filename: str, epoch: int, mode: str):
        with open(
            self._log_path / f"{self._expname}_{mode}_{epoch}_output.log", "a"
        ) as log_file:
            log_file.write(filename + "|" + "".join(output) + "\n") ###

    def write_best_weights(self, weights: Dict, epoch: int) -> None:
        torch.save(weights, self._best_weight_path)
        with open(self._best_weight_id_path, "a") as f_out:
            f_out.write(f"{epoch}\n")
        self._best_weight_epoch = epoch

    def write_current_weights(self, weights: Dict) -> None:
        torch.save(weights, self._last_weight_path)

    def export_parameters(self, args: Namespace):
        with open(self._log_path / f"params_{self._expname}.conf", "w+") as param_file:
            params = vars(args)
            for k in params.keys():
                param_file.write('{}="{}"\n'.format(k.upper(), params[k]))


def setup() -> Namespace:
    # fmt: off
    parser = argparse.ArgumentParser(description="Sequence to Sequence net", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("exp_name", type=str, help="experiment name")
    parser.add_argument("root_data_path", type=Path, help="root path for the experiment data")
    parser.add_argument("dataset", type=str, help="dataset to use")

    parser.add_argument("--test", type=Path, help="Path to test weights", default=None)
    parser.add_argument("--wandb_project", type=str, help="WandB project name", default="RRC")
    parser.add_argument("--wandb_mode", type=str, help="WandB operation mode", default="online", choices=["online", "disabled"])
    parser.add_argument("--log_path", type=Path, help="Root path for logging data", default="./logs")

    # Dataset
    parser.add_argument("--tokenised", action="store_true", help="Use tokenised versions of the data (with plaintext label) if available")
    parser.add_argument("--reduced_vocab", action="store_true", help="Use reduced vocabulary versions of the data if available")
    parser.add_argument("--toy_model", action="store_true", help="Reduce dataset size to 100 for a toy-model run")
    parser.add_argument("--augmented", action="store_true", help="Use data augmentation or not")
    parser.add_argument("--max_length", type=int, help="Max sequence length", default=120)
    parser.add_argument("--threads", type=int, help="Dataloader threads", default=8)
    parser.add_argument("--target_width", type=int, help="Image input width", default=800)
    parser.add_argument("--target_height", type=int, help="Image input height", default=64)

    # Training
    parser.add_argument("--device", type=str, help="Device to train on", default="cuda")
    parser.add_argument("--start_epoch", type=int, help="previous checkpoint", default=0)
    parser.add_argument("--max_epochs", type=int, help="max number of epochs (0 if unlimited)", default=0)
    parser.add_argument("--early_stopping", type=int, help="epochs for early stopping in case of no improvement", default=20)
    parser.add_argument("--learning_rate", type=float, help="learning rate", default=3e-4)
    parser.add_argument("--learning_sigma", type=float, help="factor by which to change learning rate learning_epochs epochs", default=0.1)
    parser.add_argument("--learning_epochs", type=int, help="learning rate variation epochs", default=20)
    parser.add_argument("--batch_size", type=int, help="batch size", default=4)

    # Model
    parser.add_argument("--hidden_size", type=int, help="RNN Hidden size", default=512)
    parser.add_argument("--embed_size", type=int, help="char embedding size for decoder", default=128)
    parser.add_argument("--layers", type=int, help="RNN layers in the encoder and the decoder", default=4)
    parser.add_argument("--label_smoothing", type=float, help="Apply label smoothing", default=0.0)
    parser.add_argument("--weight_decay", type=float, help="Amount of weight decay to apply", default=1e-2)
    parser.add_argument("--dropout", type=float, help="Amount of dropout to apply", default=0.5)
    parser.add_argument("--teacher_rate", type=float, help="Amount of dropout to apply", default=0.0)
    # fmt: on

    args = parser.parse_args()

    return args


def create_loss_function(args: Namespace, vocab: CompetitionVocab) -> nn.Module:
    loss_function = nn.CrossEntropyLoss(
        label_smoothing=args.label_smoothing,
        ignore_index=vocab.token2index[vocab.PAD_TAG],
    )

    return loss_function


def levenshtein(source, target):
    matrix = []
    if len(target) == 0:
        return len(source)

    # We call tuple() to force strings to be used as sequences
    # ('c', 'a', 't', 's') - numpy uses them as values by default.
    source = np.array(tuple(source))
    target = np.array(tuple(target))

    previous_row = np.arange(target.size + 1)

    matrix.append(previous_row)
    for s in source:
        current_row = previous_row + 1

        current_row[1:] = np.minimum(
            current_row[1:], np.add(previous_row[:-1], target != s)
        )
        current_row[1:] = np.minimum(current_row[1:], current_row[0:-1] + 1)

        previous_row = current_row
        matrix.append(previous_row)

    return [previous_row[-1] / float(len(target)), matrix]


def infer(
    args: Namespace,
    model: nn.Module,
    data: D.DataLoader,
    loss_function: nn.Module,
    epoch: int,
    mode: str,
    logger: Logger,
    vocab: CompetitionVocab,
    opt: optim.Optimizer = None,
):
    """Perform inference step over dataset.

    Perform inference step over dataset. If training is enabled on the model
    then it will also update weights accordingly.

    Parameters
    ----------
    model: nn.Module
        Model on which inference should be performed.

    data: D.DataLoader
        Inference dataset wrapped in a torch.utils.data.Dataloader.

    loss: nn.Module
        Loss function layer from torch.nn

    epoch: int
        Epoch number for logging reasons

    mode: str
        Training, testing or validation mode for logging reasons

    opt: optim.Optimizer
        Optimizer module to update weights of the model.

    Returns
    -------
    mean_loss: float
        Mean loss from the inference step

    """
    total_loss = 0
    total_ser = 0

    for batch_index, batch in enumerate(tqdm(data)):
        img = batch["img"].to(args.device)
        tokenised = batch["tokenised"].to(args.device)

        output, _ = model(
            img,
            tokenised,
            batch["imsize"][:, 1],
            args.teacher_rate,
            mode == "train",
        )
        train_label = tokenised.permute(1, 0)[1:].contiguous().view(-1)  # remove<GO>
        output_l = output.view(-1, len(vocab))  # remove last <EOS>

        loss = loss_function(output_l, train_label)

        if model.training and opt is not None:
            opt.zero_grad()
            loss.backward()
            opt.step()

        total_loss += loss.item()

        output = output.to("cpu").detach()

        output_classes = output.permute(1, 0, 2).topk(1)[1].squeeze(2).numpy()
        ground_truth = batch["transcript"]

        for b, gt_seq in enumerate(ground_truth):
            output_detokenised = vocab.unprepare(output_classes[b])

            if len(output_detokenised) > 0:
                perf, _ = levenshtein(output_detokenised, gt_seq)
                total_ser += perf
            elif len(output_detokenised) == 0:
                total_ser += 1

            logger.write_output(
                output_detokenised, str(batch["img_path"][b]), epoch, mode
            )

            if batch_index == len(data) - 1 and not model.training: ###
                logger.log(
                    f"Image: {str(batch['img_path'][b])}\n"
                    f"Ground Truth: {''.join(gt_seq)}\n"
                    f"Output: {''.join(output_detokenised)}\nSER: {perf:.3%}\n\n"
                )

        if mode == "train":
            wandb.log({"batch_loss": loss})

    return total_loss / len(data), total_ser / len(data.dataset)


def load_datasets(args: Namespace):
    # Hack to simplify edits
    base_data_path = args.root_data_path / args.dataset

    vocab_path = (
        base_data_path / "vocab_small.json"
        if (base_data_path / "vocab_small.json").exists() and args.reduced_vocab
        else base_data_path / "vocab.json"
    )
    image_path = base_data_path / "img"

    vocab = CompetitionVocab(vocab_path)
    collator = CompetitionCollator(vocab, args.max_length)

    dataloaders = []
    for split in ["train", "valid", "test"]:
        dataset = CompetitionDataset(
            image_path,
            base_data_path / f"{args.dataset}_{split}_tokenised.json"
            if (base_data_path / f"{args.dataset}_{split}_tokenised.json").exists()
            and args.tokenised
            else base_data_path / f"{args.dataset}_{split}.json",
            (args.target_height, args.target_width),
            split == "train",
            args.augmented,
            args.toy_model,
        )
        dataloaders.append(
            D.DataLoader(
                dataset,
                batch_size=args.batch_size,
                shuffle=split == "train",
                num_workers=args.threads,
                pin_memory=True,
                collate_fn=collator.collate_train
                if split == "train"
                else collator.collate_eval,
            )
        )

    return dataloaders[0], dataloaders[1], dataloaders[2], vocab


def create_model(args: Namespace, vocab: CompetitionVocab) -> nn.Module:
    encoder = Encoder(
        args.hidden_size,
        args.layers,
        args.target_height,
        args.target_width,
        args.dropout,
    )
    decoder = Decoder(
        args.hidden_size,
        args.embed_size,
        len(vocab),
        Attention,
        None,
        args.layers,
        args.device,
    )
    seq2seq = Seq2Seq(
        encoder,
        decoder,
        args.max_length,
        len(vocab),
        args.device,
    )

    return seq2seq


def main(args: Namespace) -> None:
    logger = Logger(args.exp_name, args.log_path)

    # Load Datasets
    logger.log("Loading Datasets...")
    trainloader, validloader, testloader, vocab = load_datasets(args)
    logger.log("Datasets loaded successfully!")

    # Create Model
    logger.log("Creating model...")
    seq2seq = create_model(args, vocab)
    loss_function = create_loss_function(args, vocab)
    logger.log("Model created successfully!")

    if args.test is not None:
        seq2seq.load_state_dict(torch.load(args.test))
        seq2seq = seq2seq.to(args.device)
        test_loss, test_ser = infer(
            args, seq2seq, testloader, loss_function, 0, "test", logger, vocab
        )
        logger.log_loss(test_loss, "test")
        logger.log_ser(test_ser, "test")
        exit(0)

    # Set up optimizer settings
    optimizer = optim.AdamW(
        seq2seq.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay
    )
    scheduler = optim.lr_scheduler.MultiStepLR(
        optimizer,
        milestones=[x * args.learning_epochs for x in range(1, 5)],
        gamma=args.learning_sigma,
    )

    # Update scheduler
    if args.start_epoch > 0:
        for _ in range(args.start_epoch + 1):
            scheduler.step()

    valid_metric = 999999999
    last_improvement = 0

    # Send model to device
    seq2seq.to(args.device)
    loss_function = loss_function.to(args.device)

    wandb.init(
        project=args.wandb_project,
        dir=args.log_path,
        config=vars(args),
        mode=args.wandb_mode,
        name=args.exp_name,
        save_code=True,
    )

    # Perform training
    for epoch in range(
        args.start_epoch + 1 if args.start_epoch > 0 else 0,
        args.max_epochs if args.max_epochs > 0 else 99999999,
    ):
        logger.log(f"Epoch {epoch}: Learning rate: {scheduler.get_last_lr()}")

        seq2seq.train()
        train_loss, train_ser = infer(
            args,
            seq2seq,
            trainloader,
            loss_function,
            epoch,
            "train",
            logger,
            vocab,
            optimizer,
        )
        logger.log_loss(train_loss, "train")
        logger.log_ser(train_ser, "train")

        wandb.log(
            {"final_train_loss": train_loss, "train_SER": train_ser, "epoch": epoch}
        )
        logger.write_current_weights(seq2seq.state_dict())

        with torch.no_grad():
            seq2seq.eval()
            valid_loss, valid_ser = infer(
                args,
                seq2seq,
                validloader,
                loss_function,
                epoch,
                "valid",
                logger,
                vocab,
            )
            logger.log_loss(valid_loss, "valid")
            logger.log_ser(valid_ser, "valid")

            wandb.log(
                {"valid_loss": valid_loss, "valid_SER": valid_ser, "epoch": epoch}
            )

            epoch_validation = valid_ser

            seq2seq.eval()
            test_loss, test_ser = infer(
                args,
                seq2seq,
                testloader,
                loss_function,
                epoch,
                "test",
                logger,
                vocab,
            )
            logger.log_loss(test_loss, "test")
            logger.log_ser(test_ser, "test")

            wandb.log({"test_loss": test_loss, "test_SER": test_ser, "epoch": epoch})

        scheduler.step()

        if epoch_validation < valid_metric:
            last_improvement = epoch
            valid_metric = epoch_validation

            logger.write_best_weights(seq2seq.state_dict(), epoch)

        elif 0 < args.early_stopping < epoch - last_improvement:
            break

    logger.log("Training complete at epoch {}".format(epoch))


if __name__ == "__main__":
    main(setup())
