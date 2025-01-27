PIP = pip3
PYTHON = python3

PYTHON3_OK := $(shell python3 --version 2>&1)
ifeq ('$(PYTHON3_OK)','')
	# not available
	PIP 	= pip
	PYTHON = python
endif

.PHONY: all
all: init build

.PHONY: init
init:
	$(PIP) install -r requirements.txt

.PHONY: build
build:
	$(PYTHON) build.py

.PHONY: clean
clean:
	@rm -f dist/*
	@rm -f README.md