FROM osrf/ros:humble-desktop

SHELL ["/bin/bash", "-c"]

ENV RCUTILS_COLORIZED_OUTPUT=1

# Install dependencies
RUN apt update && \
    apt install -y \
    build-essential \
    cmake \
    git \
    curl \
    lsb-release \
    gnupg \
    libbullet-dev \
    python3-colcon-common-extensions \
    python3-flake8 \
    python3-pip \
    python3-pytest-cov \
    python3-rosdep \
    python3-setuptools \
    python3-vcstool \
    python3-colcon-clean \
    wget \
    clang-format

# Install Python packages
RUN python3 -m pip install -U \
    argcomplete \
    flake8-blind-except \
    flake8-builtins \
    flake8-class-newline \
    flake8-comprehensions \
    flake8-deprecated \
    flake8-docstrings \
    flake8-import-order \
    flake8-quotes \
    pytest-repeat \
    pytest-rerunfailures \
    pytest 

# Install Gazebo Harmonic - Default Gazebo version in ROS2 Humble is Fortress
RUN curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
RUN apt-get update
RUN apt-get install -y ros-humble-ros-gzharmonic
RUN apt install -y \
    ros-humble-turtle-tf2-py \
    ros-humble-tf2-tools \
    ros-dev-tools \
    ros-humble-plotjuggler-ros

RUN apt-get update
RUN apt-get upgrade -y

# Install CrazySim with crazyflie-firmware
ARG HOME=/root
WORKDIR $HOME
RUN git clone https://github.com/gtfactslab/CrazySim.git --recursive 
RUN cd CrazySim && \
    git checkout 8ad9bb8dfe8c827f349b3a224d47f7808c186d06 && \
    git submodule update --init --recursive && \
    cd crazyflie-lib-python && \
    pip install -e .

# Install crazyflie-lib-python
RUN cd $HOME/CrazySim/crazyflie-lib-python && \
    python3 -m pip install -e .

# Install crazyflie-firmware (CMake uses python, so we need to install python-is-python3)
RUN apt-get update && apt-get install -y \
    python-is-python3 && \ 
    python3 -m pip install -U \
    Jinja2

RUN cd $HOME/CrazySim/crazyflie-firmware && \
    mkdir -p sitl_make/build && \
    cd sitl_make/build && \
    cmake .. && \
    make all

# Additional dependencies for evs_gz_utils
RUN python3 -m pip install -U \
    numpy==1.22 \
    quaternionic

# Copy workspace
COPY . /root/ros2_ws

# Add useful things to bashrc
RUN echo ". /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc \
    && echo ". /root/ros2_ws/install/setup.bash" >> ~/.bashrc \
    && echo "alias cd_crazysim='cd /root/CrazySim'" >> ~/.bashrc 

CMD [ "sleep", "infinity" ]
