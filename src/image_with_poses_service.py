import concurrent.futures as futures
import grpc
import grpc_reflection.v1alpha.reflection as grpc_reflection
import logging
import image_with_poses_pb2
import image_with_poses_pb2_grpc
import utils


_MODULE_ENV_VAR = 'MODULE'
_MODULE_DEFAULT = 'external'

_PORT_ENV_VAR = 'PORT'
_PORT_DEFAULT = 8061

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

_CALLING_FUNCTION_NAME = 'calling_function'


class ServiceImpl(image_with_poses_pb2_grpc.ImageWithPosesServiceServicer):

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
        processed_image = self.__calling_fn(image, poses)
        return image_with_poses_pb2.Image(data=processed_image)

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


if __name__ == '__main__':
    logging.basicConfig(
        format='[ %(levelname)s ] %(asctime)s (%(module)s) %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)

    calling_fn = utils.get_calling_function()
    if not calling_fn:
        exit(1)

    server = grpc.server(futures.ThreadPoolExecutor())
    image_with_poses_pb2_grpc.add_ImageWithPosesServiceServicer_to_server(
        ServiceImpl(calling_fn),
        server)

    # Add reflection
    service_names = (
        image_with_poses_pb2.DESCRIPTOR.services_by_name['ImageWithPosesService'].full_name,
        grpc_reflection.SERVICE_NAME
    )
    grpc_reflection.enable_server_reflection(service_names, server)

    utils.run_server(server)
