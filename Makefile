PIP 	= pip3
PYTHON = python3

PYTHON3_OK := $(shell python3 --version 2>&1)
ifeq ('$(PYTHON3_OK)','')
	# not available
	PIP 	= pip
	PYTHON = python
endif

.PHONY: all
all: init build

init:
	$(PIP) install -r requirements.txt

build:
	$(PYTHON) build.py
