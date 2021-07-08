#!/bin/bash
mkdir -p my-rules
python3 __main__.py \
    -r "my-rules" "default-rules" \
    -k "..." \ # Paste your access key between those quotes
    $@ 
