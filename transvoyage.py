#!/usr/bin/python
# -*- coding: utf-8 -*-
#  transvoyage.py
#  Version 0.3
#  
#  Copyright 2014 Guénaël Muller <contact@inkey-art.net>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
# 
#TODO
# - se conformer à la PEP 8
# - commentaires et TODO bilingue.
# - optimisations
# -	traduction inversé amélioré
# - nouveau langages
# - debugage de certains regex et autres


import sys
import os
import subprocess 
import re
import urllib
import argparse

# traductions des types Articles

listTypeFr=('Ville','Région continentale','Région','Pays'   ,'Quartier','Itinéraire','Parc')
listTypeEn=('city' ,'continent'          ,'region','country','district','itinerary' ,'park')


#Equivalences sections
listSectionFr=["Comprendre","Aller" ,"Circuler"  ,"Voir","Faire","Acheter","Manger","Boire un verre / Sortir","Se loger","Aux environs","Travailler","Apprendre","Gérer le Quotidien","Sécurité","Communiquer"]
listSectionEn=["Understand","Get in","Get around","See" ,"Do"   ,"Buy"    ,"Eat"   ,"Drink"                  ,"Sleep"   ,"Go next","Work"           ,"Learn"     ,"Cope"             ,"Stay safe", "Connect"   ]

listSectionFr.extend(["Respecter","Parler","Éléctricité"])
listSectionEn.extend(["Respect","Talk","Electricity"])

listSectionFr.extend(["Se préparer","Étapes","Autres destinations","Lire","Douanes","En taxi","Santé","Monnaie","Villes","Régions","Quartiers","Bureaux d'information touristique"])
listSectionEn.extend(["Prepare","Route","Other destinations","Read","Customs","By taxi","Stay healthy","Currency","Cities","Regions","Districts","Tourist office"])

listSectionFr.extend(['Histoire', 'Paysage', 'Flore et faune',"Climat","Randonnée","Droits d'accès","Droits d'accès","Activités","Météo","Nature"])
listSectionEn.extend(['History', 'Landscape', 'Flora and fauna',"Climate","Hiking","Fees/permits","Fees/Permits","Activities","Weather","Wildlife"])

listSectionFr.extend(['À pied', 'En train', 'En bus',"En avion","En ferry","En bateau","En voiture","En vélo","En vélo","En vélo","En motoneige","En stop"])
listSectionEn.extend(['By foot', 'By train', 'By bus',"By plane","By ferry","By boat","By car","By bicycle","By cycle","By bike","By snowmobile","By thumb"])

listSectionFr.extend(['Bon marché', 'Prix moyen','Prix moyen', 'Luxe','Hôtel','Logements','Dans la nature'])
listSectionEn.extend(['Budget', 'Mid-range','Mid range', 'Splurge','Hotel','Lodging','Backcountry'])

# Équivalence image

listImageFr=["[[Fichier:","[[Fichier:","gauche","droite","vignette","vignette"]
listImageEn=["[[Image:","[[File:","left","right","thumbnail","thumb"]

#Equivalence Listings

#titre listings
listListingDebFr=["Listing","Faire","Voir","Acheter","Manger","Sortir","Se loger","Destination","Aller","Circuler"]
listListingDebEn=["listing","do" ,"see","buy","eat","drink","sleep","listing","listing","listing"]

#paramètres
listListingFr=["nom=","adresse=","téléphone","latitude=","longitude=","email=","direction=","numéro gratuit=","fax=","prix=","description=<!-- ","-->}}","arrivée=","départ=","horaire="]
listListingEn=["name=","address=" ,"phone","lat=","long=","email=","directions=","tollfree=","fax=","price=","content=","}}","checkin=","checkout=","hours="]

#Equivalence Itineraires
listItineraireFr=["Jour ",": De"," à "]
listItineraireEn=["Day ",":"," to "]

#Equivalence Dans
listDansFr=["Dans"]
listDansEn=["IsPartOf"]

#Equivalence Carte

#Debut
listMapDebFr=["ListeRegions","carte=","taillecarte="]
listMapDebEn=["Regionlist","regionmap=","regionmapsize="]

#Paramètres
listMapFr=["nomregion0=","couleurregion0=","elementsregion0=","descriptionregion0="]
listMapEn=["region0name=","region0color=","region0items=","region0description="]

