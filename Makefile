.DEFAULT_GOAL := all
project_name = kk_plap_generator
mypylint = mypy $(project_name) --ignore-missing-imports --no-warn-unused-ignores --warn-redundant-casts --warn-unused-ignores --pretty --show-error-codes --check-untyped-defs

.PHONY: format
format:
	ruff format $(project_name)
	ruff check --fix
	$(mypylint)

.PHONY: lint
lint:
	ruff check
	$(mypylint)

.PHONY: need_update
need_update:
	flakeheaven lint kk-plap-generator --format=colored

.PHONY: test
test:
	pytest $(project_name)
.PHONY: all

all: lint test
