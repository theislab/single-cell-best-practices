JUPYTER_BOOK_DIR = jupyter-book
JUPYTER_KERNEL := python3

build:
	jupyter-book build $(JUPYTER_BOOK_DIR)

build-all:
	jupyter-book build --all $(JUPYTER_BOOK_DIR)

clean:
	jupyter-book clean --all $(JUPYTER_BOOK_DIR)

pdf:
	jupyter-book build jupyter-book/ --builder pdfhtml
