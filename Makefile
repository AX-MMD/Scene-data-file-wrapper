.DEFAULT_GOAL := all
isort = isort kk-plap-generator
black = black kk-plap-generator

.PHONY: format
format:
	$(isort)
	$(black)
	flakeheaven lint kk-plap-generator --format=colored

.PHONY: lint
lint:
	$(isort) --check-only
	$(black) --check
	flakeheaven lint kk-plap-generator --format=colored

.PHONY: test
test:
	pytest --cov
.PHONY: all

all: lint test
