
import os
import setuptools
from version import version as this_version

this_directory =  os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'MK8D', '_version.py'), 'wt') as fversion:
    fversion.write('__version__ = "'+this_version+'"')


REQUIRED_PACKAGES=[
    'matplotlib>=3.3.2'
]


with open("README.md", "r") as fh:
    long_description = fh.read()