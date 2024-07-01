from torch.utils.data import Dataset
from pathlib import Path
from .augmentation import augmidi

import numpy as np
import cv2
import os
import json

from typing import Tuple, AnyStr, List, Dict

# class SynMidiSample(TypedDict):
#     midi_name: AnyStr
#     img_name: AnyStr
#     threshold: int
#     groundtruth: List
#     tokenised: np.ndarray
#     img: np.ndarray
#     imsize: Tuple[int, int]
#     oldsize: Tuple[int, int]
#
# SynMidiJSON = List[SynMidiSample]

SynMidiSample = Dict
SynMidiJSON = List[SynMidiSample]


class SynMidi(Dataset):
    PERSONAL_PATH = Path("/home/pau/Documents/midi_score/datasets/syn_midi")
    CLUSTER_PATH = Path("/data2fast/users/ptorras/midi/syn_midi")

    ROOT_PATH = PERSONAL_PATH if os.path.exists(PERSONAL_PATH) else CLUSTER_PATH

    # Following midi configuration is assumed:
    #   HEADER: <Type:      Htrk (header)>
    #           <Length:    xx   (unknown yet)>
    #           <Format:    00   (single track)>
    #           <ntracks:   1    (single track)>
    #           <division:  0384 (metric - 384 ticks per quarter note)>
    #   C or a tonalities - No alterations
    #   4/4 beat

    CLASSES = [
        "GO",
        "END",
        "PAD",
        "MIDI_NOTEON",
        "MIDI_NOTEOFF",
        "MIDI_VELOCITY",
        "MIDI_PITCH",
        "MIDI_DELTA",
        "SCALAR_0",
        "SCALAR_1",
        "SCALAR_2",
        "SCALAR_3",
        "SCALAR_4",
        "SCALAR_5",
        "SCALAR_6",
        "SCALAR_7",
        "SCALAR_8",
        "SCALAR_9",
    ]
    NCLASSES = len(CLASSES)

    INDEX2CLASS = {i: cl for i, cl in enumerate(CLASSES)}
    CLASS2INDEX = {cl: i for i, cl in INDEX2CLASS.items()}

    MAX_LEN = 120  # max is actually 187, 112 without midi channel/velocity parameters

    def __init__(
        self,
        target_resolution: Tuple[int, int],
        partition: AnyStr,
        augmentation: bool = False,
        smallmode: bool = False,
    ) -> None:
        self.target_resolution = target_resolution
        self.partition = partition
        self.augmentation = augmentation
        self.smallmode = smallmode

        self.data = self.__load_json(self.partition)
        if self.smallmode:
            self.data = self.data[:100]
        self.__tokenise()

    def __getitem__(
        self, item: int
    ) -> (AnyStr, np.ndarray, np.ndarray, Tuple[int, int], Tuple[int, int]):
        sample = self.data[item]
        img, imsize, oldsize = self.__load_image(sample)

        return sample["img_name"], sample["tokenised"], img, imsize, oldsize

    def __len__(self) -> int:
        return len(self.data)

    def __load_json(self, partition: AnyStr) -> SynMidiJSON:
        with open(self.ROOT_PATH / "syn_midi.json", "r") as f_js:
            jstring = f_js.read()
        temp = json.loads(jstring)
        return temp[partition]

    def __tokenise(self):
        for x in self.data:
            aux = (
                [self.CLASS2INDEX["GO"]]
                + [self.CLASS2INDEX[element] for element in x["groundtruth"]]
                + [self.CLASS2INDEX["END"]]
            )
            aux = aux + ([self.CLASS2INDEX["PAD"]] * (self.MAX_LEN - len(aux)))
            x["tokenised"] = np.array(aux)

            assert len(x["tokenised"]) == self.MAX_LEN

    @staticmethod
    def detokenise(vect: np.ndarray) -> List[AnyStr]:
        sequence = []
        for i in range(len(vect)):
            token = SynMidi.INDEX2CLASS[vect[i]]
            if token == "GO":
                continue
            if token == "END":
                break
            sequence.append(token)
        return sequence

    def parse(self):
        pass

    def __load_image(
        self, x: SynMidiSample
    ) -> (np.ndarray, Tuple[int, int], Tuple[int, int]):
        img = cv2.imread(
            str(self.ROOT_PATH / "img" / x["img_name"]), cv2.IMREAD_GRAYSCALE
        )

        # Normalise Image
        img = (img - img[:].min()) / (img.max() - img.min())
        img = 1.0 - img

        # Resize image and adapt to canvas
        tar_height, tar_width = self.target_resolution
        img_height, img_width = img.shape

        rs_rate = min(tar_height / img_height, tar_width / img_width)

        nw_width = int(img_width * rs_rate)
        nw_height = int(img_height * rs_rate)

        resimg = cv2.resize(img, (nw_width, nw_height), interpolation=cv2.INTER_CUBIC)
        img = np.zeros(self.target_resolution)
        img[:nw_height, :nw_width] = resimg

        # Image Augmentation
        if self.augmentation:
            img = augmidi.augmentor(img)

        # Expand into 3 channels + VGG normalisation
        img = np.vstack([np.expand_dims(img, axis=0)] * 3)

        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        img = (img - mean[:, np.newaxis, np.newaxis]) / std[:, np.newaxis, np.newaxis]

        return img, (nw_height, nw_width), (img_height, img_width)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    test = SynMidi((256, 800), "train", False)

    for x in test:
        plt.figure()
        plt.imshow(np.transpose(x[2], (1, 2, 0)))
        plt.show()
        plt.close()
