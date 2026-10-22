#!/usr/bin/env bash
set -euo pipefail

mkdir -p tn/assets/images
shopt -s nullglob

for file in assets/images/*.{jpg,jpeg,png}; do
  base="$(basename "$file")"
  out="tn/assets/images/$base"
  if [[ ! -f "$out" ]]; then
    convert "$file" -thumbnail 160x160^ -gravity center -extent 160x160 "$out"
  fi
done



