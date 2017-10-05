#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Package configuration."""

import sys

import os
from os.path import join

from setuptools import setup
from setuptools.command.test import test as TestCommand

# To build this project you must be in an env that has pipenv
from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

PFILE = Project(chdir=False).parsed_pipfile
REQUIRES = convert_deps_to_pip(PFILE['packages'], r=False)
TEST_REQUIRES = convert_deps_to_pip(PFILE['dev-packages'], r=False)

HERE = os.path.abspath(os.path.dirname(__file__))
PKG_DIR = 'skeleton'

# Packages in the distribution build
PACKAGES = [PKG_DIR]


class PyTest(TestCommand):
    """setup.py test override class."""

    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count
            self.pytest_args = ['-n', str(cpu_count()), '--boxed']
        except (ImportError, NotImplementedError):
            self.pytest_args = ['-n', '1', '--boxed']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


# Autoload bin/* into packages scripts
SCRIPTS = []
for fin in os.listdir('bin'):
    SCRIPTS.append(join('bin', fin))

ABOUT = {}
with open(os.path.join(HERE, PKG_DIR, "__version__.py")) as f:
    exec(f.read(), ABOUT)  # pylint: disable=W0122

with open('README.md', 'r') as f:
    README = f.read()
with open('HISTORY.md', 'r') as f:
    HISTORY = f.read()


setup(
    name=ABOUT['__title__'],
    version=ABOUT['__version__'],
    description=ABOUT['__description__'],
    long_description=README + '\n\n' + HISTORY,
    author=ABOUT['__author__'],
    author_email=ABOUT['__author_email__'],
    url=ABOUT['__url__'],
    install_requires=REQUIRES,
    packages=PACKAGES,
    package_data={'': ['LICENSE', 'NOTICE'], PKG_DIR: ['*.pem']},
    package_dir={ABOUT['__title__']: PKG_DIR},
    include_package_data=True,
    license=ABOUT['__license__'],
    zip_safe=False,
    scripts=SCRIPTS,
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python'
    ),
    cmdclass={'test': PyTest},
    test_suite='tests',
    tests_require=TEST_REQUIRES
)
