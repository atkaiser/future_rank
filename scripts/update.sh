#!/bin/bash

source ~/.virtualenvs/future_rank/bin/activate

cd ~/dev/future_rank/scripts

date

python generate_data.py > ../static/js/data.js

cd ..

gulp js
