FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Update system
RUN apt update && apt upgrade -y

# Install NS-3 dependencies (from your document)
RUN apt install -y \
    build-essential \
    gcc \
    g++ \
    gdb \
    git \
    cmake \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    pkg-config \
    sqlite3 \
    libsqlite3-dev \
    libxml2 \
    libxml2-dev \
    libgtk-3-dev \
    qtbase5-dev \
    qtchooser \
    qt5-qmake \
    qtbase5-dev-tools \
    libboost-all-dev \
    doxygen \
    graphviz \
    wget \
    curl \
    unzip \
    tcpdump \
    wireshark

RUN apt -y install python-is-python3
RUN pip install matplotlib numpy pandas tqdm pyshark

# Clone custom NS-3 NB-IoT repository
WORKDIR /

RUN git config --global http.version HTTP/1.1
RUN git config --global protocol.version 0

RUN git -c http.version=HTTP/1.1 -c protocol.version=0 \
        ls-remote https://github.com/h3dema/ns3-nbiot-ambient-iot.git

RUN git -c http.version=HTTP/1.1 -c protocol.version=0 \
        clone https://github.com/h3dema/ns3-nbiot-ambient-iot.git /opt/ns3-nbiot

# copy the example scenario file (list the in docs) into the scratch directory
# COPY example/nb-scenario5.cc /opt/ns3-nbiot/scratch

# Set working directory to the NS-3 directory
WORKDIR /opt/ns3-nbiot

# Build NS-3
RUN ./waf configure && \
    ./waf build

# Default command: open a shell inside the NS-3 directory
CMD ["/bin/bash"]
