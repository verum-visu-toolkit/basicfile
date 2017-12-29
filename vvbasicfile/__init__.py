# import ijson
try:
    import ijson.backends.yajl2_cffi as ijson  # use yajl2 and cffi; much faster
    print('using yajl ijson backend')
except ImportError:
    import ijson  # use pure-python parser
    print('using pure python ijson backend')

# Static basicfile formats

import static

# Streaming basicfile formats

from .fmsfile import FmsFormatReader, FmsFrameMaker, FmsFormatWriter
from .rndfile import RndFormatReader, RndFrameMaker, RndFormatWriter
from .utils import load_basicfile_field
