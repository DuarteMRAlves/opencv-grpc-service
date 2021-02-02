import concurrent.futures as futures
import grpc
import importlib
import inspect
import logging
import opencv_service_pb2
import opencv_service_pb2_grpc
import os
import time


_MODULE_ENV_VAR = 'MODULE'
_MODULE_DEFAULT = 'external'

_PORT_ENV_VAR = 'PORT'
_PORT_DEFAULT = 50051

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

_CALLING_FUNCTION_NAME = 'calling_function'


class ServiceImpl(opencv_service_pb2_grpc.OpenCVServiceServicer):

    def __init__(self, calling_function):
        """
        Args:
            calling_function: the function that should be called
                              when a new request is received

                              the signature of the function should be:

                              (image: bytes, poses: List[Dict[int,(float, float)]])
                              -> bytes

                              as described in the process method

        """
        self.__calling_fn = calling_function

    def process(self, request, context):
        """Processes a given ImageWithPoses request

        It expects that a process function was already registered
        with the following signature

        (image: bytes, poses: List[Dict[int,(float, float)]]) -> bytes

        Image is the bytes of the image to process.

        Poses represent the detected poses. Each element of the list
        is a dictionary representing a detected pose. The dictionary is
        indexed by the key-point index and the values are the relative
        coordinates of the key-point

        Args:
            request: The ImageWithPoses request to process
            context: Context of the gRPC call

        Returns:
            The Image with the applied function

        """
        image = request.image.data
        poses = [
            self.__build_pose_dictionary(pose)
            for pose in request.detected_poses.poses
        ]
        print(poses)
        processed_image = self.__calling_fn(image, poses)
        return opencv_service_pb2.Image(data=processed_image)

    @staticmethod
    def __build_pose_dictionary(pose):
        """Transforms a Pose protobuf message into a Dict[int,(float, float)]

        Args:
            pose: The Pose protobuf message

        Returns:
            A new dictionary indexed by the key-point indexed
            and with the coordinates of the key-point as values

        """
        return {kp.index: (kp.x, kp.y) for kp in pose.key_points}


def get_port():
    """
    Parses the port where the server should listen
    Exists the program if the environment variable
    is not an int or the value is not positive
    Returns:
        The port where the server should listen
    """
    try:
        server_port = int(os.getenv(_PORT_ENV_VAR, _PORT_DEFAULT))
        if server_port <= 0:
            logging.error('Port should be greater than 0')
            exit(1)
        return server_port
    except ValueError:
        logging.exception('Unable to parse port')
        exit(1)


def import_module(name):
    """Imports the given module

    Args:
        name: name of the module to import

    Returns:
        The module if successful and None otherwise

    """

    try:
        return importlib.import_module(name)
    except ImportError as err:
        logging.exception('Unable to import module with external code', err)
        return None


def get_calling_function(module, name):
    """Tries to retrieve the function with the given
    name from the given module

    Args:
        module: module for the function
        name: name to search

    Returns:
        The found function if any or None otherwise

    """
    candidates = inspect.getmembers(
        module,
        lambda x: inspect.isfunction(x) and x.__name__ == name
    )
    num_candidates = len(candidates)
    if num_candidates == 1:
        return candidates[0][1]
    else:
        logging.error(f'No function with name \'{name}\' in module \'{module.__name__}\'')
        return None


if __name__ == '__main__':
    logging.basicConfig()
    module_name = os.getenv(_MODULE_ENV_VAR, _MODULE_DEFAULT)
    # Check if external module was imported
    module = import_module(module_name)
    if not module:
        exit(1)

    calling_fn = get_calling_function(module, _CALLING_FUNCTION_NAME)
    if not calling_fn:
        exit(1)

    port = get_port()
    target = f'[::]:{port}'
    server = grpc.server(futures.ThreadPoolExecutor())
    opencv_service_pb2_grpc.add_OpenCVServiceServicer_to_server(
        ServiceImpl(calling_fn),
        server)
    server.add_insecure_port(target)
    server.start()
    logging.info(f'Server started at {target}')
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
