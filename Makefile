SHELL := /bin/bash


.PHONY: setup install-local

setup:
	@python3 -m venv .venv --clear
	@.venv/bin/pip3 install --upgrade pip --quiet
	@.venv/bin/pip3 install poetry
	@.venv/bin/poetry config virtualenvs.in-project true
	@.venv/bin/poetry install --no-interaction
	@echo ""
	@echo ""
	@echo "Setup complete. Activate the virtual environment with: source .venv/bin/activate"

install-local:
	@poetry version $(shell git describe --tags --abbrev=0)
	@pipx install --force .
	@poetry version 0.0.0