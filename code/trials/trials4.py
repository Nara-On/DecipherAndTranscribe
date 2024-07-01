# -*- coding: utf-8 -*-

import os
import numpy as np
import json

from typing import List, NamedTuple, Optional, Tuple, Union
from numpy.typing import ArrayLike


"""
exp_seq2seq.py 110 <module>
exp = Seq2SeqExperiment()

exp_seq2seq.py 33 __init__
super().__init__()

base_experiment.py 75 __init__
self.initialise_everything()

exp_seq2seq.py 40 initialise_everything
self.train_data = BaseDataset(

base_dataset.py 290 __init__
self._load_data()

base_dataset.py 314 _load_data
transcript = self._vocab.prepare_data(

base_dataset.py 216 prepare_data
data = self.pad(self.encode(data_in), pad_len, special)

base_dataset.py 115 encode
return [self.vocab2index[x] for x in labels]

KeyError:
was
"""

blank = "<BLANK>"
go_tok = "<GO>"
stop_tok = "<STOP>"
pad_tok = "<PAD>"

BLANK_INDEX = 0
GO_INDEX = 1
STOP_INDEX = 2
PAD_INDEX = 3


tokens = [blank, go_tok, stop_tok, pad_tok]

vocab = [" ", "\"", "#", "%", "(", ")", "*", "+", ".", "3", ":", "=", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "N", "P", "R", "S", "T", "U", "V", "X", "Z", "^", "_", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "}", "\u00e4", "\u00f6", "\u00fc"]
vocab = tokens + vocab


vocab2index = {x: ii for ii, x in enumerate(vocab)}
index2vocab = {v: k for k, v in vocab2index.items()}


def encode(labels: List[str]) -> List[int]:
    return [vocab2index[x] for x in labels]
    

def decode(encoded: List[int]) -> List[str]:
    return [index2vocab[x] for x in encoded]

    
def pad(encoded: List[int], pad_len: int, special: bool = False,) -> ArrayLike:
    padded = np.full(pad_len, PAD_INDEX)
    if special:
        assert len(encoded) + 2 <= pad_len
        padded[1 : len(encoded) + 1] = encoded
        padded[0] = GO_INDEX
        padded[len(encoded) + 1] = STOP_INDEX
    else:
        assert len(encoded) <= pad_len
        padded[: len(encoded)] = encoded
    return padded


def unpad(padded: List[int]) -> List[int]:
    output = []
    for x in padded:
        if x == vocab2index[stop_tok]:
            break
        if (
            x == vocab2index[pad_tok]
            or x == vocab2index[go_tok]
        ):
            continue
        output.append(x)
    return output


if __name__ == '__main__':
    
    inputGT_ex1 = "was verloreN geweseN worauf er reiheherum"
    inputGT_ex2 = "neN bruder sich proponireN lasseN der f\u00fcr ihn guaranti"
    
    #inputInd_ex1 = encode(inputGT_ex1)
    #inputInd_ex2 = encode(inputGT_ex2)
    
    #output_ex1 = "".join(decode(inputInd_ex1))
    #output_ex2 = "".join(decode(inputInd_ex2))
    
    
    #dataIn_ex1 = pad(encode(inputGT_ex1), 64, True)
    #dataIn_ex2 = pad(encode(inputGT_ex2), 64, True)
    
    #dataOut_ex1 = "".join(unpad(decode(dataIn_ex1)))
    #dataOut_ex2 = "".join(unpad(decode(dataIn_ex2)))
    
    labels = inputGT_ex1.split(" ")
    line = " ".join(labels)
    
    inputLine = encode(line)
    
    
    
    
    