JUPYTER_BOOK_DIR = jupyter-book
JUPYTER_KERNEL := python3

serve:
	cd $(JUPYTER_BOOK_DIR) && jupyter book start

build:
	cd $(JUPYTER_BOOK_DIR) && jupyter book build --html
	python3 scripts/postbuild/reload_on_back.py $(JUPYTER_BOOK_DIR)/_build/html
	python3 scripts/postbuild/expand_toc.py $(JUPYTER_BOOK_DIR)/_build/html
	python3 scripts/postbuild/legacy_redirects.py $(JUPYTER_BOOK_DIR)/_build/html

dropdown:
	python3 scripts/dropdowns/insert_dropdowns.py

clean:
	cd $(JUPYTER_BOOK_DIR) && jupyter book clean --all

pdf:
	cd $(JUPYTER_BOOK_DIR) && jupyter book build --pdf
