"""Produce alignment using a Sequence to Sequence model with Attention Mechanism."""

from pathlib import Path

import torch
from torch import nn
import torch.utils.data as D
import numpy as np
from tqdm.auto import tqdm

from models.encoder_vgg import Encoder
from models.decoder import Decoder
from models.seq2seq import Seq2Seq
from models.attention import locationAttention as Attention

from datasets.syn_midi import SynMidi
from datasets.comref_dataset import ComrefDataset
from datasets.decrypt_dataset import CopialeDataset, BorgDataset, VaticanDataset

DATASETS = {
    "syn_midi": SynMidi,
    "comref": ComrefDataset,
    "copiale": CopialeDataset,
    "borg": BorgDataset,
    "vatican": VaticanDataset,
}

WEIGHTS_PATH = Path("/home/ptorras/Documents/Decrypt/seq2seq_weights")

EXP_NAME = "decrypt_copiale_large_noaug_pretrain_lowlr"
TARGET_WIDTH = 1200
TARGET_HEIGHT = 64
START_EPOCH = 0
BATCH_SIZE = 1
HIDDEN_SIZE = 512
EMBED_SIZE = 128
LAYERS = 4
LABEL_SMOOTHING = 0.4
DATASET = "copiale"
THREADS = 4
SMALLMODE = False
DEVICE = torch.device("cuda")
DATA_AUGMENTATION = False
MAX_LENGTH = 120

WEIGHTS_FILENAME = "exp_decrypt_copiale_large_noaug_pretrain_lowlr_epoch_16.weights"

encoder = Encoder(HIDDEN_SIZE, LAYERS, TARGET_HEIGHT, TARGET_WIDTH, 0.5)
decoder = Decoder(
    HIDDEN_SIZE, EMBED_SIZE, len(DATASETS[DATASET].CLASSES), Attention, None, LAYERS
)
seq2seq = Seq2Seq(encoder, decoder, MAX_LENGTH, len(DATASETS[DATASET].CLASSES))

seq2seq.load_state_dict(torch.load(WEIGHTS_PATH / WEIGHTS_FILENAME))

# %%

# Load dataset

additional = {"mode": "lines"} if DATASET in ["copiale", "vatican", "borg"] else {}

testdata = DATASETS[DATASET](
    (TARGET_HEIGHT, TARGET_WIDTH), "test", False, SMALLMODE, MAX_LENGTH, **additional
)
testloader = D.DataLoader(
    testdata, BATCH_SIZE, shuffle=False, pin_memory=False, num_workers=THREADS
)

# %%

import cv2

from numpy.typing import ArrayLike
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from scipy.optimize import curve_fit

from typing import List, Optional, Tuple


cdict = {
    "red": ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
    "green": ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
    "blue": ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
    "alpha": ((0.0, 1.0, 1.0), (1.0, 0.0, 0.0)),
}
alpha_colormap = mpl.colors.LinearSegmentedColormap("alpha_cmap", cdict)


def plotimg(img: ArrayLike) -> None:
    """Display an image in a singleton plot.

    :param img: Input image in array-like fashion.
    """
    plt.figure(dpi=150)
    plt.imshow(img)
    plt.axis("off")
    plt.show()
    plt.close()


def plot_attn(img: ArrayLike, attn: ArrayLike) -> None:
    """Plot a single attention mask onto an image.

    Parameters
    ----------
    img : ArrayLike
        Image array. Should have width x height x channels dimensionality.
    attn : ArrayLike
        An attention mask as an array of a single dimension.

    """
    height, width, channels = img.shape
    weights = len(attn)

    width_ratio = width / weights

    plt.figure(dpi=150, figsize=(8, 2))
    plt.tick_params(axis="both", which="major", labelsize=4)
    plt.xticks(np.arange(weights) * width_ratio, np.arange(weights))
    plt.imshow(
        img,
        extent=(-0.5, width + 0.5, -0.5, height + 0.5),
    )
    plt.imshow(
        attn[None, :] + 1e-4,
        extent=(-0.5, width + 0.5, -0.5, height + 0.5),
        cmap=alpha_colormap,
        alpha=0.5,
    )
    plt.tight_layout()
    plt.show()
    plt.close()


