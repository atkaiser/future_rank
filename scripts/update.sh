#!/bin/bash

TOURNAMENT=Rome
TYPE="Masters 96"

# Where this script is stored
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR

python generate_data.py -n 300 "$TOURNAMENT" "$TYPE" > $DIR/../static/js/data.js

cd ..

gulp js