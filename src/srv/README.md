# ~#PROJECT#~

*Brief project description ...*

* **category**    Service
* **copyright**   ~#CURRENTYEAR#~ ~#OWNER#~
* **license**     see [LICENSE](LICENSE)
* **link**        ~#PROJECTLINK#~


## Description

Full project description ...


## Requirements

```
sudo pip install json-spec
```

## Quick Start

This project includes a Makefile that allows you to test and build the project in a Linux-compatible system with simple commands.

All the artifacts and reports produced using this Makefile are stored in the *target* folder.

To see all available options:
```
make help
```

To build and test the project inside a Conda environment:  
```
make build
```

The coverage report is available at:  
```env-~#PROJECT#~/conda-bld/coverage/htmlcov/index.html```

To build the project inside a Docker container (requires Docker):
```
make dbuild
```

An arbitrary make target can be executed inside a Docker container by specifying the "MAKETARGET" parameter:
```
MAKETARGET='build' make dbuild
```
The list of make targets can be obtained by typing ```make```


The base Docker building environment is defined in the following Dockerfile:
```
resources/DockerDev/Dockerfile
```

To format the code (please use this command before submitting any pull request):
```
make format
```

## Useful Docker commands

To manually create the container you can execute:
```
docker build --tag="~#VENDOR#~/~#PROJECT#~dev" .
```

To log into the newly created container:
```
docker run -t -i ~#VENDOR#~/~#PROJECT#~dev /bin/bash
```

To get the container ID:
```
CONTAINER_ID=`docker ps -a | grep ~#VENDOR#~/~#PROJECT#~dev | cut -c1-12`
```

To delete the newly created docker container:
```
docker rm -f $CONTAINER_ID
```

To delete the docker image:
```
docker rmi -f ~#VENDOR#~/~#PROJECT#~dev
```

To delete all containers
```
docker rm $(docker ps -a -q)
```

To delete all images
```
docker rmi $(docker images -q)
```


## Usage

```bash
~#PROJECT#~

Usage:
  ~#PROJECT#~ [--config-dir=<config-dir>] [--log-level=<log-level>]
  ~#PROJECT#~ -h | --help
  ~#PROJECT#~ -v | --version

Options:
  -c --config-dir=<config-dir>  Configuration directory to be added on top of the search list
  -l --log-level=<log-level>    Log level: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
  -h --help                     Show this screen.
  -v --version                  Show version.

Examples:
  ~#PROJECT#~ -c /home/user/config

Note:
  ~#SHORTDESCRIPTION#~
```

## Configuration

If no command-line parameters are specified, then the ones in the configuration file (**config.json**) will be used.
The configuration files can be stored in the current directory or in any of the following (in order of precedence):
* ./
* config/
* ~/~#PROJECT#~/
* /etc/~#PROJECT#~/

This program also support loading the configuration from an URL.
The remote configuration location can be defined either in the local configuration file using the following parameters, or with environment variables:

* **remoteConfigProvider** : remote configuration source ("url");
* **remoteConfigEndpoint** : remote configuration URL (e.g. https://raw.githubusercontent.com/~#VENDOR#~/~#PROJECT#~);
* **remoteConfigPath** : remote configuration path where to search fo the configuration file (e.g. "/master/resources/etc/~#PROJECT#~");
* **remoteConfigSecretKeyring** : path to the openpgp secret keyring used to decript the remote configuration data (e.g. "token=0123456789ABCDEF");

The equivalent environment variables are:

* ~#UPROJECT#~_REMOTECONFIGPROVIDER
* ~#UPROJECT#~_REMOTECONFIGENDPOINT
* ~#UPROJECT#~_REMOTECONFIGPATH
* ~#UPROJECT#~_REMOTECONFIGSECRETKEYRING


## Examples

Once the application has being compiled with `make build`, it can be quickly tested:

* activate the Conda environment:  
```
source ../env-~#PROJECT#~/bin/activate
```
* install the runtime dependencies listed in conda/meta.yaml, for example:  
```
conda install python docopt python-json-logger structlog statsd ujson requests werkzeug -c conda-forge -c https://repo.continuum.io/pkgs/main -c https://repo.continuum.io/pkgs/free
```
* start the program  
```
python -m ~#PROJECT#~ --config-dir=...
```

## Logs

This program logs the log messages in JSON format is StdErr and SysLog.

## Metrics

This programs sends metrics to the configured StatsD server.
