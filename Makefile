SHELL := /bin/bash
PROJECT_NAME = $(notdir $(PWD))

install:
	python -m venv .venv && \
	source .venv/Scripts/activate &&\
	python -m pip install --upgrade pip setuptools wheel && \
	pip install -r requirements.txt && \
	pip install . &&\
	python -m ipykernel install --user --name "$(notdir $(CURDIR))-venv" --display-name "Python ($(notdir $(CURDIR)))"

app:
	source .venv/Scripts/activate &&\
	streamlit run src/main.py --server.port 8502