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
from DB import DB
import logging
import setting
import mwparserfromhell
import re
logging.basicConfig()

class Translator(object):
    """Translation of file"""

    def __init__(self,content,args,logLevel=setting.LOGLEVEL):
        self.logger = logging.getLogger("Translator")
        self.logger.setLevel(logLevel)
        self.text=mwparserfromhell.parse(content)
        self.args=args

    def translate(self):
        self.transHeadings()
        self.transListings()

    def transType(self):
        pass

    def transListings(self):
        '''Translate listing'''
        #init DB
        csv = './db/listings.csv'
        db = DB(csv,self.args['src'],self.args['dest'])
        dbList = db.getList()
        #arg DB
        argcsv = './db/listingparams.csv'
        argdb = DB(argcsv,self.args['src'],self.args['dest'])
        argList = argdb.getList()

        for element in self.text.filter_templates(recursive=False):
            if element.name.matches(dbList):
                trans = db.getTranslation(element.name)
                if trans:
                    element.name = trans
                #for param in element.params:
                #    if re.matche(argList,param):
                #        trans = db.getTranslation(param)
                #        element.params[param]=trans

    def transHeadings(self):
        '''Translate headings'''
        #init DB
        csv = './db/headings.csv'
        db = DB(csv,self.args['src'],self.args['dest'])
        dbList = db.getList()
        for element in self.text.filter_headings(recursive=False):
            if element.title.matches(dbList):
                trans = db.getTranslation(element.title)
                if trans:
                    element.title = trans

    def transStatus(self):
        pass

    def __str__(self):
        return str(self.text)

