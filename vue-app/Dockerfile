FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /home

COPY . /home

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

RUN npm install

EXPOSE 3000

CMD ["/bin/bash", "-c", "cd src; npm run dev"]
