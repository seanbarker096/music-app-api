#!/bin/bash

export ENV_FILE=".env.dev"

docker compose up --build flask-api
