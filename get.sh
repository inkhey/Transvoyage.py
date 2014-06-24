#!/bin/bash
# Mini-script to Download live English wikicode
# based on transvoyage code
TITLE=$1
WIKICODE="temp"
wget --quiet -O $WIKICODE "https://en.wikivoyage.org/w/index.php?title=$TITLE&action=raw"
