# Contributing

We highly welcome community contributions and encourage contributions.
There are several

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

## Environment setup

Run the following command with the environment file of choice to create the environment for the chapter that you want to build.

```bash
conda env create -f CHAPTER.yml
```

Now you can execute all cells in the notebook.

## Data access

We are currently still working on making all datasets accessible.
The problem here isn't data protection or other terrible reasons, but rather the requirement to host them somewhere and ensuring that the correct versions are used per notebook.

## Contributing new best practices, tutorials, quizzes and solutions

### best practices

Contributing or correcting new best practices is welcome, but subject to a high standard. Our philosophy is that we base our recommendations only on external (= not by the tools' authors) and independent benchmarks. Therefore, if you propose new best practices we strongly advise you to open an issue first and discuss them with us. We will certainly have questions, but are super keen on getting to know the latest best practices.

### Contributing new tutorials, quizzes and solutions

We want this book to become a prime resource for introducing people to the field of single-cell and especially best practice data analysis. In the past we have been involved in many teaching efforts, and we noticed that it is imperative to make people reflect on their learning for the most effective outcome. Therefore, we try to add many small quizzes with solutions for self-learners to encourage such a learning style. These quizzes and solutions can always be extended, and we would be happy to get community help.

Entirely new tutorials on topics not yet covered or extensions are subject to "best practices" and we would encourage you to get in touch first with us by opening an issue to discuss such an addition. If best practices for a new topic do not yet exist we are generally open for new tutorials, but again, please ask us first to ensure that your work is not in vain!
