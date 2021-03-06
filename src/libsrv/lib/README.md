# ~#PROJECT#~

*~#SHORTDESCRIPTION#~*

* **category**    Library
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

To test inside a `conda_dev` environment using setuptools:  
```
make test
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

