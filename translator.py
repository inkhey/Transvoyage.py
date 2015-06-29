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
        self.logLevel=logLevel
        self.logger.setLevel(logLevel)
        self.args=args
        content=self.preformat(content)
        self.text=mwparserfromhell.parse(content)

    def clean(self):
        rmlist=[]
        for node in self.text.nodes:
            if isinstance(node, mwparserfromhell.nodes.Text):
                node.value="\n"
            elif ( not isinstance(node, mwparserfromhell.nodes.Heading)
                    and not isinstance(node, mwparserfromhell.nodes.Template)):
                rmlist.append(node)
        for node in rmlist:
            self.text.remove(node)

    def preformat(self,text):
        csv = './db/preformat.csv'
        db = DB(csv,self.args['src'],self.args['dest'],self.logLevel)
        for elem in db.getList():
            trans = db.getTranslation(elem)
            if trans:
                text=re.sub(elem,trans,text)
        return text

    def translate(self):
        self.clean()
        self.transHeadings()
        self.transListings()

    def transType(self):
        pass

    def transListings(self):
        '''Translate listing'''
        #init DB
        csv = './db/listings.csv'
        db = DB(csv,self.args['src'],self.args['dest'],self.logLevel)
        dbList = db.getList()
        #arg DB
        argcsv = './db/listingparams.csv'
        argdb = DB(argcsv,self.args['src'],self.args['dest'],self.logLevel)
        argList = argdb.getList()
        rmlist=[]
        for element in self.text.filter_templates(recursive=True):
            if element.name.matches(dbList):
                trans = db.getTranslation(element.name)
                if trans:
                    element.name = trans
                for param in element.params:
                    if param.name.matches(argList):
                        trans = argdb.getTranslation(param.name)
                        if trans:
                            param.name=trans
            else:
                rmlist.append(element)
        for element in rmlist:
            self.text.remove(element)

    def transHeadings(self):
        '''Translate headings'''
        #init DB
        csv = './db/headings.csv'
        db = DB(csv,self.args['src'],self.args['dest'],self.logLevel)
        dbList = db.getList()
        for element in self.text.filter_headings(recursive=False):
            if element.title.matches(dbList):
                trans = db.getTranslation(element.title)
                if trans:
                    element.title = trans

    def transStatus(self):
        pass

    def __str__(self):
        ret=str(self.text)
        ret=re.sub("(\n+)","\n",ret)
        return ret

if __name__ == '__main__':
    string="""* {{flag|Zimbabwe}} {{listing
    | name=Zimbabwe | url= | email=
    | address=Axel-Springer-Straße 54a/Kommundantenstr. 80 | lat= | long= | directions=
    | phone=+49 30 206 2263 | tollfree= | fax=
    | hours=M-F 09:00-13:00, 14:00-16:00 | price=
    | content=
    }}
    |}"""
    args={'src':'en','dest':'fr'}
    t= Translator(string,args)
    t.translate()
    print(t)
