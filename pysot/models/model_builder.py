from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import torch
import torch.nn as nn
import torch.nn.functional as F
from pysot.core.config import cfg
from pysot.models.loss_car import make_siamcar_loss_evaluator
from ..utils.location_grid import compute_locations
from pysot.utils.xcorr import xcorr_depthwise
from pysot.models.channelsplit import get_BS
from pysot.models.backbone import get_backbone
from pysot.models.neck import get_neck
from pysot.models.fusion import get_FS
from pysot.models.head.car_head import CARHead


class ModelBuilder(nn.Module):
    def __init__(self):
        super(ModelBuilder, self).__init__()
        self.zf = None

        self.channelsplit = get_BS(cfg.BS.TYPE)

        self.backbone = get_backbone(cfg.BACKBONE.TYPE,
                                     **cfg.BACKBONE.KWARGS)

        if cfg.ADJUST.ADJUST:
            self.neck = get_neck(cfg.ADJUST.TYPE,
                                 **cfg.ADJUST.KWARGS)
        self.fs = get_FS(cfg.FS.TYPE)
        self.car_head = CARHead(cfg, 256)
        self.xcorr_depthwise = xcorr_depthwise
        self.loss_evaluator = make_siamcar_loss_evaluator(cfg)
        self.down = nn.ConvTranspose2d(256 * 3, 256, 1, 1)

    def template(self, z):
        bs_z = self.channelsplit(z)
        for i in range(len(bs_z[0])):
            z = bs_z[0][i]
            zf = self.backbone(z)
            if cfg.ADJUST.ADJUST:
                zf = self.neck(zf)
            if i == 0:
                zff = [zf]
            else:
                zff.append(zf)
        self.zf = zff

    def track(self, x):
        bs_x = self.channelsplit(x)
        i5 = [x[0] for x in bs_x[1]]
        wnm = [v / sum(i5) for v in i5]
        for i in range(len(bs_x[0])):
            x = bs_x[0][i]
            xf = self.backbone(x)
            if cfg.ADJUST.ADJUST:
                xf = self.neck(xf)
            f = self.xcorr_depthwise(xf[0], self.zf[i][0])
            for j in range(len(xf) - 1):
                fn = self.xcorr_depthwise(xf[j + 1], self.zf[i][j + 1])
                f = torch.cat([f, fn], 1)
            fdn = self.down(f)
            if i == 0:
                fsit = [fdn]
            else:
                fsit.append(fdn)
        fsw = [fsit[g] * wnm[g] for g in range(len(i5))]
        f = self.fs(fsw)
        cls, loc, cen = self.car_head(f)
        return {
            'cls': cls,
            'loc': loc,
            'cen': cen
        }

    def log_softmax(self, cls):
        b, a2, h, w = cls.size()
        cls = cls.view(b, 2, a2 // 2, h, w)
        cls = cls.permute(0, 2, 3, 4, 1).contiguous()
        cls = F.log_softmax(cls, dim=4)
        return cls

    def forward(self, data):
        """ only used in training
        """
        template = data['template'].cuda()
        search = data['search'].cuda()
        label_cls = data['label_cls'].cuda()
        label_loc = data['bbox'].cuda()

        tpes = self.channelsplit(template)
        ses = self.channelsplit(search)
        imp = ses[1]

        for j in range(len(imp[0])):
            li = [x[j] for x in imp]

            nm = [v / sum(li) for v in li]
            if j == 0:
                nist1 = [nm]
            else:
                nist1.append(nm)

        for k in range(len(nist1[0])):
            li = [x[k] for x in nist1]
            agv = sum(li) / len(li)
            if k == 0:
                i5 = [agv]
            else:
                i5.append(agv)
        for i in range(len(tpes[0])):
            t3 = tpes[0][i]
            s3 = ses[0][i]
            zf = self.backbone(t3)
            xf = self.backbone(s3)
            if cfg.ADJUST.ADJUST:
                zf = self.neck(zf)
                xf = self.neck(xf)
            f = self.xcorr_depthwise(xf[0], zf[0])
            for k in range(len(xf) - 1):
                fn = self.xcorr_depthwise(xf[k + 1], zf[k + 1])
                f = torch.cat([f, fn], 1)
            f = self.down(f)
            w = sum(ses[1][i]) / len(ses[1][i])

            # if i == 0:
            #     wist1 = [w]
            #     f_w = [f]
            # else:
            #     wist1.append(w)
            #     f_w.append(f)
        # fsw = [f_w[g] * i5[g] for g in range(len(i5))]

        fsw = [w[g] * i5[g] for g in range(len(i5))]
        f_f = self.fs(fsw)
        cls, loc, cen = self.car_head(f_f)
        locations = compute_locations(cls, cfg.TRACK.STRIDE)
        cls = self.log_softmax(cls)
        spcls = ((F.mse_loss(template.view(template.shape[0], template.shape[1], -1), tpes[3]) + 0.001 * sum(
            torch.nm(param, p=2) for param in self.channelsplit.parameters())) / (
                               template.shape[2] * template.shape[3]).data + (
                               F.mse_loss(search.view(search.shape[0], search.shape[1], -1), ses[3]) + 0.001 * sum(
                           torch.nm(param, p=2) for param in self.channelsplit.parameters())) / (
                               search.shape[2] * search.shape[3]).data) / 2
        cls_loss, loc_loss, cen_loss = self.loss_evaluator(locations, cls, loc, cen, label_cls, label_loc)

        # get loss
        outputs = {}
        outputs['total_loss'] = cfg.TRAIN.CLS_WEIGHT * cls_loss + \
                                cfg.TRAIN.LOC_WEIGHT * loc_loss + cfg.TRAIN.CEN_WEIGHT * cen_loss + cfg.TRAIN.CG_WEIGHT * spcls
        outputs['cls_loss'] = cls_loss
        outputs['loc_loss'] = loc_loss
        outputs['cen_loss'] = cen_loss
        return outputs
