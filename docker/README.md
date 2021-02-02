# OpenCV gRPC Dockers

## Overview

This directory provides Dockerfiles to be able to run the built services with Docker.
The docker images already have all the project dependencies installed.
Also, they are already build with the necessary sources for the gRPC services to run.

## Usage

In order to use this images, executed the following steps *(from the repository root directory)*:

* Build the image:

```shell
$ docker build --tag opencv-grpc-server:latest -f docker/Dockerfile . 
```

* Run the image:

```shell
$ docker run --rm -it -p 50051:50051 --name opencv-grpc-server opencv-grpc-server:latest
```