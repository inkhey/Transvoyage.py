#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Transvoyage.py
#
#  Copyright 2015 Guénaël Muller <contact@inkey-art.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
import logging
# Global vars
APP = "transvoyage"
LOCALE_DIR = "./locale"
D_LANG_SOURCE = "en"   # default source language
D_LANG_DEST = "fr"   # default destination language
S_LANG = ["fr", "en"] # supported languages
#Download url
D_URL = "https://[L].wikivoyage.org/w/index.php?title=[T]&action=raw"
LOGLEVEL=logging.WARNING
