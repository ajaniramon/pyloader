#!/bin/bash

export ADMIN_USER=$1
export ADMIN_PASSWORD=$2
uvicorn api:app --reload
