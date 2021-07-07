#!/bin/bash
mkdir -p my-rules
python3 __main__.py \
    -r "my-rules" "default-rules" \
    -k "..." \  # paste your key between those quotes
    $@ \
&& firefox lint_results.html
