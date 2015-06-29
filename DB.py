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
import re
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
        self._initDB(filename,self.db)
        self.logger.info("init DB ok")


    def _initDB(self,filename,db):
        '''initialise DB'''
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile,delimiter=';')
            for row in reader:
                self.logger.debug("read row-before :\t"+str(row))
                val=row['globalref']
                row.pop('globalref')
                #drop useless lang data
                listLang=[self.langS,self.langD]
                delLang = [lang for lang in row if lang not in listLang]
                for lang in delLang:
                    row.pop(lang)
                self.logger.debug("read row-after :\t"+str(row))
                #store data
                db[val]=row

    def getList(self):
        '''get list of elements from source language'''
        l=[]
        for row in self.db:
            if self.langS in self.db[row]:
                l.append(self.db[row][self.langS].lower())
        return l

    def _getTranslationDB(self,source,db):
        '''get translation of a source language element'''

        source=str(source).replace("\n","")
        source=source.lower()
        for row in db:
            if ( self.langS in db[row]
                  and db[row][self.langS].lower() == source
                  and db[row][self.langD] ):
                    return db[row][self.langD]
        return False
    def getTranslation(self,source):
        '''get translation of a source language element'''
        return self._getTranslationDB(source,self.db)

    def __str__(self):
        return str(self.db).replace('},','},\n')


class DBnumber(DB):
    '''DB with [n] params converted as number'''
    def getList(self):
        '''get list of elements from source language'''
        l=[]
        for row in self.db:
            if self.langS in self.db[row]:
                elem = self.db[row][self.langS].lower()
                elem = elem.replace('[n]','(?P<number>[0-9]+)')
                l.append(elem)
        return l

    def getTranslation(self,source):
        '''get translation of a source language element'''
        source=str(source).replace("\n","")
        source=source.lower()
        for row in self.db:
            if ( self.langS in self.db[row]):
                tmpLangS = self.db[row][self.langS].lower()
                tmpLangS = tmpLangS.replace('[n]','(?P<number>[0-9]+)')
                self.logger.debug("tmpLangS:\t"+tmpLangS)
                self.logger.debug("source:\t"+source)
                if tmpLangS:
                    test = re.match(tmpLangS,source)
                    self.logger.debug("test:\t"+str(bool(test)))
                    if test:
                        #get [n] value ?
                        number=""
                        if "[n]" in self.db[row][self.langS]:
                            number=test.group('number')
                            self.logger.debug("number:\t"+number)
                        if self.db[row][self.langD]:
                            dest = self.db[row][self.langD]
                            self.logger.debug("dest-before:\t"+dest)
                            dest = dest.replace('[n]',number)
                            self.logger.debug("dest-after:\t"+dest)
                            return dest
        return False

class DBDouble(DB):
    '''DB with database value as params'''

    def __init__(self,filename,filename2,langS,langD,
            nameParam="w",logLevel=logging.WARNING):
        super().__init__(filename,langS,langD,logLevel)
        self.nameParam=nameParam
        self.db2={}
        self._initDB(filename2,self.db2)
        self.logger.info("init DBDouble ok")


    def getList(self):
        '''get list of elements from source language'''
        l=[]
        for row in self.db:
            if self.langS in self.db[row]:
                elem = self.db[row][self.langS].lower()
                elem = elem.replace('['+self.nameParam+']','(?P<word>.+)')
                l.append(elem)
        return l
    def getTranslation(self,source):
        '''get translation of a source language element'''
        source=str(source).replace("\n","")
        source=source.lower()
        for row in self.db:
            if self.langS in self.db[row]:
                tmpLangS = self.db[row][self.langS].lower()
                tmpLangS = tmpLangS.replace('['+self.nameParam+']','(?P<word>.+)')
                self.logger.debug("tmpLangS:\t"+tmpLangS)
                self.logger.debug("source:\t"+source)
                if tmpLangS:
                    test = re.match(tmpLangS,source)
                    self.logger.debug("test:\t"+str(bool(test)))
                    if test:
                        #get word value ?
                        word=""
                        wordTrans=""
                        if '['+self.nameParam+']' in self.db[row][self.langS]:
                            word=test.group('word')
                            self.logger.debug("word:\t"+word)
                            wordTrans=self._getTranslationDB(word,self.db2)
                            if not wordTrans:
                                wordTrans=word
                            self.logger.debug("wordTrans:\t"+wordTrans)
                        if self.db[row][self.langD]:
                            dest = self.db[row][self.langD]
                            self.logger.debug("dest-before:\t"+dest)
                            if wordTrans:
                                dest=dest.replace('['+self.nameParam+']',wordTrans)
                            self.logger.debug("dest-after:\t"+dest)
                            return dest
        return False
    def __str__(self):
        ret=super().__str__()
        ret+="\n\n"
        ret+=str(self.db2).replace('},','},\n')
        return ret


if __name__ == '__main__':
    print("====DB====")
    print("\n##init\n")
    db = DB('./db/listingparams.csv','en','fr',logging.DEBUG)
    print("\n##getList\n")
    l = db.getList()
    print(l)
    print("\n##translations\n")
    for elem in l:
        print(db.getTranslation(elem))
    print("\n##str method\n")
    print(db)
    print("\n\n\n")

    print("====DBDNumber====")
    print("\n##init\n")
    db = DBnumber('./db/specialModule/Map/mapparams.csv','en','fr',logging.DEBUG)
    print("\n##getList\n")
    l = db.getList()
    print(l)
    print("\n##translations of region12description\n")
    print(db.getTranslation("region12description"))
    print("\n##translations of regionmap\n")
    print(db.getTranslation("regionmap"))
    print("\n##str method\n")
    print(db)
    print("\n\n\n")

    print("====DBDouble====")
    print("\n##init\n")
    db = DBDouble('./db/specialModule/Climate/arg.csv',
        './db/specialModule/Climate/month.csv','en','fr','m',logging.DEBUG)
    print("\n##getList\n")
    l = db.getList()
    print(l)
    print("\n##translations of julhigh\n")
    print(db.getTranslation("junhigh"))
    print("\n##str method\n")
    print(db)
