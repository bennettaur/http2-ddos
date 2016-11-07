#!/bin/bash

if [ -z $1 ]; then
    PORT=443
else
    PORT=$1
fi

docker rm -f httpd nginx

docker build -t bennettaur/nginx-http2-exp -f Dockerfile-nginx-http2-ex .
docker run -d -p $PORT:443 --name nginx bennettaur/nginx-http2-exp
