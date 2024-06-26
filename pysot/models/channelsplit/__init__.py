from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pysot.models.channelsplit.ssse import ssse

BS = {
    'ssse': ssse,
}


def get_BS(name, **kwargs):
    return BS[name](**kwargs)
