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
from DB import DB, DBnumber, DBDouble
import logging
import setting
import mwparserfromhell
import re
logging.basicConfig()


class Translator(object):

    """Translation of file"""

    def __init__(self, content, args, logLevel=setting.LOGLEVEL):
        self.logger = logging.getLogger("Translator")
        self.logLevel = logLevel
        self.logger.setLevel(logLevel)
        self.args = args
        content = self.preformat(content)
        self.text = mwparserfromhell.parse(content, skip_style_tags=True)
        self.rmList = []

    def preformat(self, text):
        csv = './db/preformat.csv'
        db = DB(csv, self.args['src'], self.args['dest'], self.logLevel)
        for elem in db.getList():
            trans = db.getTranslation(elem)
            if trans:
                text = re.sub(elem, trans, text)
        return text
    # translate

    def translate(self):
        self.transHeadings()
        self.transListings()
        self.clean()
    # Translate

    def transType(self):
        pass

    def transListings(self):
        '''Translate listing'''
        # Listing DB
        csv = './db/listings.csv'
        db = DB(csv, self.args['src'], self.args['dest'], self.logLevel)
        dbList = db.getList()
        # Listignarg DB
        csv = './db/listingparams.csv'
        argdb = DB(csv, self.args['src'], self.args['dest'], self.logLevel)
        argList = argdb.getList()
        # Map params DB
        csv = './db//specialModule/Map/mapparams.csv'
        mapdb = DBnumber(
            csv, self.args['src'], self.args['dest'], self.logLevel)
        mapList = mapdb.getList()
        # Climate params DB
        csv = './db/specialModule/Climate/arg.csv'
        csv2 = './db//specialModule/Climate/month.csv'
        climatedb = DBDouble(
            csv, csv2, self.args['src'], self.args['dest'], 'm', self.logLevel)
        climateList = climatedb.getList()
        # type DB
        csv = './db/specialModule/Climate/arg.csv'
        csv2 = './db//specialModule/Climate/month.csv'
        # Translation
        for element in self.text.filter_templates(recursive=True):
            # listings
            if element.name.matches(dbList):
                trans = db.getTranslation(element.name)
                if trans:
                    element.name = trans
                # params
                for param in element.params:
                    if param.name.matches(argList):
                        trans = argdb.getTranslation(param.name)
                        if trans:
                            param.name = trans
                    elif self._re__list_match(str(param.name), mapList):
                        trans = mapdb.getTranslation(param.name)
                        if trans:
                            param.name = trans
                    elif self._re__list_match(str(param.name), climateList):
                        trans = climatedb.getTranslation(param.name)
                        if trans:
                            param.name = trans
                    else:
                        self.rmList.append(param)
            else:
                self.rmList.append(element)

    def _re__list_match(self, elem, l):
        for pattern in l:
            if pattern and re.match(pattern, elem):
                return True
        return False

    def transHeadings(self):
        '''Translate headings'''
        # init DB
        csv = './db/headings.csv'
        db = DB(csv, self.args['src'], self.args['dest'], self.logLevel)
        dbList = db.getList()
        for element in self.text.filter_headings(recursive=False):
            if element.title.matches(dbList):
                trans = db.getTranslation(element.title)
                if trans:
                    element.title = trans
    # postFormat

    def clean(self):
        for node in self.text.nodes:
            if isinstance(node, mwparserfromhell.nodes.Text):
                node.value = "\n"
            if isinstance(node, mwparserfromhell.nodes.Wikilink):
                self.rmList.append(node)
            if isinstance(node, mwparserfromhell.nodes.Wikilink):
                self.rmList.append(node)
            if isinstance(node, mwparserfromhell.nodes.ExternalLink):
                self.rmList.append(node)
            if isinstance(node, mwparserfromhell.nodes.Comment):
                self.rmList.append(node)
            if isinstance(node, mwparserfromhell.nodes.HTMLEntity):
                self.rmList.append(node)
        for node in self.rmList:
            self.text = str(self.text).replace(str(node), "")
        self.text = mwparserfromhell.parse(self.text)

    def addHeader(self):
        pass

    def __str__(self):
        ret = str(self.text)
        ret = re.sub("(\n+)", "\n", ret)
        return ret

