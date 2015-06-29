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

# sys
import sys
import os
import subprocess
import urllib.request
import urllib.error
import urllib.parse
# regex
import re
# translate
import locale
import gettext
#settings
from setting import *
from translator import Translator
# other
import logging
logging.basicConfig()

# init translation
def initTranslation():
    ''' init Translation with gettext'''

    lang = gettext.NullTranslations()
    try:
        lang = gettext.translation(APP, localedir=LOCALE_DIR)
    except IOError:
        pass
    lang.install()


def translateArgparse(Text):
    ''' to Translate argparse module'''

    Text = Text.replace("usage", _("usage"))
    Text = Text.replace("show this help message and exit",
                        _("show this help message and exit"))
    Text = Text.replace("error:", _("error:"))
    Text = Text.replace("the following arguments are required:",
                        _("the following arguments are required:"))
    Text = Text.replace("too few arguments",
                        _("too few arguments"))
    return Text

initTranslation()
gettext.gettext = translateArgparse
import argparse


class Transvoyage(object):

    "CLI interface of Transvoyage.py"


    def readCli(self):
        '''CLI:Argument parser'''

        parser = argparse.ArgumentParser()
        parser.add_argument(
            'title',
            metavar=_('title'),
            help=_("name of page to convert")
        )
        parser.add_argument(
            '-p',
            '--path',
            help=_("use a local path file")
        )
        parser.add_argument(
            '--src',
            help=_("source language : fr,en,…"),
            default='en'
        )

        parser.add_argument(
            '--dest',
            help=_("destination language : fr,en,…"),
            default='fr'
        )
        parser.add_argument(
            '-d',
            '--debug',
            action='store_true',
            help=_(
                "debug mod : source page available at the same time as result")
        )
        parser.add_argument(
            '-C',
            '--nocomment',
            action='store_true',
            help=_("unable comments in source language in result page.")
        )
        parser.add_argument(
            '-o',
            '--output',
            action='store_true',
            help=_("output file.")
        )
        parser.add_argument(
            '--proxy',
            default=None,
            help=_("use proxy to find wikivoyage webpage.")
        )
        self.args = parser.parse_args()
        self.args.dest = self.args.dest.lower()
        self.args.src = self.args.src.lower()

        # Verify args
        if not (self.args.src in S_LANG):
            self.logger.error("Bad source language value.")
            return False

        if not (self.args.dest in S_LANG):
            self.logger.error("Bad destination language value.")
            return False

        return True

    def getFilebByUrl(self):
        ''' Obtain wikivoyage file by downloading'''

        assert(self.args.title)
        assert(self.args.dest)
        assert(self.args.src)
        assert(self.args.dest in S_LANG)
        assert(self.args.src in S_LANG)

        # correct url
        url = D_URL.replace("[L]", self.args.src)
        url = url.replace("[T]", self.args.title)
        self.url = url

        # proxy conf
        if self.args.proxy:
            proxy_handler = urllib.request.ProxyHandler({self.proxy})
            opener = urllib.request.build_opener(proxy_handler)
        # try download file
        try:
            self.doc = urllib.request.build_opener().open(url).read().decode("utf-8")
        except:
            self.logger.error(_("Failed to download wikivoyage webpage."))
            return False
        return True

    def getFileByPath(self):
        ''' Obtain wikivoyage file from local file'''
        pass

    def __init__(self,logLevel=LOGLEVEL):
        ''' Launch CLI'''

        self.logger = logging.getLogger("Transvoyage")
        self.logger.setLevel(logLevel)

        if self.readCli():
            bFile = False
            if self.args.path:
                bFile = self.getFileByPath()
            else:
                bFile = self.getFilebByUrl()

            if bFile:
                self.translator=Translator(self.doc,
                    vars(self.args),LOGLEVEL)
                self.translator.translate()
                if self.args.output:
                    self.saveFile()
                else:
                    print(self.__str__())
            else:
                print (_("No file"))

    def __str__(self):
        '''Print text'''

        if self.translator:
            return str(self.translator)
        else :
            return _("No file")

    def saveFile(self):

        with open("./"+self.args.title+".txt", "w") as doc:
            doc.write(self.__str__())


if __name__ == '__main__':

    t = Transvoyage()
