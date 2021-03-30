# OpenCV gRPC Docker integration


## Overview

This directory provides Dockerfiles to be able to run the gRPC service with Docker.
The docker image already has all the project dependencies installed.
Also, it is already build with the necessary sources for the gRPC service to run.


## Usage

In order to use the images, execute the following command:

```shell
$ docker run --rm -it -p 8061:8061 --mount type=bind,source=<path to file with function>,target=/workspace/external.py sipgisr/opencv-grpc:<specific tag>-latest
```

NOTE: The `<path to file with function>` must be the absolute path to the file where the `calling_function` is defined.

### Available Tags

* `generic-latest` is used to tag the generic images gRPC service
* `poses-latest` is used to tag the image with poses gRPC service

## Environment Variables

The docker images define several environment variables, to enable additional customization:

### MODULE

`MODULE` defines the name of the external module (the default is 'external').

### PORT

`PORT` specifies the port where the gRPC server should listen (the default is 8061).


## Building the image

In this repository, we define multiple gRPC services. 
In order to build the image for a specific service, execute the respective command *(from the repository root directory)*:

### Generic Image Service

```shell
$ docker build --tag sipgisr/opencv-grpc:generic-latest --build-arg SERVICE_NAME=image_generic -f docker/Dockerfile .
```

### Image With Poses Service

```shell
$ docker build --tag sipgisr/opencv-grpc:poses-latest --build-arg SERVICE_NAME=image_with_poses -f docker/Dockerfile .
```