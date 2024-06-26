
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pysot.models.fusion.cfmf import cfmf

FS = {
    'cfmf': cfmf,
}


def get_FS(name, **kwargs):
    return FS[name](**kwargs)

