# ssh and setup environ
ssh sc2ls@sc2ls.mooo.com /bin/bash << EOF
  echo "Sourcing bash profile"
  source /home/sc2ls/.bash_profile
  echo "Loading virtual env"
  workon future_rank
  echo "Pulling"
  git pull origin master
  echo "Gulping"
  gulp js
  gulp css
  echo "Stopping server"
  ps aux | grep uwsgi | grep utils | grep -v grep | sed 's/\s\+/ /g' | cut -d' ' -f2 | xargs kill -9
  echo "Starting server ..."
  nohup uwsgi --ini utils/wsgi.ini > /var/log/ftr/server/server.out 2>&1 < /dev/null &
EOF