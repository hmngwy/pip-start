#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Package configuration."""

import os

from os.path import basename
from os.path import splitext
from os.path import join

from setuptools import setup
from setuptools import find_packages

REQMNTS = {'base': [], 'setup': [], 'test': []}
SCRIPTS = []

if os.path.isdir('requirements'):
    for fin in os.listdir('requirements'):
        if fin.endswith('.txt'):
            with open(join('requirements', fin)) as f:
                handle = splitext(basename(fin))[0]
                REQMNTS[handle] = f.read().splitlines()

if os.path.isdir('requirements'):
    for fin in os.listdir('bin'):
        SCRIPTS.append(join('bin', fin))

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name='skeleton',
    version='0.0.0',
    description='A short description.',
    long_description=README,
    author='John Doe',
    author_email='john@doe.com',
    url='https://github.com/johndoe/skeleton',
    packages=find_packages(include=['skeleton']),
    scripts=SCRIPTS,
    test_suite='tests',
    install_requires=REQMNTS['base'],
    setup_requires=REQMNTS['setup'],
    tests_require=REQMNTS['test'],
    extras_require=REQMNTS
)
