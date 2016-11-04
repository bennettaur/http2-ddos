#!/bin/bash

bash /home/mbennett/http2-ddos/docker_rm_all.sh

docker build -t bennettaur/httpd-http2-exp -f Dockerfile-httpd-http2-ex .
docker run -d --net=host --name httpd bennettaur/httpd-http2-exp
