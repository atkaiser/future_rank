git add -p
git commit
git push origin master

# ssh and setup environ
ssh akaiser@akaiser0.mooo.com /bin/bash << EOF
  echo "Sourcing bash profile"
  source /home/akaiser/.bashrc
  echo "Loading virtual env"
  workon future_rank
  echo "Pulling"
  git pull origin master
  echo "Gulping"
  gulp js
  gulp css
EOF