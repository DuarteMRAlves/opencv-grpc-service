# Test for the estimation of a single image key-points

import argparse
import grpc
import io
import matplotlib.pyplot as plt
import opencv_service_pb2
import opencv_service_pb2_grpc
import PIL.Image as PIL_image


def create_random_keypoints(x_coords, y_coords):
    return [
        opencv_service_pb2.KeyPoint(
            index=i,
            x=x_coords,
            y=y_coords,
            score=1
        )
        for i in range(18)
    ]

def create_random_poses():
    key_points1 = create_random_keypoints(1, 1)
    key_points2 = create_random_keypoints(2,2)
    poses = (
        opencv_service_pb2.Pose(key_points=key_points1),
        opencv_service_pb2.Pose(key_points=key_points2)
    )
    return opencv_service_pb2.DetectedPoses(poses=poses)


def process_image(stub, image_path):
    print(f'Processing image: \'{image_path}\'')
    with open(image_path, 'rb') as fp:
        image_bytes = fp.read()
    image = opencv_service_pb2.Image(data=image_bytes)
    poses = create_random_poses()
    request = opencv_service_pb2.ImageWithPoses(
        image=image,
        detected_poses=poses)
    return stub.process(request)


def display_image(image):
    img = PIL_image.open(io.BytesIO(image.data))
    ax = plt.gca()
    ax.imshow(img)
    plt.show()


def parse_args():
    """
    Parse arguments for test setup

    Returns:
        The arguments for the test
    """
    parser = argparse.ArgumentParser(description='Test for OpenPose gRPC Service')
    parser.add_argument(
        'image',
        help='Path to the image to send to the server')
    parser.add_argument(
        '--target',
        metavar='target',
        default='localhost:8061',
        help='Location of the tested server (defaults to localhost:50051)')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    target = args.target
    image_path = args.image
    with grpc.insecure_channel(target) as channel:
        estimator_stub = opencv_service_pb2_grpc.OpenCVServiceStub(channel)
        try:
            response = process_image(estimator_stub, image_path)
            display_image(response)
        except grpc.RpcError as rpc_error:
            print('An error has occurred:')
            print(f'  Error Code: {rpc_error.code()}')
            print(f'  Details: {rpc_error.details()}')
