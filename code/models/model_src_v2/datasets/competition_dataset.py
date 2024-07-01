"""Loads COMREF samples into a Seq2Seq model."""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import torch
import torchvision.transforms as T
from numpy.typing import ArrayLike
from PIL import Image
from torch.utils.data import Dataset


class CompetitionVocab:
    START_TAG = "<START>"
    STOP_TAG = "<STOP>"
    PAD_TAG = "<PAD>"
    UNKNOWN_TAG = "<UNK>"

    AUX_TAGS = [START_TAG, STOP_TAG, PAD_TAG, UNKNOWN_TAG]

    def __init__(self, vocab_file: Path) -> None:
        with open(vocab_file, "r") as f_in:
            data = json.load(f_in)

        self.tokens = self.AUX_TAGS + data["labels"]

        self.token2index = {tok: ii for ii, tok in enumerate(self.tokens)}
        self.index2token = {ii: tok for tok, ii in self.token2index.items()}

    def __len__(self) -> int:
        return len(self.token2index)

    def tokenise(self, line: List[str]) -> List[int]:
        # Decryption
        line = " ".join(line)
        return [
            self.token2index[tok]
            if tok in self.token2index
            else self.token2index[self.UNKNOWN_TAG]
            for tok in line
        ]

    def pad(self, tokenised: List[int], size: int) -> ArrayLike:
        padded = np.full((size,), self.token2index[self.PAD_TAG])
        max_index = min(len(tokenised), size - 2)
        padded[1 : max_index + 1] = tokenised[:max_index]
        padded[0] = self.token2index[self.START_TAG]
        padded[max_index + 1] = self.token2index[self.STOP_TAG]
        return padded

    def prepare(self, line: List[str], size: int) -> ArrayLike:
        return self.pad(self.tokenise(line), size)

    def unpad(self, padded: ArrayLike) -> List[int]:
        output: List[int] = []
        for tok in padded:
            if tok not in {
                self.token2index[self.START_TAG],
                self.token2index[self.PAD_TAG],
            }:
                if tok == self.token2index[self.STOP_TAG]:
                    return output
                output.append(tok)

        return output

    def detokenise(self, tokenised: List[int]) -> List[str]:
        return [self.index2token.get(ind, self.UNKNOWN_TAG) for ind in tokenised]

    def unprepare(self, padded: ArrayLike) -> List[str]:
        return self.detokenise(self.unpad(padded))


class CompetitionCollator:
    def __init__(self, vocab: CompetitionVocab, max_len: int) -> None:
        self.vocab = vocab
        self.max_len = max_len

    def collate_train(self, batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        output_batch = {}

        output_batch["img_path"] = [sample["img_path"] for sample in batch]
        output_batch["transcript"] = [sample["transcript"] for sample in batch]
        output_batch["tokenised"] = torch.LongTensor(
            np.stack(
                [
                    self.vocab.prepare(sample["transcript"], self.max_len)
                    for sample in batch
                ]
            )
        )

        output_batch["img"] = torch.stack([sample["img"] for sample in batch])
        output_batch["imsize"] = torch.LongTensor(
            np.stack([sample["imsize"] for sample in batch])
        )
        output_batch["oldsize"] = torch.LongTensor(
            np.stack([sample["oldsize"] for sample in batch])
        )

        return output_batch

    def collate_eval(self, batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self.collate_train(batch)


class CompetitionDataset(Dataset):
    """Loads and processes COMREF input images into a seq2seq model."""

    DEFAULT_AUGMENTATIONS = [
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]

    def __init__(
        self,
        img_path: Path,
        gt_path: Path,
        target_resolution: Tuple[int, int],
        training: bool,
        augmentation: bool = False,
        smallmode: bool = False,
    ) -> None:
        self.img_path = img_path
        self.gt_path = gt_path
        self.target_resolution = target_resolution
        self.augmentations = T.Compose(
            (
                [
                    T.ToTensor(),
                    T.RandomPerspective(fill=255),
                    T.ColorJitter(0.05, 0.0, 0.0, 0.2),
                    # T.GaussianBlur(3),
                ]
                if augmentation and training
                else [T.ToTensor()]
            )
            + self.DEFAULT_AUGMENTATIONS
        )
        self.smallmode = smallmode

        self.data = self._load_json(self.gt_path)

        if self.smallmode:
            self.data = self.data[:100]

    def __getitem__(self, item: int) -> Dict[str, Any]:
        """Load a single sample for inference."""
        sample = self.data[item]
        img, imsize, oldsize = self._load_image(str(sample["img_path"]))

        return {
            **sample,
            "img": img,
            "imsize": imsize,
            "oldsize": oldsize,
        }

    def __len__(self) -> int:
        """Get the number of samples of the dataset.

        Returns
        -------
        int
            Number of samples currently present in the dataset object.
        """
        return len(self.data)

    def _load_json(self, gt_path: Path) -> List[Dict[str, Any]]:
        with open(gt_path, "r", encoding="utf8") as f_js:
            data = json.load(f_js)

        samples = []
        for fname, info in data.items():
            sample = {}
            sample["img_path"] = self.img_path / fname
            
            # Transcription
            #sample["transcript"] = info["ts"].split(" ")
            
            # Decryption
            sample["transcript"] = list(info["ts"])
            
            samples.append(sample)

        return samples

    def _load_image(
        self, path: str
    ) -> Tuple[ArrayLike, Tuple[int, int], Tuple[int, int]]:
        img = Image.open(path).convert("RGB")

        img_width, img_height = img.size
        tgt_height, tgt_width = self.target_resolution

        factor = min(tgt_width / img_width, tgt_height / img_height)
        nw_width, nw_height = (int(img_width * factor), int(img_height * factor))

        img = img.resize((nw_width, nw_height))

        padded_img = Image.new(img.mode, (tgt_width, tgt_height), (255, 255, 255))
        padded_img.paste(img, (0, 0))

        augmented_img = self.augmentations(padded_img)

        return augmented_img, (nw_height, nw_width), (img_height, img_width)


if __name__ == "__main__":
    import debug_functions as db
