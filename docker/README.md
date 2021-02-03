# OpenCV gRPC Docker integration

## Overview

This directory provides Dockerfiles to be able to run the gRPC service with Docker.
The docker image already has all the project dependencies installed.
Also, it is already build with the necessary sources for the gRPC service to run.

## Usage

In order to use this image, execute the following steps *(from the repository root directory)*:

* Build the image:

```shell
$ docker build --tag opencv-grpc-server:latest -f docker/Dockerfile . 
```

* Run the image:

```shell
$ docker run --rm -it -p 50051:50051 --mount type=bind,source=<path to file with function>,target=/opencv-grpc/external.py --name opencv-grpc-server opencv-grpc-server:latest
```

## Environment Variables

The docker image defines several environment variables:

### MODULE

`MODULE` defines the name of the external module (the default is 'external').


### PORT

`PORT` specifies the port where the gRPC server should listen (the default is 50051).