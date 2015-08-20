'''
Raster/DXF Image to G code Converter Package
Author: Andrew Ilersich
Last modified: August 19, 2015
'''

__author__ = 'Andrew Ilersich'
__email__ = 'andrew.ilersich@mail.utoronto.ca'
__version__ = '0.0.0'
__all__ = ['gOut', 'gRead', 'config']

# Import user-intended package functions
from im2glib.gRead import imToPaths
from im2glib.gOut import toTextFile, toSerial
from im2glib.config import IMDIM, SMOOTHERR