# Tout les regex en string par langue de Destination
RegSFr=["(.*)\[\[(Image|Fichier):(.*)\s*$","(=+)(.*)(=+)(.*)","(.*){{(Listing|Faire|Voir|Acheter|Manger|Boire|Sortir|Se loger|Destination|Aller|Circuler)\s(.*)\s*$","(.*)}}[.\s]*$","{{Dans\|(.*)}}\s*$"]
#               0                                1                                2                                                            3           4 
RegSFr.extend(["^(=+)(.*) à (.*)(=+)\s*$","(.*){{ListeRegions(.*)","(.*)region([0-9]+)=(.*)","{{Avancement\|statut=(ébauche|esquisse|utilisable|guide|étoile)\|type=0}}(.*)","(.*){{Climat(.*)","(.*){{Représentation diplomatique"])
#                         5                  6                        7                                 8                                9                       10
RegSEn=["(.*)\[\[(Image|File):(.*)\s*$", "(=+)(.*)(=+)(.*)","(.*){{(listing|do|see|buy|eat|drink|sleep)\s(.*)\s*$","(.*)}}[.\s]*$","{{IsPartOf\|(.*)}}\s*$"]
#               0                                1                                2                                 3               4 
RegSEn.extend(["^(=+)(.*) to (.*)(=+)\s*$","(.*){{Regionlist(.*)","(.*)region(.*)name=(.*)","{{(outline|usable|guide|stub|star)0}}(.*)","(.*){{Climate(.*)","(.*){{flag|(.*)}}(.*){{Listing(.*)"])
#                         5                  6                        7                                 8                                9                       10

#Avancement
avFr="{{Avancement|statut=esquisse|type=0}}\n" 
avEn="{{outline0}}\n"

#Equivalence climat
listMoisFr=["jan","fev","mar","avr","mai","jui","jul","aou","sep","oct","nov","dec"]
listMoisEn=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]

listClimatFr=["Climat","description"]
listClimatEn=["Climate","description"]
for mois in listMoisFr :
	listClimatFr.append("tmin-"+mois)
	listClimatFr.append("tmax-"+mois)
	listClimatFr.append("prec-"+mois)
for mois in listMoisEn :
	listClimatEn.append(mois+"low")
	listClimatEn.append(mois+"high")
	listClimatEn.append(mois+"precip")


# Trousse à mots par langues
ListFr=(listTypeFr,listSectionFr,listImageFr,listListingDebFr,listListingFr,listItineraireFr,listDansFr,listMapDebFr,listMapFr,RegSFr,avFr,listClimatFr)
ListEn=(listTypeEn,listSectionEn,listImageEn,listListingDebEn,listListingEn,listItineraireEn,listDansEn,listMapDebEn,listMapEn,RegSEn,avEn,listClimatEn)
#           0         1            2               3           4             5                6              7           8         9    10  11

ListingsSpecialFr={"Villes":"Ville","Autres destinations":"Destinations","Aux environs":"Destinations"}
#lien langage/trousse
ListLang ={"fr":ListFr, "en":ListEn}

#Langue source et destination et contenu récupérer

src=ListEn
dest=ListFr
lang="en"
content=""
section=""
# Pour récupérér le type de l'article (Ville,Itinéraire,Quartier,etc…)
def recupTypeArticle() :
	typeArticle = dest[0][0]
	listRegex = list()
	for mot in src[0] :
		s=src[9][8].replace("0",mot)
		listRegex.append(re.compile(s))

	bOk=True
	for line in content:
		if (not bOk) :
			break
		for i in range (len(listRegex)) :
			if listRegex[i].search(line) :
				typeArticle=dest[0][i]
				bOk=False
				break
	return typeArticle
	
#Pour créer l'entête 
def creationEntete (typeArticle,titre) :
	s=""
	if dest==ListFr : # Si on traduit en français
		s="""{{Bannière page}}
{{Info """+typeArticle+"""
| nom=
| nom local=
| région=
| image=
| légende image=
| rivière=
| superficie=
| population=
| population agglomération=
| année population= 
| altitude=
| latitude=
| longitude=
| zoom=
| code postal=
| indicatif=
| adresse OT=
| horaire OT=
| téléphone OT=
| numéro gratuit OT=
| email OT=
| facebook OT=
| twitter OT=
| URL OT=
| URL officiel=
| URL touristique=
}}
"""
	return s
# Pour récupérer les images (et les traduire)
def recupImage(line) :
	s=line
	for i in range (len(src[2])) :
		s=s.replace(src[2][i],dest[2][i])
	return s
#Pour récupérer les sections et sous-sections
def recupSection(line) :
	s=line
	for i in range (len(src[1])) :
		s=s.replace(src[1][i],dest[1][i])
	return s
#Pour récupérer les listings
def recupListing(line,debut)	:
	s=line
	if debut :
		for i in range (len(src[3])) :
			s=s.replace(src[3][i],dest[3][i])
						
	for i in range (len(src[4])) :
		s=s.replace(src[4][i],dest[4][i])
	return s
	
#Pour récupérer les sections d'étapes
def recupItineraire(line) :
	s=line
	for i in range (len(src[5])) :
			s=s.replace(src[5][i],dest[5][i])
	return s

#Pour récupérer la catégorisation
def recupDans(line) :
	s=line
	for i in range (len(src[6])) :
			s=s.replace(src[6][i],dest[6][i])
	return s

