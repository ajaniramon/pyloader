#!/bin/bash
docker rm pyloader
docker build -t pyloader .
docker container run --name pyloader -p 8000:8000 pyloader:latest