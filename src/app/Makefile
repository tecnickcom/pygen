# MAKEFILE
#
# @link        https://github.com/~#VENDOR#~/~#PROJECT#~
# ------------------------------------------------------------------------------

# List special make targets that are not associated with files
.PHONY: help version conda build doc format clean

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
CURRENTDIR=$(shell pwd)

# Conda environment
CONDA_ENV=$(shell dirname ${CURRENTDIR})/env-${PROJECT}

# Include default build configuration
include $(CURRENTDIR)/config.mk


# --- MAKE TARGETS ---

# Display general help about this command
help:
	@echo ""
	@echo "$(PROJECT) Makefile."
	@echo "The following commands are available:"
	@echo ""
	@echo "    make version    : Set version from VERSION file"
	@echo "    make conda      : Build minimal Conda environment"
	@echo "    make build      : Build a Conda package"
	@echo "    make doc        : Start a server to display source code documentation"
	@echo "    make format     : Format the source code"
	@echo "    make clean      : Remove any build artifact"
	@echo "    make dbuild     : Build everything inside a Docker container"
	@echo ""

all: help

# Set the version from VERSION file
version:
	sed -i "s/version:.*$$/version: $(VERSION).$(RELEASE)/" conda/meta.yaml
	sed -i "s/__version__.*$$/__version__ = '$(VERSION)'/" ~#PROJECT#~/__init__.py
	sed -i "s/__release__.*$$/__release__ = '$(RELEASE)'/" ~#PROJECT#~/__init__.py

# Build minimal Conda environment
conda:
	./conda/setup-conda.sh

# Build a conda package
build: clean version conda
	mkdir -p target
	"${CONDA_ENV}/bin/conda" build --prefix-length 128 --no-anaconda-upload --no-remove-work-dir --override-channels $(ARTIFACTORY_CONDA_CHANNELS) conda
	cp -Rf "${CONDA_ENV}/conda-bld" target/

# Generate source code documentation
doc:
	pydoc -p 1234 $(PROJECT)

# Format the source code
format:
	find . -type f -name '*.py' -exec autopep8 --in-place --max-line-length=255 {} \;

# Remove any build artifact
clean:
	rm -rf target Dockerfile htmlcov build dist .cache .benchmarks ./tests/*.so ./tests/__pycache__ ./~#PROJECT#~/__pycache__ ./~#PROJECT#~.egg-info
	find . -type f -name '*.pyc' -exec rm -f {} \;

# Build everything inside a Docker container
dbuild:
	@mkdir -p target
	@rm -rf target/*
	@echo 0 > target/make.exit
	CVSPATH=$(CVSPATH) VENDOR=$(VENDOR) PROJECT=$(PROJECT) MAKETARGET='$(MAKETARGET)' ./dockerbuild.sh
	@exit `cat target/make.exit`
