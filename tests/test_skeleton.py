# -*- coding: utf-8 -*-

"""Tests for skeleton."""
from skeleton import __version__


def test_version():
    """Test if version set."""
    assert __version__.__version__ == '0.0.0'
