.DEFAULT_GOAL := all
project_path = src/kk_plap_generator
mypylint = mypy $(project_path) --ignore-missing-imports --no-warn-unused-ignores --warn-redundant-casts --warn-unused-ignores --pretty --show-error-codes --check-untyped-defs

.PHONY: format
format:
	ruff format $(project_path)
	ruff check --fix
	$(mypylint)

.PHONY: lint
lint:
	ruff check
	$(mypylint)

.PHONY: test
test:
	pytest $(project_path)
.PHONY: all

all: lint test
