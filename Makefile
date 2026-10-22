PYTHON ?= .venv/bin/python
.PHONY: html latex pdf bundle all
html latex pdf bundle all:
	$(PYTHON) scripts/build_book.py $@
