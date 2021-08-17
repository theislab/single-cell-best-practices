FROM ubuntu:21.10

LABEL authors="Lukas Heumos (lukas.heumos@posteo.net)" \
    description="Docker image containing all requirements for building the single-cell tutorial"

# To get real time output we need to disable the stdout buffer
ENV PYTHONUNBUFFERED 1
# Enable colors
ENV TERM xterm-256color

# Install some basic utilities
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    ca-certificates \
    sudo \
    git \
    bzip2 \
    libx11-6 \
    build-essential \
    lshw \
    && rm -rf /var/lib/apt/lists/*

# Install & update Conda
RUN wget -O ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-py39_4.10.3-Linux-x86_64.sh \
    && chmod +x ~/miniconda.sh \
    && ~/miniconda.sh -b -p ~/miniconda \
    && rm ~/miniconda.sh
ENV PATH=/root/miniconda/bin:$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false
RUN conda update conda

# Install Mamba
RUN conda install -c conda-forge mamba

# Copy and install the environment.yml file into a new environment
COPY environment.yml .
RUN mamba env create -f environment.yml && mamba clean -a

# Activate the environment
RUN echo "source activate single-cell-tutorial" >> ~/.bashrc
ENV PATH /root/miniconda/envs/single-cell-tutorial/bin:$PATH

# Dump the details of the installed packages to a file for posterity
RUN mamba env export --name single-cell-tutorial > single_cell_tutorial_environment.yml
