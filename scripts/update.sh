#!/bin/bash

TOURNAMENT=Halle
TYPE="ATP 500"

source ~/.virtualenvs/future_rank/bin/activate

cd ~/dev/future_rank/scripts

date

python generate_data.py -n 300 "$TOURNAMENT" "$TYPE" > ../static/js/data.js

cd ..

gulp js
