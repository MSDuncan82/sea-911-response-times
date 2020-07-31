FROM continuumio/anaconda3

RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    #
    ## apt installs
    && apt-get -y install \
        git \
        openssh-client \
        less \
        iproute2 \
        procps \
        iproute2 \
        lsb-release \
        build-essential \
        bash-completion \
        unzip \
        python3-dev \
        libpq-dev \
        telnet \
    #
    ## pip installs
    && /opt/conda/bin/pip install \
        pylint \
        boto3 \
        python-dotenv \
        ipdb \
        black \
        psycopg2 \
        
    #
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8888
EXPOSE 5432

