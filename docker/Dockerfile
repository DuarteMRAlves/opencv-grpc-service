# Define workdir folder for all stages
# Must be renewed in the beggining of each stage
ARG WORKDIR=/opencv-grpc/

# --------------------------------------
# Builder stage to generate .proto files
# --------------------------------------

FROM python:3.8.7-slim-buster as builder
# Renew workdir arg
ARG WORKDIR

RUN pip install --upgrade pip && \
    pip install grpcio grpcio-tools

# Path for the protos folder to copy
ARG PROTOS_FOLDER_DIR=protos

COPY ${PROTOS_FOLDER_DIR} ${WORKDIR}
WORKDIR ${WORKDIR}

# Compile proto file and remove it
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. opencv_service.proto && \
    rm opencv_service.proto


# -----------------------------
# Stage to generate final image
# -----------------------------

FROM python:3.8.7-slim-buster
# Renew workdir arg
ARG WORKDIR

ARG USER=runner
ARG GROUP=runner-group
ARG GRPC_SERVICES_DIR=src

# Create non-privileged user to run
RUN addgroup --system ${GROUP} && \
    adduser --system --no-create-home --ingroup ${GROUP} ${USER}

RUN pip install --upgrade pip && \
    # Install headless version of opencv-python for server usage
    # Does not install graphical modules
    # See https://github.com/opencv/opencv-python#installation-and-usage
    pip install opencv-python-headless grpcio protobuf

# Copy generated .py files
COPY --from=builder --chown=${USER}:${GROUP} ${WORKDIR} ${WORKDIR}
# Copy code
COPY ${GRPC_SERVICES_DIR} ${WORKDIR}

# Change to non-privileged user
USER ${USER}

WORKDIR ${WORKDIR}

CMD ["python", "opencv_service.py"]