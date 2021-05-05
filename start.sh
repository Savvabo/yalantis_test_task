#!/bin/bash
app="yalantis"
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
rm pythonsqlite.db
rm api.log
rm tests.log

docker rm $(docker stop $(docker ps -a -q --filter ancestor=${app} --format="{{.ID}}"))
docker image rm ${app}
docker build -t ${app} .
docker run -d \
  --name=${app} \
  --network=host\
  -v $PWD:/app ${app}