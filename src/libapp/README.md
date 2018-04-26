# ~#PROJECT#~

*~#SHORTDESCRIPTION#~*

* **category**    Application + Library
* **copyright**   ~#CURRENTYEAR#~ ~#OWNER#~
* **license**     see [LICENSE](LICENSE)
* **link**        ~#PROJECTLINK#~


## Description

~#SHORTDESCRIPTION#~

This project builds one library and one application package.

For further information about the package and the library,
please read the README.md files inside the `app` and `lib` folders.


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
resources/Docker/Dockerfile.dev
```

To format the code (please use this command before submitting any pull request):
```
make format
```
