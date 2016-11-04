#!/bin/bash

bash /home/mbennett/http2-ddos/docker_rm_all.sh

docker build -t bennettaur/nginx-http2-exp -f Dockerfile-nginx-http2-ex .
docker run -d --net=host --name nginx bennettaur/nginx-http2-exp
