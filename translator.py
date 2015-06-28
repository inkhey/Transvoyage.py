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
import DB
import logging
import setting
import mwparserfromhell
logging.basicConfig()

class Translator(object):
    """Translation of file"""

    def __init__(self,content,args,logLevel=setting.LOGLEVEL):
        self.logger = logging.getLogger("Translator")
        self.logger.setLevel(logLevel)
        self.text=mwparserfromhell.parse(content)

    def translate(self):
        pass

    def transType(self):
        pass

    def transSection(self):
        pass

    def transStatus(self):
        pass

    def __str__(self):
        return str(self.text)

