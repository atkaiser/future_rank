#!/bin/bash

source ~/.virtualenvs/future_rank/bin/activate

cd ~/dev/future_rank/scripts

date

python generate_data.py > ../static/js/data.js

cd ..

export NVM_DIR="/home/akaiser/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm

gulp js
