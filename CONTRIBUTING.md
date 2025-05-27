# Contributing

## Our philosophy

We aim for this book to be a resource for introducing people to single-cell and spatial data analysis while ensuring that newcomers and experienced analysts alike do things properly.
To ensure our recommendations reflect best practices, we try to rely exclusively on external and independent benchmarks.

## How can I contribute?

We warmly welcome contributions, especially those that help us keep our best practices up to date!
However, as mentioned [above](#our-philosophy), these recommendations are held to high standards.

If you're proposing new tutorials, corrections, or extensions, we strongly recommend opening an issue first to talk about your ideas with us.
We're always eager to learn about the latest developments and are happy to discuss the current state of best practices.
We also encourage contributions in the form of [quizzes and flashcards](#create-custom-quizzes-and-flashcards).
Whatever proposal you have: Just open an issue and let's get in touch!

[![Open an Issue](https://img.shields.io/badge/Open%20Issue-blue?logo=github)](https://github.com/theislab/single-cell-best-practices/issues/new?title=Your+Issue+Title&body=Describe+your+issue+here)

## Book architecture

The `jupyter_book` folder contains the source content and configuration for the book.
In addition to several configuration files, all chapters are grouped into their respective section folders — for example, the `conditions` folder.
Each section contains the relevant notebooks along with their [associated files](#essential-files-for-every-chapter).

Here’s an example of the folder layout:

```bash
├── conditions
│   ├── compositional_keytakeaways.txt
│   ├── compositional.bib
│   ├── compositional.ipynb
│   ├── compositional.yml
│   ├── differential_gene_expression_keytakeaways.txt
│   ├── differential_gene_expression.bib
│   ├── differential_gene_expression.ipynb
│   ├── differential_gene_expression.yml
│   ├── gsea_pathway_keytakeaways.txt
│   └── ...
├── ...
├── _toc.yml
├── _config.yml
├── acknowledgements.md
├── CHANGELOG.md
├── glossary.md
├── outlook.md
├── preamble.md
├── _static
│   ├── book.css
│   ├── book.js
│   ├── favicon.ico
│   ├── images
│   │   ├── conditions
│   │   │   ├── compositional.jpg
│   │   │   └── differential_gene_expression.jpg
│   │   └── ...
```

## Building the book

The book requires the following dependencies to be installed:

1. jupyter-book
2. jupytext
3. beautifulsoup4

[An example Conda environment can be found here](https://github.com/theislab/single-cell-best-practices/blob/development/environment.yml).

Run the following command with the environment file to create the environment to build the book.

```bash
conda env create -f environment.yml
```

Building the book is then as simple as:

```bash
make
```

which will build the complete book.
This does not execute any notebooks and any updated chapters must be updated in a separate step.

To clean the build directory run:

```bash
make clean
```

### Building individual chapters

All chapters are available as Jupyter Notebooks and end-to-end executable.
The diverse requirements of tools for the chapters do not allow it for us to provide a single environment that can build all chapters.
Hence, we decided to provide minimal Conda environments per chapter.
These can be found in the respective folders.

> [!NOTE]
> Run the following command with the environment file of choice to create the environment for the chapter that you want to build.
>
> ```bash
> conda env create -f CHAPTER-NAME.yml
> ```
>
> Now you can execute all cells in the notebook.

## Style guide for contributors

### Essential files for every chapter

Each chapter comes with a few essential files.
The `.ipynb` notebook contains the main content and includes citations drawn from the accompanying `.bib` file.
The `.yml` file defines a minimal Conda environment, as described [above](#building-individual-chapters).
Finally, the `_keytakeaways.txt` file summarizes the chapter’s main ideas, following the specified [format](#key-takeaways-environment-and-lamin-dropdown).

```bash
├── SECTION-NAME
│   ├── CHAPTER-NAME.ipynb
│   ├── CHAPTER-NAME.bib
│   ├── CHAPTER-NAME.yml
│   ├── CHAPTER-NAME_keytakeaways.txt
│   ├── ...
```

### Notebook Structure

Each `.ipynb` notebook should follow this standard structure:

1. 🧠 **Title**
2. 🔽 **Dropdown Section**
   - Key Takeaways
   - Environment Setup
   - Lamin Setup
3. 📖 **Main Content**
4. 🔗 **See Also** _(Dropdown)_
5. ❓ **Quiz / Flashcards**
6. 📚 **References**
7. 👥 **Contributors**

All dropdowns immediately following the title are automatically inserted if they meet the corresponding [requirements](#key-takeaways-environment-and-lamin-dropdown).
In addition, each chapter should conclude with a few questions that reinforce the main concepts covered.
[Below](#create-custom-quizzes-and-flashcards) you will find instructions on how to create quizzes and flashcards in our custom format.
We’ve also prepared a chapter [template](/jupyter-book/template/template.ipynb) with which you can quickly and effectively create a chapter for our book.

### Helpful links

- [Jupyter Book documentation](https://jupyterbook.org/en/stable/intro.html)
- [MyST Markdown documentation](https://mystmd.org)
- [Sphinx documentation](https://www.sphinx-doc.org/en/master/)

### Rules

- Place each sentence on its own line to make reviewing easier.
- Use dropdowns so that the reader is not overwhelmed by the content.
- To reduce noise, we should aim to write clean code that avoids generating warnings, and also filter out any non-informative warnings at the start of the notebook.
- In each chapter, link all used glossary terms with `` {term}`EXAMPLE TERM` ``.
  - Only link the **first occurrence** of each term within the chapter — not every time it appears.
  - Add a new term to the glossary only if it appears multiple times throughout the book and has not yet been listed.
    In this case, also add the link to this term in the other chapters.
    If the term is used just once and may be unclear, provide a direct explanation within the corresponding chapter.
  - To link a term that has the same meaning or a different spelling than its glossary entry, use this format: `` {term}`YOUR TERM <GLOSSARY TERM>` `` (e.g.: `` {term}`barcodes <Barcode>` ``).
  - Don't link terms in the key takeaways!
- Based on hours of proofreading: Always make a space before `{cite}` (e.g., ``"This was shown by {cite}`Smith2017`."``).
- References should always contain `doi` and `url`.
- Write in American English.

### Key takeaways, environment and lamin dropdown

The environment and lamin dropdowns are inserted after the title of every chapter.
If you don't want to have those dropdowns in your chapter, make sure to list your notebook in the blacklists of `scripts/dropdowns/keytakeaways.py` (`black_list_files_yml` or `black_list_files_lamin`).
A key takeaways dropdown is only inserted if a file called `<name-notebook>_keytakeaways.txt` is in the same directory as your notebook.
This file has to contain the key takeaways in the following format:

```
1
The first sentence of key takeaway 1.
The second sentence of key takeaway 1.

2
The first sentence of key takeaway 2.

...
```

If you want to link a key takeaway to a certain heading in your chapter, add `<section-name>-<notebook-name>-key-takeaway-<key-takeaway-number>` as a label before the heading.
Replace all `_` with `-`, and the card of the key takeaway will be linked to the heading in the text (e.g., `(preprocessing-visualization-dimensionality-reduction-key-takeaway-2)=`).

Our CI workflow (`.github/worksflows/build_book.yml`) will call `make dropdown` when building the book.
For testing, you can insert the dropdowns locally by calling `make dropdown` before `make`.

> [!WARNING]
> Executing `make dropdown` locally will modify nearly all notebook files.
> These changes should never be committed or pushed to the repository.
> We recommend discarding these changes immediately after running the command using `git restore .`.
> Ensure you’ve staged your wanted changes (`git add`) beforehand.

### LaminDB

LaminDB is an open-source data framework to enable learning at scale in computational biology.
We use lamindb to store, share, and load datasets and notebooks using the [theislab/sc-best-practices](https://lamin.ai/theislab/sc-best-practices) instance.
We acknowledge free hosting from [Lamin Labs](https://lamin.ai/).

When making contributions that got merged, ask us to be added to the `theislab/sc-best-practices` instance.
Then, ensure that all used datasets are loaded directly from the instance.
If you upload a new dataset to the instance, create a separate notebook for it and place it in the [`scripts`](/scripts/) folder.
You can use the existing notebooks in the [`scripts`](/scripts/) folder as a guide.
Finally, use `ln.track()` and `ln.finish()` while rerunning the notebook, and we have the latest version also in the instance.
The [template](/jupyter-book/template/template.ipynb) shows the basic steps for tracking a notebook!

> [!Note]
>
> 1. **Create a lamin account**
>
>    - Sign up and log in following [the instructions](https://docs.lamin.ai/setup#sign-up-log-in)
>    - Ask us to be added to the `theislab/sc-best-practices` instance.
>
> 2. **Install lamindb**
>
>    - Install the lamindb Python package in your environment:
>
>    ```bash
>    pip install lamindb[bionty,jupyter,zarr]
>    ```
>
> 3. **Connect to the [theislab/sc-best-practices instance](https://lamin.ai/theislab/sc-best-practices)**
>
>    - Run the `lamin connect` command:
>
>    ```bash
>    lamin connect theislab/sc-best-practices
>    ```
>
>    - You should now see `→ connected lamindb: theislab/sc-best-practices`.
>    - You are ready to use lamindb in your notebook!

### Create custom quizzes and flashcards

To build quizzes or flashcards, use the helper functions in `jupyter-book/src/lib.py`.
You can create multiple-choice questions or simple flip cards.

1. Start your notebook code cell with

```python
%run ../src/lib.py
```

2. Then, add as many questions as you like. For example:

```python
flip_card("q1", "What is 2 + 2?", "4")
multiple_choice_question(
   "q1",
   "What is the capital of France?",
   ["Paris", "London", "Berlin", "Madrid"],
   "Paris",
   {
         "London": "London is the capital of the UK",
         "Berlin": "Berlin is the capital of Germany",
         "Madrid": "Madrid is the capital of Spain",
   }
)
```

3. Run the code cell and it will build the multiple-choice questions or flip cards as output.

> [!WARNING]
> Add the cell tag `remove-input` to the code cell to remove the code, when building the book.

You can also adjust the font size, text color and much more.
For detailed information, check out the method descriptions in `jupyter-book/src/lib.py`.

### Pre commit

Pre-commit is a tool that automatically checks your markdown and code for mistakes before you commit it.

1. Please install `pre-commit`:

```bash
pip install pre-commit
```

2. Next, activate it in the root of the repository:

```bash
pre-commit install
```

3. Afterwards, you can always manually run it:

```bash
pre-commit run -a
```

If you try to commit changes, they are automatically checked for errors and adjusted if possible.
Simply add these changes to your commit with `git add`.

### Adding changelog entries with `towncrier`

We use `towncrier` to manage our changelog. Here’s how to include a changelog entry when making a PR:

1. Install `towncrier` (only once):

```bash
pip install towncrier
```

2. Make your pull request as usual.

3. After opening your PR, note the PR number (e.g., 34), and create a changelog fragment:

```bash
towncrier create -c 'update blah blah ([#34](https://github.com/theislab/single-cell-best-practices/pull/34)) <sub>@seohyonkim</sub>' 34.changed.md
```

Replace "update blah blah" with a brief description of your change, PR number with your PR number, and the author of the PR with your github tag.
Valid categories for the filename of the `markdown` are:

`added`
`changed`
`fixed`
`removed`

4. This will create a `.md` file (e.g., `34.changed.md`) in the `changelog.d/` directory (at the root of the repo). Make sure this file is included in your commit.

5. Push your changes again.

#### Releasing a new version (maintainers only)

To release a new version:

1. Run Towncrier to build the changelog:

```bash
towncrier build --yes --version 2.0.0
```

This will update `CHANGELOG.md` and remove the `changelog.d/` directory.

2. Add contributor names and links to the PR manually under each relevant PR entry in the generated `CHANGELOG.md`.

3. Recreate the `changelog.d/` directory for future PRs:

```bash
mkdir changelog.d
touch changelog.d/.gitkeep
```

## Data access

We are currently still working on making all datasets accessible.
The problem here isn't data protection or other terrible reasons, but rather the requirement to host them somewhere and ensuring that the correct versions are used per notebook.
