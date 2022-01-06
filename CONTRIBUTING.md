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

1. Clone this repository.

   ```bash
   git clone https://github.com/theislab/extended-single-cell-best-practices/
   ```

2. Please ensure that you have docker installed and available on your system.
3. Download the container and start it.

   ```bash
   bash download_container.sh
   docker run --interactive --tty --name sc_best_practice_book_211119 --publish 8888-8892:8888-8892 --volume $HOME:/root/host_home --workdir /root sc_best_practice_book:211119 /bin/bash
   ```

4. Once you are done with your container session, you have two options:
4.1 You can either discard the container with the command below and start over with a clean container the next time using the docker run command from step 3.

```bash
docker rm sc_best_practice_book_211119
```

4.2 Alternatively, you can choose to not remove the container and reuse it in you next session. It will look exactly as you left it with additional packages installed etc. To reuse the container:

```
docker start -i sc_best_practice_book_211119
```

### Downloading the data

TODO

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

Note that this will require the execution of all notebooks to rebuild the book.

## Contributing new best-practices, tutorials, quizzes and solutions

### best-practices

Contributing or correcting new best-practices is welcome, but subject to a high standard. Our philosophy is that we base our recommendations only on external (= not by the tools' authors) and independent benchmarks. Therefore, if you propose new best-practices we strongly advise you to open an issue first and discuss them with us. We will certainly have questions, but are super keen on getting to know the latest best-practices.

### Contributing new tutorials, quizzes and solutions

We want this book to become a prime resource for introducing people to the field of single-cell and especially best-practice data analysis. In the past we have been involved in many teaching efforts and we noticed that it is imperative to make people reflect on their learning for the most effective outcome. Therefore, we try to add many small quizzes with solutions for self-learners to encourage such a learning style. These quizzes and solutions can always be extended and we would be happy to get community help.

Entirely new tutorials on topics not yet covered or extensions are subject to "best-practices" and we would encourage you to get in touch first with us by opening an issue to discuss such an addition. If best-practices for a new topic do not yet exist (e.g. multimodal data analysis) we are generally open for new tutorials, but again, please ask us first to ensure that your work is not in vain.
