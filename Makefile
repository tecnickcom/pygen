# MAKEFILE
#
# @author      Nicola Asuni <info@tecnick.com>
# @link        https://github.com/tecnickcom/pygen
#
# This file is intended to be executed in a Linux-compatible system.
# ------------------------------------------------------------------------------

# Current directory
CURRENTDIR=$(dir $(realpath $(firstword $(MAKEFILE_LIST))))

# Set default project type
ifeq ($(TYPE),)
	TYPE=app
endif

# Set default project configuration file
ifeq ($(CONFIG),)
	CONFIG=default.cfg
endif

# Include the configuration file
include $(CONFIG)

# Generate a prefix for environmental variables
UPROJECT=$(shell echo $(PROJECT) | tr a-z A-Z | tr - _)

# Base project name
BASEPROJECT=${PROJECT}


# --- MAKE TARGETS ---

# Display general help about this command
.PHONY: help
help:
	@echo ""
	@echo "PyGen Makefile."
	@echo "The following commands are available:"
	@echo ""
	@echo "    make new TYPE=app CONFIG=myproject.cfg  :  Generate a new project"
	@echo "    make clean                              :  Remove all generated projects"
	@echo ""
	@echo "    * TYPE is the project type:"
	@echo "        lib      : library"
	@echo "        app      : command-line application"
	@echo "        srv      : HTTP API service"
	@echo "        libapp   : command-line application with dependency library"
	@echo "        libsrv   : HTTP API service with dependency library"
	@echo ""
	@echo "    * CONFIG is the configuration file containing the project settings."
	@echo ""

# Alias for help target
all: help

# Generate a new project
.PHONY: new
new: newproject rename template confirm

# Copy the project template in the output folder
.PHONY: newproject
newproject:
	@mkdir -p ./target/$(CVSPATH)/$(PROJECT)
	@rm -rf ./target/$(CVSPATH)/$(PROJECT)/*
	@cp -rf ./src/$(TYPE)/. ./target/$(CVSPATH)/$(PROJECT)/

# Rename project files
.PHONY: rename
rename:
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type d -name "lib__PROJECT_*" -execdir mv '{}' "lib_$(PROJECT)" \; -prune
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type d -name "app__PROJECT_*" -execdir mv '{}' "app_$(PROJECT)" \; -prune
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type d -name "srv__PROJECT_*" -execdir mv '{}' "srv_$(PROJECT)" \; -prune
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type d -name "_PROJECT_*" -execdir mv '{}' "$(PROJECT)" \; -prune

# Replace text templates in the code
.PHONY: template
template:
	@find ./target/$(CVSPATH)/$(PROJECT)/lib/ -type f -exec sed -i "s/~#PROJECT#~/lib_~#PROJECT#~/g" {} \; 2>/dev/null || true
	@find ./target/$(CVSPATH)/$(PROJECT)/app/ -type f -exec sed -i "s/~#PROJECT#~/app_~#PROJECT#~/g" {} \; 2>/dev/null || true
	@find ./target/$(CVSPATH)/$(PROJECT)/srv/ -type f -exec sed -i "s/~#PROJECT#~/srv_~#PROJECT#~/g" {} \; 2>/dev/null || true
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#PROJECT#~/$(PROJECT)/g" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#BASEPROJECT#~/$(BASEPROJECT)/g" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#UPROJECT#~/$(UPROJECT)/g" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#SHORTDESCRIPTION#~/$(SHORTDESCRIPTION)/g" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s|~#CVSPATH#~|$(CVSPATH)|g" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s|~#PROJECTLINK#~|$(PROJECTLINK)|g" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#VENDOR#~/$(VENDOR)/g" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#OWNER#~/$(OWNER)/g" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#OWNEREMAIL#~/$(OWNEREMAIL)/g" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#CURRENTYEAR#~/$(CURRENTYEAR)/g" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#LIBPACKAGE#~/$(LIBPACKAGE)/g" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#LICENSE#~/$(LICENSE)/g" {} \;

# Print confirmation message
.PHONY: confirm
confirm:
	@echo "A new "$(TYPE)" project has been created: "target/$(CVSPATH)/$(PROJECT)

# Remove all generated projects
.PHONY: clean
clean:
	@rm -rf ./target

# Test all templates
.PHONY: test
test:
	make clean new TYPE=srv
	cd target/github.com/dummyvendor/dummy && make build
	make clean new TYPE=app
	cd target/github.com/dummyvendor/dummy && make build
	make clean new TYPE=lib
	cd target/github.com/dummyvendor/dummy && make build
	make clean new TYPE=libapp
	cd target/github.com/dummyvendor/dummy && make build
	make clean new TYPE=libsrv
	cd target/github.com/dummyvendor/dummy && make build
