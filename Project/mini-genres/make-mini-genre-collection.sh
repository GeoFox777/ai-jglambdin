#!/bin/sh
rm -f *.mf

for d in *
do
  if [ -d $d ]
  then
    mkcollection -l $d -c $d $d/
  fi
done

cat *.mf >> genre.mf



