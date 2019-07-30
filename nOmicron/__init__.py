#   Copyright © Oliver Gordon, 2019

"""
nOmicron package/API for automatically control of Matrix through Python
"""

__version__ = '1.0'

__all__ = ['mate', 'microscope', 'utils']
name = "nOmicron"

from .mate import *
from .microscope import *
from .utils import *
