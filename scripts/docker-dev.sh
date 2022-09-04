#!/bin/bash

export ENV_FILE=".env.dev"


# Need to run in detached mode otherwise the container will not be left running and wont appear with docker ps
docker compose up --detach --build flask-api 

