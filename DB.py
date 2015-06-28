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

import csv
import logging
logging.basicConfig()

class DB(object):
    "Translation database object to translate file"

    def __init__(self,filename,langS,langD,logLevel=logging.WARNING):
        '''create DB'''
        self.logger = logging.getLogger("DB")
        self.logger.setLevel(logLevel)
        self.db={}
        self.langS=langS
        self.langD=langD
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile,delimiter=';')
            for row in reader:
                val=row['globalref']
                row.pop('globalref')

                #drop useless lang data
                listLang=[langS,langD]
                delLang = [lang for lang in row if lang not in listLang]
                for lang in delLang:
                    row.pop(lang)
                self.db[val]=row

    def getList(self):
        '''get list of elements from source language'''
        l=[]
        for row in self.db:
            if self.langS in self.db[row]:
                l.append(self.db[row][self.langS])
        return l

    #def existInList(self,value)
    #   for elem in self.getList:
    #        if value.match(

    def getTranslation(self,source):
        '''get translation of a source language element'''
        source=str(source).replace("\n","")
        source=source.lower()
        for row in self.db:
            if ( self.langS in self.db[row]
                  and self.db[row][self.langS].lower() == source
                  and self.db[row][self.langD] ):
                    return self.db[row][self.langD]
        return False

    def __str__(self):
        return str(self.db).replace('},','},\n')

if __name__ == '__main__':

    db = DB('./db/listingparams.csv','en','fr')
    l = db.getList()
    print(l)
    for elem in l:
        print(db.getTranslation(elem))
