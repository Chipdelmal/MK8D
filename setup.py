
import os
import setuptools
from version import version as this_version

this_directory =  os.path.abspath(os.path.dirname(__file__))
version_path = os.path.join(this_directory, 'MK8D', '_version.py')
with open(version_path, 'wt') as fversion:
    fversion.write('__version__ = "'+this_version+'"')


REQUIRED_PACKAGES=[
    'matplotlib>=3.3.2', 'xmltodict>=0.12.0',
    'pandas>=1.1.4', 'numpy>=1.19.4', 'plotly>=4.13.0',
    'plotly-express>=0.4.1', 'colour>=0.1.5'
]


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="MK8D",                                                # name of project
    install_requires=REQUIRED_PACKAGES,                         # all requirements used by this package
    version=this_version,                                       # project version, read from version.py
    author="chipdelmal",                                        # Author, shown on PyPI
    scripts=['./bin/MK8D_lss_parse'],                           # command line scripts installed
    author_email="chipdelmal@gmail.com",                        # Author email
    description="Mario Kart 8 Deluxe livesplit analyzer",       # Short description of project
    long_description=long_description,                          # Long description, shown on PyPI
    long_description_content_type="text/markdown",              # Content type. Here, we used a markdown file.
    url="https://github.com/Chipdelmal/MK8D",                   # github path
    packages=setuptools.find_packages(),                        # automatically finds packages in the current directory. You can also explictly list them.
    classifiers=[                                               # Classifiers give pip metadata about your project. See https://pypi.org/classifiers/ for a list of available classifiers.
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',                                    # python version requirement
)