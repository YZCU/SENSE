from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import torch.nn as nn
import torch


def sc(fc, od):
    fi = []
    b = fc.size()[0]
    wi = [[None for j in range(b)] for i in range(5)]
    obi, odbd = od[0], od[1]
    for i in range(5):
        gg = fc[None, 0, odbd[0, i * 3:i * 3 + 3], :, :]
        wi[i][0] = obi[0, i * 3:i * 3 + 3].detach().mean().item()
        for k in range(1, b):
            gg = torch.cat((gg, fc[None, k, odbd[k, i * 3:i * 3 + 3], :, :]), dim=0)
            wi[i][k] = obi[k, i * 3:i * 3 + 3].detach().mean().item()
        fi.append(gg)

    return fi, wi


class ssse(nn.Module):
    def __init__(self):
        super(ssse, self).__init__()
        channel = 16

        self.spectral = nn.Sequential(nn.Conv2d(channel, channel * 2,1, 1, bias=False),
                                      nn.BatchNorm2d(channel * 2),
                                      nn.ReLU(),
                                      nn.Conv2d(channel * 2, channel * 4,1, 1,bias=False),
                                      nn.BatchNorm2d(channel * 4),
                                      nn.ReLU(),
                                      )

        self.spatial = nn.Sequential(
            nn.Conv2d(channel * 4, channel * 2,3, 1, 1, bias=False),
            nn.BatchNorm2d(channel * 2),
            nn.ReLU(),
            nn.Conv2d(channel * 2, channel * 2,3, 1, 1, bias=False),
            nn.BatchNorm2d(channel * 2),
            nn.ReLU(),
        )

        self.mlpd = nn.Sequential(nn.Linear(channel * 2, channel * 2, bias=True),nn.Tanh(),
                                         nn.Linear(channel * 2, channel, bias=True),
                                         nn.Tanh(), )

    def forward(self, x):
        # select

        # x = x.mul(1 / 255.0).clamp(0.0, 1.0)
        it = x
        b1, c1, w1, h1 = x.size()
        x2 = self.spatial(self.spectral(x))
        b, c, w, h = x2.size()
        x3 = x2.view(b, c, -1)
        w0 = self.mlpd(x3.permute(0, 2, 1))

        res = w0.permute(0, 2, 1)
        y0 = res.mean(dim=2)
        y1 = y0.view(b, 16, 1)
        ty = y1.permute(0, 2, 1)

        C = torch.bmm(y1, ty)
        for i in range(16):
            w0[:, i, i] = 0.0

        w = torch.norm(C, p=2, dim=2)

        oy = torch.sort(w, dim=-1, descending=True, out=None)

        fi, wi = sc(x, oy)

        a = it.view(b1, c1, -1)
        cgh = torch.bmm(C, a)

        return fi, wi, oy, cgh
