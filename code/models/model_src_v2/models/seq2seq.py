import random

import torch
from torch import nn
from torch.autograd import Variable

print_shape_flag = False


class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder, output_max_len, vocab_size, device="cuda"):
        super(Seq2Seq, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.output_max_len = output_max_len
        self.vocab_size = vocab_size

        self.device = device

    # src: Variable
    # tar: Variable
    def forward(self, src, tar, src_len, teacher_rate, train=True):
        tar = tar.permute(1, 0)  # time_s, batch
        batch_size = src.size(0)
        # max_len = tar.size(0) # <go> true_value <end>
        outputs = Variable(
            torch.zeros(self.output_max_len - 1, batch_size, self.vocab_size),
            requires_grad=True,
        ).clone()  # (14, 32, 62) not save the first <GO>
        outputs = outputs.to(self.device)
        # src = Variable(src)
        out_enc, hidden_enc = self.encoder(src, src_len)
        # t,b,f    layers, b,f

        output = Variable(self.one_hot(tar[0].data))
        attns = []

        hidden = hidden_enc

        attn_weights = Variable(
            torch.zeros(out_enc.shape[1], out_enc.shape[0]), requires_grad=True
        ).to(
            self.device
        )  # b, t
        for t in range(0, self.output_max_len - 1):  # max_len: groundtruth + <END>
            teacher_force_rate = random.random() < teacher_rate
            output, hidden, attn_weights = self.decoder(
                output, hidden, out_enc, src_len, attn_weights
            )
            outputs[t] = output
            # top1 = output.data.topk(1)[1].squeeze()
            output = Variable(
                self.one_hot(tar[t + 1].data)
                if train and teacher_force_rate
                else output.data
            )
            attns.append(attn_weights.data.cpu())  # [(32, 55), ...]

        return outputs, attns

    def one_hot(self, src):  # src: torch.cuda.LongTensor
        ones = torch.eye(self.vocab_size).to(self.device)
        return ones.index_select(0, src)
