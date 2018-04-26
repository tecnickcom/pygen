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

To format the code (please use this command before submitting any pull request):
```
make format
```

