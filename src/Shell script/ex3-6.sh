#!/bin/bash

if [ -d "$1" ]
then
   exit 0
else
   mkdir "$1"
   cd "$1"
   i=0
   while [ $i -lt 5 ]
   do
       touch "file$i.txt"
       i=$((i + 1))
   done

   tar cf "$1.tar" file0.txt file1.txt file2.txt file3.txt file4.txt

   mkdir "$1"
   
   mv "$1.tar" "$1"
   cd "$1"
   tar xf "$1.tar" > /dev/null  

   echo $(ls)

   cd ../..
   ls "$1"/*.txt | xargs -n 1 basename
fi

exit 0

