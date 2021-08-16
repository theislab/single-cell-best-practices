PYTHON_SCRIPTS_DIR = python_scripts
NOTEBOOKS_DIR = notebooks
JUPYTER_BOOK_DIR = jupyter-book
JUPYTER_KERNEL := python3

.PHONY: build clean full-clean
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

build: build-book build-notebooks  # builds the book and all notebooks

build-book:  # builds only the book
	jupyter-book build $(JUPYTER_BOOK_DIR)

# https://nbconvert.readthedocs.io/en/latest/execute_api.html#module-nbconvert.preprocessors
build-notebooks:  # builds all notebooks 
	jupyter nbconvert --ExecutePreprocessor.timeout=6000 --to notebook --inplace --execute $(NOTEBOOKS_DIR)/*.ipynb

clean: clean-book clean-full # cleans the build caches

clean-book:  # Keeps the jupyter-cache cache folder
	jupyter-book clean $(JUPYTER_BOOK_DIR)

clean-full:  # Deletes the jupyter-cache folder
	rm -rf $(JUPYTER_BOOK_DIR)/_build
