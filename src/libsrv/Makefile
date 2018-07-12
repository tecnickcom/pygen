# MAKEFILE
#
# @link        ~#PROJECTLINK#~
# ------------------------------------------------------------------------------

# List special make targets that are not associated with files
.PHONY: help version conda conda_dev build doc format clean

# Project name
PROJECT=~#PROJECT#~

# Current directory
CURRENTDIR=$(shell pwd)

# Include configuration
include $(CURRENTDIR)/config.mk

# extract all packages
ALLPACKAGES=$(shell cat lib/conda/meta.yaml srv/conda/meta.yaml | grep -oP '^\s*-\s\K(.*)' | sed "s/.*${PROJECT}//" | sed '/^\s*$$/d' | sort -u | tr -d ' ' | sed 's/[^ ][^ ]*/"&"/g' | tr '\r\n' ' ')

# --- MAKE TARGETS ---

# Display general help about this command
help:
	@echo ""
	@echo "$(PROJECT) Makefile."
	@echo "The following commands are available:"
	@echo ""
	@echo "    make version    : Set version from VERSION file"
	@echo "    make conda      : Build minimal Conda environment"
	@echo "    make conda_dev  : Build development Conda environment"
	@echo "    make build      : Build a Conda package"
	@echo "    make doc        : Start a server to display source code documentation"
	@echo "    make format     : Format the source code"
	@echo "    make clean      : Remove any build artifact"
	@echo "    make dbuild     : Build everything inside a Docker container"
	@echo ""

all: help

# Set the version from VERSION file
version:
	cp -t lib/ VERSION RELEASE LICENSE
	cp -t srv/ VERSION RELEASE LICENSE
	cd lib && make version
	cd srv && make version

# Build minimal Conda environment
conda:
	cd lib && make conda
	cd srv && make conda

# Build development Conda environment
conda_dev:
	ENV_NAME=env-dev-~#PROJECT#~ ./lib/conda/setup-conda.sh
	. env-dev-~#PROJECT#~/bin/activate && \
	env-dev-~#PROJECT#~/bin/conda install --override-channels $(CONDA_CHANNELS) -y $(ALLPACKAGES)

# Build a conda package
build: version
	cd lib && make build
	cd srv && make build
	
# Generate source code documentation
doc:
	cd lib && make doc
	cd srv && make doc

# Format the source code
format:
	cd lib && make format
	cd srv && make format

# Remove any build artifact
clean:
	cd lib && make clean
	cd srv && make clean

# Build everything inside a Docker container
dbuild:
	@mkdir -p target
	@rm -rf target/*
	@echo 0 > target/make.exit
	CVSPATH=$(CVSPATH) VENDOR=$(VENDOR) PROJECT=$(PROJECT) MAKETARGET='$(MAKETARGET)' ./dockerbuild.sh
	@exit `cat target/make.exit`
