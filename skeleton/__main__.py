# -*- coding: utf-8 -*-
"""Top-level package for skeleton."""

import requests

WAN = requests.get('http://ipinfo.io/ip')
print(WAN.text)
