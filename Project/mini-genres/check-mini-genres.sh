#!/bin/sh

bextract -fe -w genre.arff genre.mf -ds 50
kea -w genre.arff -cl GS
#kea -w genre.arff -cl SVM

