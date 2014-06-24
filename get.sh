#!/bin/bash
# Mini-script to Download live English wikicode
# based on transvoyage code

WIKICODE="temp"
wget --quiet -O $WIKICODE "https://en.wikivoyage.org/w/index.php?title=$TITLE&action=raw"
