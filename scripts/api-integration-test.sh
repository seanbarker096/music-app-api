#!/bin/bash

### API dev box ###
docker compose -f ../docker-compose.yml up flask-api --build -d

### DB Container ###
export MYSQL_ROOT_PASSWORD='mysqlroot'
export MY_SQL_CONTAINER_NAME='integration-test-mysql-host'
# build the container
docker compose -f ../test/integration/docker-compose.yml up integration-test-mysql --build -d


# # run the sql seed file in the container. -i means our shell commands map to shell in container (attaches stdin)
# docker exec -it $MY_SQL_CONTAINER_NAME /bin/bash -c "mysql -h localhost -u root -p$MYSQL_ROOT_PASSWORD < /usr/src/db/seed.sql"

