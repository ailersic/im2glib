"""
im2glib: Raster/DXF Image to G code Converter Package
Author: Andrew Ilersich
Last modified: August 19, 2015
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'im2glib',
    version = '0.0.0',
    description = 'A package that converts raster images and DXF files into G code for CNC machines',
    long_description = long_description,

    url = 'https://github.com/ailersic/im2glib',
    author = 'Andrew Ilersich',
    author_email = 'andrew.ilersich@mail.utoronto.ca',

    license = 'MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers =
    [
        'Development Status :: 3 - Alpha',
    
        'Intended Audience :: Students',
        'Topic :: Software Development :: Build Tools',
    
        'License :: OSI Approved :: MIT License',
    
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords = 'im2glib cnc image picture raster dxf gcode g code interpreter converter',

    install_requires = ['pySerial', 'pillow'],
	packages = ['im2glib'],
    zip_safe = False
)