HTTP/2 Lab
==========

## Getting Things Setup

### Requirements

* Docker - Check their site to see how to install for your platform
* Python - Either 2.7.10+ (maybe 3.x but I haven't tested)
* pip - Package manager for python. Installing this is well documented so it's not included here
* OpenSSL 1.0.2 or higher (Or another SSL library that supports ALPN)

If you're running OS X you can run
```
brew install openssl
brew install python
```
to install openssl and compile and install a version of python against that OpenSSL

If you're on a Linux, and you don't have the appropriate versions installed you'll have to either update them, or install them in an alt location.
** NOTE ** If your OpenSSL is out of date, but your python version is fine, you WILL have to recompile python against the newer OpenSSL. Check here for more info: http://stackoverflow.com/a/20740964/6338767

### Building Almost Everything!

First you need to build the base images for Apache httpd an nginx. These will download, compile and install everything Apache httpd and nginx need in order to run with HTTP/2 support

To build the images simply run the following in the root of the project:

```
docker build -t bennettaur/httpd-http2 -f Dockerfile-httpd-http2 .
docker build -t bennettaur/nginx-http2 -f Dockerfile-nginx-http2 .
```

I'll try to keep the latest images built on docker hub (I'm having issues with the automated builds) but you should be able to pull the images directly from docker hub if you don't want to wait for the builds:

```
docker pull bennettaur/httpd-http2
docker pull bennettaur/nginx-http2
```


You should now have all the base images required to start working in the lab

### Test Site

As of right now, I haven't included a site in this repo, as I want to have a more generic and simple site for testing.
To get the lab working, you can copy a static site into the folder content/website1 and the Dockerfile builds will automatically copy it into the Docker images

Alternatively, you can run the create_static_site.sh script from the ./content folder to clone a site into the appropriate folder (make sure your current working directory is ./content)

You just need to pass it in the full URL to the site you want to test. ex:
```
./create_static_site.sh "https://www.google.ca/"
```

### Building the Final Images

Finally, you need to build the final images that will load the content for the servers to server. To build them you simply need to run
```
docker build -t bennettaur/httpd-http2-exp -f Dockerfile-httpd-http2-ex .
docker build -t bennettaur/nginx-http2-exp -f Dockerfile-nginx-http2-ex .
```

If you wish to name the images differently, then you are free to do so, however you should be comfortable running with running Docker containers when doing so

Alternatively, I've made some convenient scripts to build and run the docker containers for you. These are named `build_run_apache.sh` and `build_run_nginx.sh`. These scripts will start a Docker container to port 443 by default but take an optional argument to start it on an alternative port like so:
```
build_run_apache.sh 8443
```
Additionally, if you're not familiar with docker, be sure to run `docker_rm_all.sh` but **\*\*Note\*\*** this will remove all running containers.
Be sure to check out what the scripts are doing to get a better understanding of what's going on.

### Server Push!

To get Server Push working, you need to populate the configs/apache2/httpd-http2-push.conf file with the entries that should be pushed and for what location. The current file has an example that was used during my demo at Hackfest 2016.
You can manually modify it for use with the site you cloned or alternatively you can use find to generate a line separated list of static asset paths and use the include convert_manifest.py script to generate the apache file for you.
Run the find command from the root of you website. For my example site, all the static assets were located in the "assets" folder:
```
cd content/website1
find assets -type f > all_assets.txt
cd ../../
python convert_manifest.py ../../all_assets.txt

```

You can also use the google chrome http2_push_manifest to generate an "ideal" list of assets to use for Server Push
Assuming you have Node and NPM installed you can install the tool simply by running `npm install` in the root of the project, then generate and convert the manifest file by passing it the HTML file you want it to generate assets for:
```
./node_modules/http2-push-manifest/bin/http2-push-manifest -f content/website1/index.html
python convert_manifest.py push_manifest.json
```

**NOTE** be sure to rebuild the apache image everytime you update the Server Push config (or any config).

### Final Stretch! Install Python dependencies

As long as you have pip installed this should be pretty easy. I highly recommend using virtualenv and virtualenvwrapper
```
sudo pip install virtualenvwrapper
mkvirtualenv http2
pip install -r http2_client/dependencies.txt
```

## Play Time!

So now that you should have a running HTTP/2 server for you to test against. You can verify using a browser (chrome has an extension! https://chrome.google.com/webstore/detail/http2-and-spdy-indicator/mpbpobfflnpcgagjijhmgnchggcjblin)
You may need to also modify your browsers network tools to display the protocol being used.

Next you can simply run the python scripts in http2_client

`http2_client/http2_server_push_tests.py` Will show you the difference in the size of responses in HTTP/1.1, HTTP/2 No push, and HTTP/2 with push
Run it with python and passing in the IP and port number
```
python http2_client/http2_server_push_tests.py 127.0.0.1 443
```

`http2_client/http2_req_limit_tests.py` Will loop through a list of assets and request each one. It has a number of different options for running and supports both HTTP/1.1 and HTTP/2 to allow comparisons.
Run `python http2_req_limit_tests.py -h` to see all the options. An example command to run it looks like:
```
python http2_req_limit_tests.py -r 100 -c 10 -t localhost -p 443 -f ./assets.txt -v 2 -l
```
Which will cause it to attempt to make 100 requests per second, with at most 10 concurrent requests per worker, targeting localhost on port 443 and using the line-separated assets in assets.txt and using the HTTP/2 protocol. Verbose logging is disabled.


## Local Python Alternative

If your OS doesn't have a new enough OpenSSL, you'll need to compile and install it yourself, and then recompile Python against that new version. This can be a huge PITA and can be broken on some cloud VMs
Because of this, I've also included a Dockerfile for building and running a usable python with the HTTP/2 tools.

Build it:
```
docker build -t bennettaur/python-http2 -f Dockerfile-python .
```

Then run it to get a bash shell:
```
docker run -ti --link httpd:httpd bennettaur/python-http2
```

**Note** that the "--link" options needs to be passed the name of the HTTP/2 container you are running. For the configs in this project, apache httpd this will be `--link httpd:httpd` and for nginx will be `--link nginx:nginx`

## Other Notes

There is also a `monitor.sh` script which will run nload and display docker running stats using tmux and split panes. You can use this on your OS to see how much CPU and network traffic is being generated by your server and client. You will need to ensure nload and tmux are installed on your system for it to work.