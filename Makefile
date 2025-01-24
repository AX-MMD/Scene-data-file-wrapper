.DEFAULT_GOAL := all
isort = isort kk-plap-generator
black = black kk-plap-generator
mypylint = mypy kk-plap-generator

.PHONY: format
format:
	$(isort)
	$(black)
	$(mypylint)

.PHONY: lint
lint:
	$(isort) --check-only
	$(black) --check
	$(mypylint)

.PHONY: need_update
need_update:
	flakeheaven lint kk-plap-generator --format=colored

.PHONY: test
test:
	pytest --cov
.PHONY: all

all: lint test
