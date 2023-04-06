#!/bin/zsh

DICT="../data/words_alpha.txt"

MAX_LINE_LENGTH=80
MIN_SIMILAR_LINES=1
MAX_ARGS=6
MAX_LOCALS=20
GOOD_NAMES="i,j,k,n,w,x,Type,get_Type"
PKG_ALLOW_LIST="edit_distance"

if [[ ! -f $DICT ]] ; then
    echo "$DICT does not exist. Aborting."
    exit 1
fi

if ! command -v pylint &>/dev/null ; then
    echo "pylint is not installed. Aborting"
    exit 1
fi

for file in $(find . -maxdepth 1 -type f -name '*.py') ; do
    echo "[+] Linting $file"
    pylint --spelling-private-dict "$DICT" \
           --max-line-length "$MAX_LINE_LENGTH" \
           --min-similarity-lines "$MIN_SIMILAR_LINES" \
           --max-args "$MAX_ARGS" \
           --max-locals "$MAX_LOCALS" \
           --check-quote-consistency y \
           --good-names "$GOOD_NAMES" \
           --extension-pkg-allow-list "$PKG_ALLOW_LIST" \
           $file
done
