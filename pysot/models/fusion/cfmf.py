from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import math
import torch.nn.functional as F
import torch
from torch import nn
from collections import OrderedDict


class cfmf(nn.Module):
    def __init__(self):
        super(cfmf, self).__init__()

        self.mlp_specif_fea = nn.Sequential(OrderedDict([('spec_avp', nn.AdaptiveAvgPool2d(1)),
            ('spec_fc1', nn.Sequential(nn.Conv2d(256, 64 * 5, 1, 1, bias=False), nn.ReLU(inplace=True))),
            ('spec_fc2', nn.Sequential(nn.Conv2d(64 * 5, 256 * 5, 1, 1, bias=False), nn.ReLU()))]))

        self.mlp_common_fea = nn.Sequential(OrderedDict([ ('comm_avp', nn.AdaptiveAvgPool2d(1)),
            ('comm_fc1', nn.Sequential(nn.Conv2d(256, 64 * 5, 1, 1, bias=False), nn.ReLU(inplace=True))),
            ('comm_fc2', nn.Sequential(nn.Conv2d(64 * 5, 256 * 5, 1, 1, bias=False), nn.ReLU()))]))

        self.decoder_pre = nn.Sequential(OrderedDict([('conv3', nn.Sequential(nn.Conv2d(256, 256, 3, 1, padding=1), nn.ReLU()))]))

        self.decoder_trans1 = nn.Sequential(OrderedDict([ ('WK1', nn.Sequential(nn.Linear(128, 128))),
            ('WV1', nn.Sequential(nn.Linear(128, 128))),
            ('fc_reduce1', nn.Sequential(nn.Conv2d(256, 128, 1, 1, bias=False))),
            ('fc_rise1', nn.Sequential(nn.Conv2d(128, 256, 1))),
        ]))

        self.decoder_trans2 = nn.Sequential(OrderedDict([('WK2', nn.Sequential(nn.Linear(128, 128))),
            ('WV2', nn.Sequential(nn.Linear(128, 128))),
            ('fc_reduce2', nn.Sequential(nn.Conv2d(256, 128, 1, 1, bias=False))),
            ('fc_rise2', nn.Sequential(nn.Conv2d(128, 256, 1))),
        ]))

    def Transformer_decoder1(self, x):
        x1 = self.decoder_trans1[2](x)
        bh, dim, w, h = x1.shape
        x1 = x1.permute(0, 2, 3, 1)
        xk = x_v = xq = x1.reshape(bh, w * h, dim)
        wk = (F.normalize(self.decoder_trans1[0](xk), p=2, dim=-1)).permute(0, 1, 2)
        wq = (F.normalize(self.decoder_trans1[0](xq), p=2, dim=-1)).permute(0, 2, 1)
        wvaf = (F.normalize(self.decoder_trans1[1](x_v), p=2, dim=-1)).permute(0, 2, 1)
        ot = torch.bmm(F.softmax(torch.bmm(wq, wk) * 30, dim=-1), wvaf)
        ot = self.decoder_trans1[3](ot.reshape(bh, dim, w, h))
        return ot

    def Transformer_decoder2(self, x):
        x1 = self.decoder_trans2[2](x)
        bh, dim, w, h = x1.shape
        x1 = x1.permute(0, 2, 3, 1)
        xk = x_v = xq = x1.reshape(bh, w * h, dim)
        wk = (F.normalize(self.decoder_trans2[0](xk), p=2, dim=-1)).permute(0, 1, 2)
        wq = (F.normalize(self.decoder_trans2[0](xq), p=2, dim=-1)).permute(0, 2, 1)
        wvaf = (F.normalize(self.decoder_trans2[1](x_v), p=2, dim=-1)).permute(0, 2, 1)
        ot = torch.bmm( F.softmax(torch.bmm(wq, wk) * 30, dim=-1), wvaf)
        ot = self.decoder_trans2[3](ot.reshape(bh, dim, w, h))
        return ot

    def forward(self, down_x):
        bh_size = down_x[0].shape[0]
        abd = self.mlp_specif_fea(reduce(lambda x, y: abs(x - y), down_x))
        abd = nn.Softmax(dim=1)(abd.reshape(bh_size, 5, 256, -1))
        w_d = list(map(lambda x: x.reshape(bh_size, 256, 1, 1), list(abd.chunk(5, dim=1))))
        V_d = list(map(lambda x, y: x * y, down_x, w_d))
        asb = self.mlp_common_fea(reduce(lambda x, y: x + y, down_x)).reshape(bh_size, 5, 256, -1)
        ws = list(nn.Softmax(dim=1)(asb).chunk(5, dim=1))
        vs = list(map(lambda x, y: x * y, down_x, list(map(lambda x: x.reshape(bh_size, 256, 1, 1), ws))))
        v2 = list(map(lambda x, y: x + y, list(map(lambda x, y: x + y, V_d, vs)), down_x))
        v3 = reduce(lambda x, y: x + y, v2)
        f1 = self.Transformer_decoder1(self.decoder_pre(v3))
        f3 = self.Transformer_decoder2(f1 + v3)
        x = f1 + f3 + v3

        return x