#Pour récupérer les cartes avec régions
def recupMap(line,numMap) :
	s=line
	if numMap == 0 :
		for i in range (len(src[7])) :
				s=s.replace(src[7][i],dest[7][i])
	numPrec=str(numMap-1)
	sNumMap=str(numMap)
	for i in range (len(src[8])):
		src[8][i]=src[8][i].replace(numPrec,sNumMap)
		dest[8][i]=dest[8][i].replace(numPrec,sNumMap)
	if numMap > 0 :
		for i in range (len(src[8])) :
			s=s.replace(src[8][i],dest[8][i])
	return s
def recupClimat(line) :
	s=line
	for i in range (len(src[11])):
		s=s.replace(src[11][i],dest[11][i])
	return s

#Programme en lui même

parser = argparse.ArgumentParser()
parser.add_argument('title',help="nom de la page à convertir" )
parser.add_argument('--src',help="langage source : fr,en,… par défault fr ")
parser.add_argument('--dest',help="langage destination : fr,en,… par défault en ")
parser.add_argument('-d','--debug',action='store_true' ,help="mode debugage : récupération du fichier source en même temps que le résultat")
parser.add_argument('-C','--nocomment',action='store_true' ,help="commentaires désactivé dans le résultat ")

args = parser.parse_args()
bAv=False # Pour savoir si la bannière d'avancement à été placé
result="" # Pou stocké le resultat
#arguments
title=args.title
if args.src and args.src.lower() in ListLang.keys() :
	src=ListLang[args.src.lower()]
	lang=args.src.lower()
if args.dest and args.dest.lower() in ListLang.keys() :
	dest=ListLang[args.dest.lower()]
	
url="https://"+lang+".wikivoyage.org/w/index.php?title="+title+"&action=raw"
content=urllib.urlopen(url).readlines()
# on récupère le type de l'article et on crée l'entête
TypeArticle=recupTypeArticle()
result        +=creationEntete(TypeArticle,title)
# les différents regex
regImg        =re.compile(src[9][0])
regSection    =re.compile(src[9][1])
regListing    =re.compile(src[9][2])
regListingEnd =re.compile(src[9][3])
regDans       =re.compile(src[9][4])
regItineraire =re.compile(src[9][5])
regMap        =re.compile(src[9][6])
regNomRegion  =re.compile(src[9][7])
regClimat     =re.compile(src[9][9])
regDiplomat   =re.compile(src[9][10])
# On ouvre et on lit
i=0
numMap=-1
bClimat=False
bListing=False
for line in content:
	i=i+1
	if numMap>-1 :
		if regNomRegion.search(line) :
			numMap=numMap+1
		result+=recupMap(line,numMap)
		if regListingEnd.search(line) :
			sNumMap=str(numMap)
			for i in range (len(src[8])):
				src[8][i]=src[8][i].replace(sNumMap,"0")
				dest[8][i]=dest[8][i].replace(sNumMap,"0")
			numMap=-1
	if bClimat or regClimat.search(line):
		result+=recupClimat(line)
		bClimat=True
		if regListingEnd.search(line) :
			bClimat=False
	elif bListing :
		s=recupListing(line,False)
		if regListingEnd.search(line) :					
			bListing=False
			if not regListingEnd.search(s) :
				s+="}}"
		result+=s
	elif regDiplomat.search(line) and dest==ListFr :
		s="* {{Représentation diplomatique"
		bListing=True
		result+=s
	elif regMap.search(line) :
		numMap=0
		result+=recupMap(line,numMap)
	elif regItineraire.search(line) :
		result+=recupItineraire(line)
	elif regListing.search(line) :
		s=recupListing(line,True)
		if dest==ListFr and section in ListingsSpecialFr.keys() :
			s=s.replace('Listing',ListingsSpecialFr[section])
		result+=s
		bListing=True
	elif regImg.search(line) :
		result+=recupImage(line)
	elif regSection.search(line) :
		s=recupSection(line)
		if len(s)>3 and s[2] !="=" :
			section=s.replace("==","").replace("\n","")
		result+=s
	elif regDans.search(line) :
		s=dest[10].replace("0",TypeArticle.lower()) #avancement
		result+=s
		bAv=True
		result+=recupDans(line)
if (not bAv) : # Si la bannière avancement n'a toujour pas été placé
	s=dest[10].replace("0",TypeArticle.lower())
	result+=s
# On écrit les fichiers
title=title.replace("/","-")
title=title.replace(".","-")
if args.nocomment is True :
	result=re.sub(r'<!--(.*)(.|\n)(.*)-->',r'\2',result)
with open("./"+title+".txt", "w") as fichier:
	fichier.write(result)
if args.debug is True :
	with open("./"+title+"_src.txt", "w") as fichier:
		fichier.writelines(content)