if __name__ == '__main__':

    string = """* {{flag|Zimbabwe}} {{listing
    | name=Zimbabwe | url= | email=
    | address=Axel-Springer-Straße 54a/Kommundantenstr. 80 | lat= | long= | directions=
    | phone=+49 30 206 2263 | tollfree= | fax=
    | hours=M-F 09:00-13:00, 14:00-16:00 | price=
    | content=
    }}
    |}"""
    string2 = """{{regionlist|carte=berlin_map_new.png
|taillecarte=450px
|carte=Districts of Berlin
|region1name=[[Berlin/Mitte|Mitte]]
|region1color=#c9815e
|region1items=''Mitte''
|region1description=The historical centre of Berlin, the nucleus of the former East Berlin, and the emerging city centre. Cafés, restaurants, museums, galleries, and clubs are abundant throughout the district, along with many sites of historic interest.
|region2name=[[Berlin/City West|City West]]
|region2color=#67b7b7
|region2items=''Charlottenburg, Wilmersdorf, Schöneberg, Tiergarten''
|region2description=Ku'Damm (short for ''Kurfürstendamm'') is, along with Tauentzienstraße, one of the main shopping streets in former West Berlin, especially for luxury goods. Many great restaurants and hotels are here and also on the side roads. The district also contains the Schloss Charlottenburg, Tiergarten and the Olympic Stadium. Schöneberg is generally a cosy area for ageing hippies, young families, and [[LGBT]] people.
|region3name=[[Berlin/East Central|East Central]]
|region3color=#75bb75
|region3items=''Friedrichshain, Kreuzberg, Prenzlauer Berg''
|region3description=Associated with the left wing youth culture, artists, and Turkish immigrants, this district is somewhat noisier than most, packed with lots of cafés, bars, clubs, and trendy shops, but also with some museums in Kreuzberg near the border to Mitte. These districts are undergoing gentrification as they are popular with students, artists and media professionals alike.
|region4name=[[Berlin/North|North]]
|region4color=#bdbd7b
|region4items=''Spandau, Reinickendorf, Weißensee, Pankow, Wedding''
|region4description=Spandau and Reinickendorf are beautiful old towns, which feel much more spacious than the inner city. Pankow was once synonymous with the East German government, and the villas the East German "socialist" leaders inhabited still exist.
|region5name=[[Berlin/East|East]]
|region5color=#8888dc
|region5items=''Lichtenberg, Hohenschönhausen, Marzahn, Hellersdorf''
|region5description=The museum at the site of the 1945 surrender to the Soviet army is of interest, as well as the former Stasi prison, an essential visit for anyone interested in East German history. Marzahn-Hellersdorf has an undeserved reputation for being a vast collection of dull high-rise apartment blocks, as it also contains the [http://www.gruen-berlin.de/parks-gardens/gardens-of-the-world/ "Gardens of the World"], a large park where various ethnic styles of garden design are explored.
|region6name=[[Berlin/South|South]]
|region6color=#aa6baa
|region6items=''Steglitz, Zehlendorf, Tempelhof, Neukölln, Treptow, Köpenick''
|region6description=The South is a mixed bag of different boroughs. Zehlendorf is one of the greenest and wealthiest boroughs in Berlin, while Neukölln is one of the city's poorest. However at least the Northern part of Neukölln (sometimes labeled "Kreuzkölln") is becoming more and more gentrified. Köpenick's swaths of forest around Berlin's largest lake, Müggelsee, and the nice old town of Köpenick itself beg to be discovered on bikes and using the S-Bahn.}}"""
    args = {'src': 'en', 'dest': 'fr'}
    t = Translator(string, args)
    t.translate()
    print(t)
