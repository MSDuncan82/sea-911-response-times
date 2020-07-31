.PHONY: clean data requirements sync_data_to_s3 sync_data_from_s3

#################################################################################
# GLOBALS                                                                       #
#################################################################################

# PROJECT_NAME = {{ project name }}
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = # {{ bucket name }}
PROFILE = default
PYTHON_INTERPRETER = python3

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Set up Dev Container
jupyter: requirements
	jupyter lab --port=8888 --no-browser --ip=0.0.0.0 --allow-root

build_requirements:
	bash/make_requirements.sh

term:
	bash/set_dotfiles.sh

aws:
	bash bash/install_aws.sh

## Delete all compiled Python files
clean: black
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".ipynb_checkpoints" | xargs rm -rf

black:
	black src/*

## Upload Data to S3
sync_data_to_s3: aws
ifeq (default,$(PROFILE))
	aws s3 sync data/raw s3://$(BUCKET)/
else
	aws s3 sync data/raw s3://$(BUCKET)/ --profile $(PROFILE)
endif

## Download Data from S3
sync_data_from_s3: aws
ifeq (default,$(PROFILE))
	aws s3 sync s3://$(BUCKET)/ data/raw/
else
	aws s3 sync s3://$(BUCKET)/ data/raw/ --profile $(PROFILE)
endif
