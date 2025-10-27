SHELL := /bin/bash
PROJECT_NAME = $(notdir $(PWD))

install:
	python -m venv .venv && \
	source .venv/Scripts/activate &&\
	python -m pip install --upgrade pip setuptools wheel && \
	pip install -r requirements.txt && \
	python -m ipykernel install --user --name "$(notdir $(CURDIR))-venv" --display-name "Python ($(notdir $(CURDIR)))"

