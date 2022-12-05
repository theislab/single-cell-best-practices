FROM mambaorg/micromamba:1.1.0

ADD . .

RUN find . -name "*_environment.yml" | xargs -n1 micromamba create -f
