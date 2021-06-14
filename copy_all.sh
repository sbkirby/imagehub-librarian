#!/usr/bin/env bash
path_src=.
path_dst=~/IOTstack
date=$(date +"%m%d%y")
for file_src in $path_src/*; do
  file_dst="$path_dst/$(basename $file_src | \
    sed "s/^\(.*\)\.\(.*\)/\1.\2/")"
  if [[ "$file_src" != ".git"* ]];then
    mv "$file_src" "$file_dst"
  fi
done