def plot_all_attn(img: ArrayLike, attn: ArrayLike) -> None:
    """Plot an entire set of attention weights onto an image.

    Parameters
    ----------
    img : ArrayLike
        Input image as an array.
    attn : ArrayLike
        Set of attention weights. Should be a Sequence Length x Width array.
    """
    height, width, channels = img.shape
    chars, weights = attn.shape

    width_ratio = width / weights
    plt.figure(dpi=150, figsize=(8, 8))

    for ind, attn_mask in enumerate(attn):
        plt.subplot(chars, 1, ind + 1)
        plt.tick_params(axis="both", which="major", labelsize=4)
        plt.xticks(np.arange(weights) * width_ratio, np.arange(weights))
        plt.imshow(
            img,
            extent=(-0.5, width + 0.5, -0.5, height + 0.5),
        )
        plt.imshow(
            attn_mask[None, :] + 1e-4,
            extent=(-0.5, width + 0.5, -0.5, height + 0.5),
            cmap=alpha_colormap,
            alpha=0.5,
        )
    plt.tight_layout()
    plt.show()
    plt.close()


def plot_char_positions(
    img: ArrayLike,
    boxes: ArrayLike,
    characters: List[str],
    stds: Optional[ArrayLike] = None,
) -> None:
    height, width, channels = img.shape
    nchars = len(characters)
    boxes = boxes[:nchars]

    fig = plt.figure(dpi=300, figsize=(8, 2))
    ax = fig.add_subplot()
    ax.imshow(img)

    colors = plt.cm.hsv(np.linspace(0, 1, nchars))

    for index, (bbox, character) in enumerate(zip(boxes, characters)):
        ax.text(
            bbox.mean(),
            (index % 4) * (height // 4),
            character,
            ha="center",
            va="top",
            size=4,
            bbox={
                "boxstyle": "circle",
                "fc": (1.0, 0.8, 0.8, 0.5),
                "ec": (1.0, 0.8, 0.8, 0.5),
            },
        )
        ax.add_patch(
            patches.Rectangle(
                (bbox[0], 0),
                bbox[1] - bbox[0],
                height,
                alpha=0.5,
                linewidth=1,
                color=colors[index],
            )
        )
    plt.tight_layout()
    plt.show()
    plt.close()


def get_bbox_params(
    distributions: ArrayLike, imsize: int
) -> Tuple[ArrayLike, ArrayLike]:
    batch, seqlen, width = distributions.shape

    # indices = np.arange(width) + 0.5
    # values = np.where(distributions > 1e-2, distributions, 0.0) * indices[None, None, :]
    # means = values.sum(axis=-1)
    # means = means * (imsize / width)

    low = distributions.argmax(axis=-1)
    hi = low + 1

    coordinates = np.stack((low, hi), axis=-1)
    coordinates = coordinates * (imsize / width)

    return coordinates


seq2seq = seq2seq.to(DEVICE)

results = {}

for img_name, tokenised, img, imsize, oldsize in tqdm(testloader):
    img_gpu = img.to(DEVICE)
    tokenised_gpu = tokenised.to(DEVICE)
    output, attention = seq2seq(img_gpu, tokenised_gpu, imsize[1], 0.0, False)

    groundtruth = tokenised.detach().cpu().numpy()
    groundtruth = [DATASETS[DATASET].detokenise(x) for x in groundtruth]

    clean_output = output.detach().cpu()  # Length, batch, nclasses
    clean_output = clean_output.permute((1, 0, 2))  # Batch, length, nclasses
    clean_output = clean_output.argmax(dim=-1)  # Batch, length
    clean_output = [DATASETS[DATASET].detokenise(x) for x in clean_output.numpy()]

    attention = torch.stack(attention)  # Length, batch, width
    attention = attention.permute((1, 0, 2))  # Batch, length, width
    attention = attention.cpu()

    if attention.shape[-1] != TARGET_WIDTH // 16:
        new_attention = torch.zeros(*attention.shape[:2], TARGET_WIDTH // 16)
        new_attention[:, :, : attention.shape[-1]] = attention
        attention = new_attention

    img_0 = img[0].permute((1, 2, 0))
    bboxes = get_bbox_params(attention, TARGET_WIDTH)
    plot_char_positions(img_0, bboxes[0], clean_output[0])
    break

#%%
