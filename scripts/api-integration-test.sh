#!/bin/bash

### API dev box ###
##docker compose -f ../docker-compose.yml up flask-api --build -d

### DB Container ###
export MYSQL_ROOT_PASSWORD='mysqlroot'
export MY_SQL_CONTAINER_NAME='integration-test-mysql-host'
export ENVIRONMENT='test'

echo "Checking for old containers and volumes..."

if [[ ! -z "`docker compose -f ../test/integration/docker-compose.yml ps -q`" ]]; then
    echo "Cleaning up old containers and volumes..."
    docker compose -f ../test/integration/docker-compose.yml down -v
else 
    echo "None found"
fi 

## Wait for mysql container to be up before running tests
echo "Wait for docker mysql container to be running..."


# build the container. TODO: Remove --build if dont want to rebuild every time
docker compose -f ../test/integration/docker-compose.yml up integration-test-mysql -d 

until [[ "`docker inspect -f {{.State.Health.Status}} $MY_SQL_CONTAINER_NAME`"  == "healthy" ]];
do
    sleep 0.1
done
echo "container is up"

## get the IP of the container as we need it to connect to the mysql service
export CONTAINER_IP=`$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $MY_SQL_CONTAINER_NAME)`

echo "Container IP: $CONTAINER_IP"

# Need to active pyenv environment befor running this script. Also cd out into parent dir so that All our different python packages can access eachother

cd ../

python -m pytest
