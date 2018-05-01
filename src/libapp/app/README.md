# ~#PROJECT#~

*~#SHORTDESCRIPTION#~*

* **category**    Application
* **copyright**   ~#CURRENTYEAR#~ ~#OWNER#~
* **license**     see [LICENSE](LICENSE)
* **link**        ~#PROJECTLINK#~


## Description

~#SHORTDESCRIPTION#~


## Requirements

```
sudo pip install json-spec
```

## Quick Start

This project includes a Makefile that allows you to test and build the project in a Linux-compatible system with simple commands.

To see all available options:
```
make help
```

To build a Conda development environment:
```
make conda_dev
. activate
```

To build and test the project inside a Conda environment:  
```
make build
```

The coverage report is available at:  
```env-~#PROJECT#~/conda-bld/coverage/htmlcov/index.html```

To format the code (please use this command before submitting any pull request):
```
make format
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

* **remote_config_provider** : remote configuration source ("url");
* **remote_config_endpoint** : remote configuration URL (e.g. https://raw.githubusercontent.com/~#VENDOR#~/~#PROJECT#~);
* **remote_config_path** : remote configuration path where to search fo the configuration file (e.g. "/master/resources/etc/~#PROJECT#~");
* **remote_config_secret_keyring** : path to the openpgp secret keyring used to decript the remote configuration data (e.g. "token=0123456789ABCDEF");

The equivalent environment variables are:

* ~#UPROJECT#~_REMOTECONFIGPROVIDER
* ~#UPROJECT#~_REMOTECONFIGENDPOINT
* ~#UPROJECT#~_REMOTECONFIGPATH
* ~#UPROJECT#~_REMOTECONFIGSECRETKEYRING


## Examples

Once the application has being compiled with `make build`, it can be quickly tested:

* activate the Conda environment:  
```
. ../env-~#PROJECT#~/bin/activate
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
