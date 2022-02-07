#!/bin/bash

export ADMIN_USER=$1
export ADMIN_PASSWORD=$2
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_PASSWORD=admin
uvicorn api:app --reload
