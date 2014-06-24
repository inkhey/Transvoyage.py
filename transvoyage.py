#!/usr/bin/python
# -*- coding: utf-8 -*-
#  transvoyage.py
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
# - Version en python seulement.
# - commentaires et TODO bilingue.
# - optimisations
# -	traduction inversé (regex Français)
# - nouveau langages
# - debugage de certains regex et autres

import sys
import os
import subprocess 
import re

# traductions des types Articles

listTypeFr=('Ville','Région continentale','Région','Pays'   ,'Quartier','Itinéraire','Parc')
listTypeEn=('city' ,'continent'          ,'region','country','district','itinerary' ,'park')

#Equivalences sections
listSectionFr=["Comprendre","Aller" ,"Circuler"  ,"Voir","Faire","Acheter","Manger","Boire un verre / Sortir","Se loger","Aux environs","Travailler","Apprendre","Gérer le Quotidien","Sécurité","Communiquer"]
listSectionEn=["Understand","Get in","Get around","See" ,"Do"   ,"Buy"    ,"Eat"   ,"Drink"                  ,"Sleep"   ,"Go next","Work"           ,"Learn"     ,"Cope"             ,"Stay safe", "Connect"   ]


listSectionFr.extend(["Se préparer","Étapes","Autres destination","Lire","Douanes","En taxi","Santé","Monnaie","Villes","Régions"])
listSectionEn.extend(["Prepare","Route","Other destinations","Read","Customs","By taxi","Stay healthy","Currency","Cities","Regions"])

listSectionFr.extend(['Histoire', 'Paysage', 'Flore et faune',"Climat","Randonnée","Droits d'accès","Activités","Météo","Nature"])
listSectionEn.extend(['History', 'Landscape', 'Flora and fauna',"Climate","Hiking","Fees/permits","Activities","Weather","Wildlife"])

listSectionFr.extend(['À pied', 'En train', 'En bus',"En avion","En ferry","En bateau","En voiture","En Vélo","En Vélo","En Vélo","En motoneige"])
listSectionEn.extend(['By foot', 'By train', 'By bus',"By plane","By ferry","By boat","By car","By bicycle","By cycle","By bike","By snowmobile"])

listSectionFr.extend(['Bon marché', 'Prix moyen','Prix moyen', 'Luxe','Hôtel','Logements','Dans la nature'])
listSectionEn.extend(['Budget', 'Mid-range','Mid range', 'Splurge','Hotel','Lodging','Backcountry'])

# Équivalence image

listImageFr=["[[Fichier:","[[Fichier:","gauche","droite","vignette"]
listImageEn=["[[Image:","[[File:","left","right","thumb"]

#Equivalence Listings

#titre listings
listListingDebFr=["Listing","Faire","Voir","Acheter","Manger","Sortir","Se loger"]
listListingDebEn=["listing","do" ,"see","buy","eat","drink","sleep",]

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
RegSFr=[]
RegSEn=["(.*)\[\[(Image|File):(.*)\s*$", "(=+)(.*)(=+)(.*)","(.*){{(listing|do|see|buy|eat|drink|sleep)(.*)\s*$","}}(.*)","{{IsPartOf\|(.*)}}\s*$"]
#               0                                1                                2                                 3           4 
RegSEn.extend(["^(=+)(.*) to (.*)(=+)\s*$","(.*){{Regionlist(.*)","(.*)region(.*)name=(.*)","{{(outline|usable|guide|stub|star)0}}(.*)"])
#                         5                  6                        7                                 8

#Avancement
avFr="{{Avancement|statut=esquisse|type=0}}\n" 
avEn="{{outlineO}}\n"
# Trousse à mots par langues
ListFr=(listTypeFr,listSectionFr,listImageFr,listListingDebFr,listListingFr,listItineraireFr,listDansFr,listMapDebFr,listMapFr,RegSFr,avFr)
ListEn=(listTypeEn,listSectionEn,listImageEn,listListingDebEn,listListingEn,listItineraireEn,listDansEn,listMapDebEn,listMapEn,RegSEn,avEn)
#           0         1            2               3           4             5                6              7           8         9    10

#Langue source et destination

src=ListEn
dest=ListFr

# Pour récupérér le type de l'article (Ville,Itinéraire,Quartier,etc…)
def recupTypeArticle() :
	typeArticle = "Ville"
	listRegex = list()
	for mot in src[0] :
		s=src[9][8].replace("0",mot)
		listRegex.append(re.compile(s))

	with open("./temp") as f:
		bOk=True
		for line in f:
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
	if numMap > 0 :
		numPrec=str(numMap-1)
		sNumMap=str(numMap)
		for i in range (len(src[8])):
			src[8][i]=src[8][i].replace(numPrec,sNumMap)
			dest[8][i]=dest[8][i].replace(numPrec,sNumMap)
		for i in range (len(src[8])) :
			s=s.replace(src[8][i],dest[8][i])
	return s
	
#Programme en lui même
if len(sys.argv) > 1: # Si on à entrer un nom d'article
	bAv=False # Pour savoir si la bannière d'avancement à été placé
	result="" # Pou stocké le resultat
	title=sys.argv[1]
	subprocess.call(["./get.sh", sys.argv[1]]) # programme shell pour récupérer l'article en wikicode
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
	# On ouvre et on lit
	with open("./temp") as f:
		numMap=-1
		bListing=False;
		for line in f:
			if numMap>-1 :
				if regNomRegion.search(line) :
					numMap=numMap+1
				result+=recupMap(line,numMap)
				if regListingEnd.search(line) :
					numMap=-1
			if bListing :
				result+=recupListing(line,False)
				if regListingEnd.search(line) :
					bListing=False
			elif regMap.search(line) :
				numMap=0
				result+=recupMap(line,numMap)
			elif regItineraire.search(line) :
				result+=recupItineraire(line)
			elif regListing.search(line) :
				result+=recupListing(line,True)
				bListing=True
			elif regImg.search(line) :
				result+=recupImage(line)
			elif regSection.search(line) :
				result+=recupSection(line)
			elif regDans.search(line) :
				s=dest[10].replace("0",TypeArticle.lower()) #avancement
				result+=s
				bAv=True
				result+=recupDans(line)
	if (not bAv) : # Si la bannière avancement n'a toujour pas été placé
		s=dest[10].replace("0",TypeArticle.lower())
		result+=s
	print result
else :
	print "un nom d'article est nécessaire pour que le script fonctionne"
