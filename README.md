# OpenCV gRPC Services

## Overview

This repository offers an integration between OpenCV and gRPC.
It defines a gRPC service that uses OpenCV to process images and possible human poses in the given image. 
The human poses are defined according to the Open-Pose skeletons.

## Usage

The gRPC service is deployed with docker. 
The service expects an external module with a function called 'calling_function'.
This function is implemented externally and should be mounted or added to the image.

In order to use this image, execute the following steps *(from the repository root directory)*:

* Build the image:

```shell
$ docker build --tag opencv-grpc-server:latest -f docker/Dockerfile . 
```

* Run the image:

```shell
$ docker run --rm -it -p 50051:50051 --mount type=bind,source=<path to file with calling_function>,target=/opencv-grpc/external.py --name opencv-grpc-server opencv-grpc-server:latest
```

For more information, see these [instructions](docker/README.md).


## Calling Function Signature

The specification of the 'calling_function' is as follows:

```
(image: bytes, poses: List[Dict[int:(float,float)]]) -> bytes
```

### image

`image` is the bytes for the original unprocessed image, encoded in some format (ex: .jpeg).

### poses

`poses` are the human poses that were found in the image. 
Each dictionary is a different pose.
The key-value pairs in the dictionaries represent key-points.
The keys are the index of the key-point, and the value are the x and y coordinates for the keypoint.

### return

The return value is the bytes for the image after it was processed, encoded in some format (ex: .jpeg).

## gRPC Service Definition

The gRPC service is defined in the [opencv_service](protos/image_with_poses.proto) proto file.
It defines a single unary method. 
Each request will invoke the 'calling_function' with the received parameters.