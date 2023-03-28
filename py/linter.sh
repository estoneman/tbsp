#!/bin/zsh

DICT=../data/words_alpha.txt

for file in `find . -maxdepth 1 -type f -name '*.py'` ; do
    echo "[+] Linting $file"
    pylint --spelling-private-dict $DICT \
           --max-line-length 80 \
           --min-similarity-lines 2 \
           --max-locals 20 \
           --check-quote-consistency y \
           --good-names i,j,k,n,w \
           $file
done
