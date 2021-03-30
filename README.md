# OpenCV gRPC Services


## Overview

This repository offers an integration between OpenCV and gRPC.
It specifies multiple gRPC services that use OpenCV to process images,
executing an arbitrary function that is defined by the user.


## Usage

In this section, we show how to deploy any service with [Docker](https://www.docker.com), using your own code.

The services expect an external module with a function called `calling_function`.
This function is implemented externally and should be mounted or added to the image.

All the services have a unique service interface, defined in the [protos](protos) directory,
and a specific `calling_function` signature.

In each request, the services will invoke the `calling_function` with the received parameters.

In order to run the [image](https://hub.docker.com/r/sipgisr/opencv-grpc) 
with the desired service *([list of available tags](docker/README.md#available-tags))*, execute the following command:

```shell
$ docker run --rm -it -p 8061:8061 --mount type=bind,source=<path to file with function>,target=/workspace/external.py sipgisr/opencv-grpc:<specific tag>-latest
```

NOTE: The `<path to file with function>` must be the absolute path to the file where the `calling_function` is defined.

For more information on how to use the docker images, see these [instructions](docker/README.md).


## Services Description

In this section, we present the multiple services that this repository offers:

 * Generic Image Service
 * Image With Poses Service


### Generic Image Service

The generic image service just applies a given transformation in an image.
It receives an image as parameter and outputs the transformed image.

The gRPC service interface is defined in the [image_generic protobuf file](protos/image_generic.proto),
and has the following `calling_function` signature:

```python
def calling_function(image):
    """
    (image: bytes) -> bytes
    """
    pass
```

#### image

`image` is the bytes for the original unprocessed image, encoded in some format (ex: .jpeg).

#### return

The return value is the bytes for the image after it was processed, encoded in some format (ex: .jpeg).


### Image With Poses Service

The image with poses services receives a given image, as well as the detected human poses for the image,
and applies a transformation to the given image.

The gRPC service interface is defined in the [image_with_poses protobuf file](protos/image_with_poses.proto),
and has the following `calling_function` signature:

```python
def calling_function(image, poses):
    """
    (image: bytes, poses: List[Dict[int:(float,float)]]) -> bytes
    """
    pass
```

#### image

`image` is the bytes for the original unprocessed image, encoded in some format (ex: .jpeg).

#### poses

`poses` are the human poses that were found in the image. 
Each dictionary is a different pose.
The key-value pairs in the dictionaries represent key-points.
The keys are the index of the key-point, and the value are the x and y coordinates for the keypoint.

#### return

The return value is the bytes for the image after it was processed, encoded in some format (ex: .jpeg).