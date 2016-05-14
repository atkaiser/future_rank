#!/bin/bash

TOURNAMENT=Rome
TYPE="Masters 96"

source ~/.virtualenvs/future_rank/bin/activate

cd ~/dev/future_rank/scripts

date

python generate_data.py -n 50 "$TOURNAMENT" "$TYPE" > ../static/js/data.js

cd ..

gulp js
