#!/bin/bash
python3 __main__.py \
    --api_url "http://127.0.0.1:45869/" \
    -H "localhost" -P "45868" \
    -r "my-rules" "default-rules" \
    -k "..." \
    $@ 
