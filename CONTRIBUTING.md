# Contributing

We highly welcome community contributions and encourage contributions.

## Book architecture

The following depicts the rough structure of the book inside the `jupyter_book` folder.
Beyond several configuration files, all chapters are stored inside corresponding folders, such as for example, `conditions`.
Inside, the corresponding notebooks, together with the associated `reference.bib` and `environment.yml` files, are stored.

```bash
├── conditions
│   ├── compositional_environment.yaml
│   ├── compositional.ipynb
│   ├── compositional_references.bib
│   ├── differential_gene_expression.bib
│   ├── differential_gene_expression.ipynb
│   ├── gsea_pathway.bib
│   ├── gsea_pathway_environment.yml
│   ├── gsea_pathway.ipynb
│   ├── perturbation_modeling.bib
│   ├── perturbation_modeling_environment.yml
│   └── perturbation_modeling.ipynb
├── ...
├── _toc.yml
├── _config.yml
├── acknowledgements.md
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

which will build the complete book. This does not execute any notebooks and any updated chapters must be updated in a separate step.

To clean the build directory run:

```bash
make clean
```

### Building individual chapters

All chapters are available as Jupyter Notebooks and end-to-end executable.
The diverse requirements of tools for the chapters do not allow it for us to provide a single environment that can build all chapters.
Hence, we decided to provide minimal Conda environments per chapter. These can be found in the respective folders.

## Guide for contributors

### Structure of our chapter

First of all, each chapter comes with a few files.
In the `.ipynb` you write the main content and cite the references from `.bib`.
The `.yml` file stores the minimal Conda environments, mentioned [above](#building-individual-chapters).
The `_keytakeaways.txt` stores the key takeaways of the chapter in the corresponding [format](#key-takeaways-environment-and-lamin-dropdown).

```bash
├── section_1
│   ├── chapter_1.ipynb
│   ├── chapter_1.bib
│   ├── chapter_1.yml
│   ├── chapter_1_keytakeaways.txt
│   ├── chapter_2.ipynb
│   ├── ...
```

Each chapter is structured as follows:

1. Title
2. Dropdowns
   - Key takeaways
   - Env setup
   - Lamin setup
3. Main content
4. Quiz/flashcards
5. See also dropdown (useful links/further readings)
6. References
7. Contributors

All dropdowns directly after the title are automatically inserted, when they meet the [requirements](#key-takeaways-environment-and-lamin-dropdown).
Besides that every chapter should end with some questions covering the main aspects of the chapter.
See the paragraph below to see [how to create our costum quiz/flashcard](#create-quizflashcards).

### Rules

- Every sentence should be in its own row (makes reviewing easier).
- Write in American English!
- Always add a term to the glossary if it is used several times in the book. If it is just used once and the term might be unclear, directly clarify the term in the corresponding chapter.
- In a chapter, only link the first occurrence of a term to the glossary. Do not link the term every single time within the text of a chapter.
- If you want to link a term that semantically means the same thing or is not spelled exactly the same in the glossary use: {term}`your term <glossary term>`(e.g.: {term}`barcodes <Barcode>`)
- Use dropdowns whenever possible.
- Based on ours of proofreading: Always make a space before “cite” (e.g., {cite}`Smith2017`)!

`<span>{cite}`Smith2017`</span>`

### Key takeaways, environment, and lamin dropdown

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
> Executing `make dropdown` locally will modify nearly all notebook files. These changes should never be committed or pushed to the repository. We recommend discarding these changes immediately after running the command using `git restore .`. Ensure you’ve staged your wanted changes (`git add`) beforehand.

### Create Quiz/flashcards

## Environment setup

Run the following command with the environment file of choice to create the environment for the chapter that you want to build.

```bash
conda env create -f CHAPTER.yml
```

Now you can execute all cells in the notebook.

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

## Contributing new best practices, tutorials, quizzes and solutions

### best practices

Contributing or correcting new best practices is welcome, but subject to a high standard. Our philosophy is that we base our recommendations only on external (= not by the tools' authors) and independent benchmarks. Therefore, if you propose new best practices we strongly advise you to open an issue first and discuss them with us. We will certainly have questions, but are super keen on getting to know the latest best practices.

### Contributing new tutorials, quizzes and solutions

We want this book to become a prime resource for introducing people to the field of single-cell and especially best practice data analysis. In the past we have been involved in many teaching efforts, and we noticed that it is imperative to make people reflect on their learning for the most effective outcome. Therefore, we try to add many small quizzes with solutions for self-learners to encourage such a learning style. These quizzes and solutions can always be extended, and we would be happy to get community help.

Entirely new tutorials on topics not yet covered or extensions are subject to "best practices" and we would encourage you to get in touch first with us by opening an issue to discuss such an addition. If best practices for a new topic do not yet exist we are generally open for new tutorials, but again, please ask us first to ensure that your work is not in vain!
