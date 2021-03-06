# MAKEFILE
#
# @link        ~#PROJECTLINK#~
# ------------------------------------------------------------------------------

# Use bash as shell (Note: Ubuntu now uses dash which doesn't support PIPESTATUS).
SHELL=/bin/bash

# CVS path (path to the parent dir containing the project)
CVSPATH=~#CVSPATH#~

# Project owner
OWNER=~#OWNER#~

# Project vendor
VENDOR=~#VENDOR#~

# Project name
PROJECT=~#PROJECT#~

# Project version
VERSION=$(shell cat VERSION)

# Project release number (packaging build number)
RELEASE=$(shell cat RELEASE)

# Name of RPM or DEB package
PKGNAME=${VENDOR}-${PROJECT}

# Current directory
CURRENTDIR=$(dir $(realpath $(firstword $(MAKEFILE_LIST))))

# Conda environment
CONDA_ENV=$(shell dirname ${CURRENTDIR})/env-${PROJECT}

# Include default build configuration
include $(CURRENTDIR)/config.mk

# extract all packages
ALLPACKAGES=$(shell cat conda/meta.yaml | grep -oP '^\s*-\s\K(.*)' | sed "s/.*${PROJECT}//" | sed '/^\s*$$/d' | sort -u | tr -d ' ' | sed 's/[^ ][^ ]*/"&"/g' | tr '\r\n' ' ')


# --- MAKE TARGETS ---

# Display general help about this command
.PHONY: help
help:
	@echo ""
	@echo "$(PROJECT) Makefile."
	@echo "The following commands are available:"
	@echo ""
	@echo "    make version    : Set version from VERSION file"
	@echo "    make conda      : Build minimal Conda environment"
	@echo "    make conda_dev  : Build development Conda environment"
	@echo "    make build      : Build a Conda package"
	@echo "    make wheel      : Build a Wheel package"
	@echo "    make dbuild     : Build everything inside a Docker container"
	@echo "    make test       : Execute test command - you shuould activate the conda_dev environment first"
	@echo "    make lint       : Evaluate code"
	@echo "    make doc        : Start a server to display source code documentation"
	@echo "    make format     : Format the source code"
	@echo "    make clean      : Remove any build artifact"
	@echo ""

all: help

# Set the version from VERSION file
.PHONY: version
version:
	sed -i "s/version:.*$$/version: $(VERSION)/" conda/meta.yaml
	sed -i "s/number:.*$$/number: $(RELEASE)/" conda/meta.yaml
	sed -i "s/__version__.*$$/__version__ = \"$(VERSION)\"/" ~#PROJECT#~/__init__.py
	sed -i "s/__release__.*$$/__release__ = \"$(RELEASE)\"/" ~#PROJECT#~/__init__.py

# Build minimal Conda environment
.PHONY: conda
conda:
	./conda/setup-conda.sh

# Build development Conda environment
.PHONY: conda_dev
conda_dev:
	ENV_NAME=env-dev-~#PROJECT#~ ./conda/setup-conda.sh
	. ../env-dev-~#PROJECT#~/bin/activate && \
	../env-dev-~#PROJECT#~/bin/conda install --override-channels $(CONDA_CHANNELS) -y $(ALLPACKAGES)

# Build a conda package
.PHONY: build
build: clean version conda
	mkdir -p target
	PROJECT_ROOT=${CURRENTDIR} "${CONDA_ENV}/bin/conda" build --prefix-length 128 --no-anaconda-upload --override-channels $(CONDA_CHANNELS) conda

# Build a Wheel package
.PHONY: wheel
wheel: clean version
	python setup.py sdist bdist_wheel

# Test using setuptools
.PHONY: test
test:
	python setup.py develop test

# Evaluate code
.PHONY: lint
lint:
	pylint ${PROJECT}

# Generate source code documentation
.PHONY: doc
doc:
	pydoc -p 1234 $(PROJECT)

# Format the source code
.PHONY: format
format:
	black .

# Remove any build artifact
.PHONY: clean
clean:
	rm -rf target Dockerfile htmlcov build dist .cache .benchmarks ./tests/*.so ./tests/__pycache__ ./~#PROJECT#~/__pycache__ ./~#PROJECT#~.egg-info
	find . -type f -name '*.pyc' -exec rm -f {} \;

# Build everything inside a Docker container
.PHONY: dbuild
dbuild:
	@mkdir -p target
	@rm -rf target/*
	@echo 0 > target/make.exit
	CVSPATH=$(CVSPATH) VENDOR=$(VENDOR) PROJECT=$(PROJECT) MAKETARGET='$(MAKETARGET)' ./dockerbuild.sh
	@exit `cat target/make.exit`
