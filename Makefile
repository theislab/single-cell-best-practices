JUPYTER_BOOK_DIR = jupyter-book
JUPYTER_KERNEL := python3

serve:
	cd $(JUPYTER_BOOK_DIR) && jupyter book start

build:
	cd $(JUPYTER_BOOK_DIR) && jupyter book build --html

dropdown:
	python3 scripts/dropdowns/insert_dropdowns.py

clean:
	cd $(JUPYTER_BOOK_DIR) && jupyter book clean --all

pdf:
	cd $(JUPYTER_BOOK_DIR) && jupyter book build --pdf
