SHELL := /bin/bash


.PHONY: setup

setup:
	@python3 -m venv .venv --clear
	@.venv/bin/pip3 install --upgrade pip --quiet
	@.venv/bin/pip3 install poetry
	@.venv/bin/poetry config virtualenvs.in-project true
	@.venv/bin/poetry install --no-interaction
	@echo ""
	@echo ""
	@echo "Setup complete. Activate the virtual environment with: source .venv/bin/activate"
