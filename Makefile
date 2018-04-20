# MAKEFILE
#
# @author      Nicola Asuni <info@tecnick.com>
# @link        https://github.com/tecnickcom/pygen
#
# This file is intended to be executed in a Linux-compatible system.
# ------------------------------------------------------------------------------

# List special make targets that are not associated with files
.PHONY: help all new newproject rename template confirm clean

# Current directory
CURRENTDIR=$(shell pwd)

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


# --- MAKE TARGETS ---

# Display general help about this command
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
	@echo ""
	@echo "    * CONFIG is the configuration file containing the project settings."
	@echo ""

# Alias for help target
all: help

# Generate a new project
new: newproject rename template confirm

# Copy the project template in the output folder
newproject:
	@mkdir -p ./target/$(CVSPATH)/$(PROJECT)
	@rm -rf ./target/$(CVSPATH)/$(PROJECT)/*
	@cp -rf ./src/$(TYPE)/. ./target/$(CVSPATH)/$(PROJECT)/

# Rename project files
rename:
	find ./target/$(CVSPATH)/$(PROJECT)/ -type d -name "_PROJECT_*" -execdir mv '{}' "$(PROJECT)" \; -prune

# Replace text templates in the code
template:
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#PROJECT#~/$(PROJECT)/" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#PROJECT#~/$(PROJECT)/" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#UPROJECT#~/$(UPROJECT)/" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#SHORTDESCRIPTION#~/$(SHORTDESCRIPTION)/" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s|~#CVSPATH#~|$(CVSPATH)|" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s|~#PROJECTLINK#~|$(PROJECTLINK)|" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#VENDOR#~/$(VENDOR)/" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#OWNER#~/$(OWNER)/" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#OWNEREMAIL#~/$(OWNEREMAIL)/" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#CURRENTYEAR#~/$(CURRENTYEAR)/" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#LIBPACKAGE#~/$(LIBPACKAGE)/" {} \;
	@find ./target/$(CVSPATH)/$(PROJECT)/ -type f -exec sed -i "s/~#LICENSE#~/$(LICENSE)/" {} \;

# Print confirmation message
confirm:
	@echo "A new "$(TYPE)" project has been created: "target/$(CVSPATH)/$(PROJECT)

# Remove all generated projects
clean:
	@rm -rf ./target
