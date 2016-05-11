#!/usr/bin/env python

import codecs
import os
import re
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^VERSION = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

long_description = read('README.rst')

setup(
    url = 'https://github.com/densho/ddr-idservice/',
    download_url = 'https://github.com/densho/ddr-idservice.git',
    name = 'ddr-idservice',
    description = 'ddr-idservice',
    long_description = long_description,
    version = find_version('idservice', '__init__.py'),
    #license = 'TBD',
    author = 'Geoffrey Jost',
    author_email = 'geoffrey.jost@densho.org',
    platforms = 'Linux',
    classifiers = [  # https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Other Audience',
        #'License :: OSI Approved :: TBD',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Other/Nonlisted Topic',
        'Topic :: Sociology :: History',
    ],
    install_requires = [],
    packages = [],
    include_package_data = True,
    package_dir = {},
    package_data = {},
    scripts = [
        'bin/ddr-idservice',
    ],
)
