from torch import nn
from torch.autograd import Variable
import torch
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import numpy as np

from .vgg_tro_channel3 import vgg19_bn

DROP_OUT = False
SUM_UP = True
PRE_TRAIN_VGG = True


class Encoder(nn.Module):
    def __init__(self, hidden_size, layers, height, width, dropout):
        super(Encoder, self).__init__()
        self.hidden_size = hidden_size
        self.n_layers = layers
        self.height = height
        self.width = width
        self.dropout = dropout

        self.layer = vgg19_bn(PRE_TRAIN_VGG)

        if DROP_OUT:
            self.layer_dropout = nn.Dropout2d(p=0.5)

        self.rnn = nn.GRU(
            (self.height // 16) * 512,
            self.hidden_size,
            self.n_layers,
            dropout=self.dropout,
            bidirectional=True,
        )
        if SUM_UP:
            self.enc_out_merge = (
                lambda x: x[:, :, : x.shape[-1] // 2] + x[:, :, x.shape[-1] // 2 :]
            )
            self.enc_hidden_merge = lambda x: (x[0] + x[1]).unsqueeze(0)

    def forward(self, in_data, in_data_len, hidden=None):
        batch_size = in_data.shape[0]
        out = self.layer(in_data)           # (batch, channels, height, width)
        if DROP_OUT and self.training:
            out = self.layer_dropout(out)
        out = out.permute(3, 0, 2, 1)       # (width, batch, height, channels)
        out = out.contiguous()
        out = out.view(
            -1, batch_size, self.height // 16 * 512
        )  # (width, batch, channels * height)

        width = out.shape[0]
        src_len = in_data_len.numpy() * (width / self.width)
        src_len = src_len + 0.999  # in case of 0 length value from float to int
        src_len = src_len.astype("int")
        out = pack_padded_sequence(
            out, src_len.tolist(), batch_first=False, enforce_sorted=False
        )
        output, hidden = self.rnn(out, hidden)

        # output: t, b, f*2  hidden: 2, b, f
        output, output_len = pad_packed_sequence(output, batch_first=False)
        if SUM_UP:
            output = self.enc_out_merge(output)
            # hidden = self.enc_hidden_merge(hidden)
        # # output: t, b, f    hidden:  b, f
        odd_idx = [1, 3, 5, 7, 9, 11]
        hidden_idx = odd_idx[: self.n_layers]
        final_hidden = hidden[hidden_idx]
        return output, final_hidden  # t, b, f*2    b, f*2
