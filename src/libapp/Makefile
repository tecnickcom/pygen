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
ALLPACKAGES=$(shell cat lib/conda/meta.yaml app/conda/meta.yaml | grep -oP '^    - \K(.*)' | sort -u | tr '\r\n' ' ')

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
	cp -t app/ VERSION RELEASE LICENSE
	cd lib && make version
	cd app && make version

# Build minimal Conda environment
conda:
	cd lib && make conda
	cd app && make conda

# Build development Conda environment
conda_dev:
	ENV_NAME=env-dev-~#PROJECT#~ ./lib/conda/setup-conda.sh
	. env-dev-~#PROJECT#~/bin/activate && \
	$(foreach PKG,$(ALLPACKAGES), env-dev-~#PROJECT#~/bin/conda install --override-channels $(CONDA_CHANNELS) -y $(PKG) || true ; )

# Build a conda package
build: version
	cd lib && make build
	cd app && make build
	
# Generate source code documentation
doc:
	cd lib && make doc
	cd app && make doc

# Format the source code
format:
	cd lib && make format
	cd app && make format

# Remove any build artifact
clean:
	cd lib && make clean
	cd app && make clean

# Build everything inside a Docker container
dbuild:
	@mkdir -p target
	@rm -rf target/*
	@echo 0 > target/make.exit
	CVSPATH=$(CVSPATH) VENDOR=$(VENDOR) PROJECT=$(PROJECT) MAKETARGET='$(MAKETARGET)' ./dockerbuild.sh
	@exit `cat target/make.exit`
