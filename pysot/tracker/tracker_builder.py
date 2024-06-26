from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pysot.tracker.siamcar_tracker import SiamCARTracker

TRACKS = {
          'SiamCARTracker': SiamCARTracker
         }


def build_tracker(model, cfg):
    return TRACKS[model, cfg]
SiamCARTracker