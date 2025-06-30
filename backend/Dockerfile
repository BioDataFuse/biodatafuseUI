FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /

COPY ./ ./

# Define the version of Python to install
# For example "3.11" will get the latest version of 3.11 (ex 3.11.4, 3.11.5, etc)
ARG PYVER="3.9"

# Update package list & install necessary dependencies
RUN apt-get update -y
RUN apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    python3-pip \
    npm \
    nodejs 

RUN apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get install -y python$PYVER-dev \ 
    python$PYVER-distutils

# Set PYVER as the default Python interpreter
RUN update-alternatives --install /usr/bin/python3 python /usr/bin/python$PYVER 1
RUN update-alternatives --set python /usr/bin/python$PYVER


RUN python3 -m pip install --force-reinstall --no-deps blinker==1.9.0 --ignore-installed
RUN python3 -m pip install --force-reinstall --no-deps cryptography==41.0.7 --ignore-installed


# Install packages in requirements.txt
RUN python3 -m pip install --upgrade setuptools --break-system-packages 
RUN python3 -m pip install --no-cache-dir -r requirements.txt --break-system-packages

EXPOSE 8000 

CMD ["/bin/bash", "-c", "python3 run.py"]
