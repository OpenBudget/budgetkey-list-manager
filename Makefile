.PHONY: all install list test version


PACKAGE := $(shell grep '^PACKAGE =' setup.py | cut -d "'" -f2)
VERSION := $(shell head -n 1 $(PACKAGE)/VERSION)


all: list

install:
	pip install --upgrade -e .[develop]
	
list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

test:
	pylama budgetkey_list_manager
	tox
	tests/e2e/start_test_environment.sh & 
	sleep 3 
	tests/e2e/test.sh

version:
	@echo $(VERSION)
