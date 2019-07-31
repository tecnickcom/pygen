# pygen

*Command-line tool to generate Python services, applications and libraries with reusable logic.*

[![Master Build Status](https://secure.travis-ci.org/tecnickcom/pygen.png?branch=master)](https://travis-ci.org/tecnickcom/pygen?branch=master)
[![Donate via PayPal](https://img.shields.io/badge/donate-paypal-87ceeb.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&currency_code=GBP&business=paypal@tecnick.com&item_name=donation%20for%20pygen%20project)
*Please consider supporting this project by making a donation via [PayPal](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&currency_code=GBP&business=paypal@tecnick.com&item_name=donation%20for%20pygen%20project)*

* **category**    Tool
* **author**      Nicola Asuni <info@tecnick.com>
* **copyright**   2014-2019 Nicola Asuni - Tecnick.com LTD
* **license**     MIT (see [LICENSE](LICENSE))
* **link**        https://github.com/tecnickcom/pygen


## Description

This is a command-line tool to quickly generate Python services, applications and libraries with a common set of features and reusable logic.

For an equivalent project in Go (golang) please check [GoGen](https://github.com/tecnickcom/gogen).

Each Python project built with this tool adheres to the set of conventions detailed in the following articles:

* [Software Naming](https://technick.net/guides/software/software_naming)
* [Software Structure](https://technick.net/guides/software/software_structure)
* [Software Versioning](https://technick.net/guides/software/software_versioning)
* [Software Configuration](https://technick.net/guides/software/software_configuration)
* [Software Logging Format](https://technick.net/guides/software/software_logging_format)
* [Software Metrics](https://technick.net/guides/software/software_metrics)
* [Simple API JSON Response Format](https://technick.net/guides/software/software_json_api_format)
* [Software Automation](https://technick.net/guides/software/software_automation)
* [Build Software with Docker](https://technick.net/guides/software/software_docker_build)

Each generated project is immediately functional and can be fully tested using the ```make build``` command.


## Quick Start

This project includes a Makefile that allows you to test and build the project in a Linux-compatible system with simple commands.  
All the artifacts and reports produced using this Makefile are stored in the *target* folder.  

To see all available options:
```
make help
```


## Usage

```
make new TYPE=app CONFIG=myproject.cfg
```

* **TYPE** is the project type:
    * **lib**     :  library
    * **app**     :  command-line application
    * **srv**     :  HTTP API service
    * **libapp**  :  library + command-line application
    * **libsrv**  :  library + HTTP API service

* **CONFIG** is the configuration file containing the project settings.

To create a new configuration please clone the *default.cfg* file and change the values.

All projects are creted inside the *target* directory.


## Features

### Services (srv)

* Web HTTP RESTful JSON API;
* Standard command line options;
* Multiple configuration options, including remote configuration via URL;
* Logging;
* StatsD client to collect usage metrics;
* Unit tests;
* Makefile;
* Docker build;
* Conda packaging.
* Wheel packaging.

### Applications (app)

* Standard command line options;
* Multiple configuration options, including remote configuration via URL;
* Logging;
* StatsD client to collect usage metrics;
* Unit tests;
* Makefile;
* Docker build;
* Conda packaging.
* Wheel packaging.

### Libraries (lib)

* Unit tests;
* Makefile;
* Docker build;
* Conda packaging.
* Wheel packaging.
