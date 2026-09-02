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
# when the repo is public, use the following line
RUN git clone https://github.com/BelogaevIDLab/ns3-nbiot.git
# since it is private, use the clone below and you need to pass the ssh key to docker using SSH-AGENT
# Add GitHub to known_hosts so SSH clone works
# RUN mkdir -p /root/.ssh && \
#     ssh-keyscan github.com >> /root/.ssh/known_hosts
# RUN --mount=type=ssh git clone git@github.com:BelogaevIDLab/ns3-nbiot.git /opt/ns3-nbiot


WORKDIR /opt/ns3-nbiot

# Build NS-3
RUN ./waf configure && \
    ./waf build

# Default command: open a shell inside the NS-3 directory
CMD ["/bin/bash"]
