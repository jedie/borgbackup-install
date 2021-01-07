SHELL := /bin/bash

all: help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9 -]+:.*?## / {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check-poetry:
	@if [[ "$(shell poetry --version 2>/dev/null)" == *"Poetry"* ]] ; \
	then \
		echo "Poetry found, ok." ; \
	else \
		echo 'Please install poetry first, with e.g.:' ; \
		echo 'make install-poetry' ; \
		exit 1 ; \
	fi

install-poetry:  ## install or update poetry
	pip3 install -U pip
	pip3 install -U poetry

apt-get-install:  ## install the dependencies for Debian / Ubuntu
	sudo apt-get install python3 python3-dev python3-pip python3-virtualenv \
	libssl-dev openssl \
	libacl1-dev libacl1 \
	build-essential \
	libfuse-dev fuse pkg-config

install: check-poetry ## install project via poetry
	poetry install
	poetry run python3 link_helper.py

update: check-poetry ## update the sources and installation
	git fetch --all
	git pull origin master
	poetry run pip install -U pip
	poetry update

.PHONY: help check-poetry install-poetry install update