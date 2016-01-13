# ssh and setup environ
ssh sc2ls@sc2ls.mooo.com /bin/bash << EOF
  source /home/sc2ls/.bash_profile
  workon future_rank
  git pull origin master
  ps aux | grep uwsgi | grep utils | grep -v grep | sed 's/\s\+/ /g' | cut -d' ' -f2 | xargs kill -9
  echo "Starting server ..."
  nohup uwsgi --ini utils/wsgi.ini > /var/log/ftr/server/server.out 2>&1 < /dev/null &
EOF