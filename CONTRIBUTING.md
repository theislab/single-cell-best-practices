# Contributing

We highly welcome community contributions and encourage contributions.
However, the complex single-cell environments and the modern building of a book with integrated code entails a complex environment setup.

## Book architecture

TODO

## Environment setup

### Container

Due to the inherent complexity of the required setup we only support the setup with Docker based containers.
We maintain our own container at [this repository](https://github.com/theislab/single-cell-tutorial-container).
These instructions will be updated as soon as the container has regular releases.
For now:

Follow: https://github.com/theislab/extended-single-cell-best-practices-container/

Note: This container is very big and complex. It has 90% of the packages that are required to build the respective notebooks. We are working on new solutions for the notebook environments in the future, because cramming everything into a single container does not really work out.

## Executing the notebooks

From inside the Docker container run an alias for `jupyter-lab`:

```bash
jl
```

Note that this command is an alias for

```bash
jupyter-lab --no-browser --ip=0.0.0.0 --allow-root /root/host_home
```

Now simply open the jupyter-lab instance and modify the Jupyter notebooks.

## Building the book

From inside the Docker container navigate to the root of the code. Then execute

```bash
make
```

which will build the complete book. All previously run notebooks are cached and will not rerun.

To force a rebuild of the complete book including all notebooks run:

```bash
make build-all
```

To clean the build directory run:

```bash
make clean
```

## Contributing new best-practices, tutorials, quizzes and solutions

### best-practices

Contributing or correcting new best-practices is welcome, but subject to a high standard. Our philosophy is that we base our recommendations only on external (= not by the tools' authors) and independent benchmarks. Therefore, if you propose new best-practices we strongly advise you to open an issue first and discuss them with us. We will certainly have questions, but are super keen on getting to know the latest best-practices.

### Contributing new tutorials, quizzes and solutions

We want this book to become a prime resource for introducing people to the field of single-cell and especially best-practice data analysis. In the past we have been involved in many teaching efforts and we noticed that it is imperative to make people reflect on their learning for the most effective outcome. Therefore, we try to add many small quizzes with solutions for self-learners to encourage such a learning style. These quizzes and solutions can always be extended and we would be happy to get community help.

Entirely new tutorials on topics not yet covered or extensions are subject to "best-practices" and we would encourage you to get in touch first with us by opening an issue to discuss such an addition. If best-practices for a new topic do not yet exist (e.g. multimodal data analysis) we are generally open for new tutorials, but again, please ask us first to ensure that your work is not in vain.
