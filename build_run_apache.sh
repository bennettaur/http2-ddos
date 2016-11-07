#!/bin/bash

if [ -z $1 ]; then
    PORT=443
else
    PORT=$1
fi

docker rm -f nginx httpd

docker build -t bennettaur/httpd-http2-exp -f Dockerfile-httpd-http2-ex .
docker run -d -p $PORT:443 --name httpd bennettaur/httpd-http2-exp
