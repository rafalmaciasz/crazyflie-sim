# crazyflie-sim
CrazyFlie simulation with Gazebo and ROS2 support.

Software version: 
- **ROS 2:** Humble [[docs](https://docs.ros.org/en/humble/index.html)]
- **Gazebo:** Harmonic [[docs](https://gazebosim.org/docs/harmonic/getstarted/)]
- **CrazySim:** 1.2x (commit `8ad9bb8`) [[repo](https://github.com/gtfactslab/CrazySim/tree/8ad9bb8dfe8c827f349b3a224d47f7808c186d06)]

> [!NOTE]
> This repository is prepared for working with Ubuntu OS. 
> If you are using Windows, please open Ubuntu in WSL 2.
> However, you are doing this on your own risk :smile:.

## Prerequisites

First of all, before you start anything, please fork this repository and **work on your own copy**.

The best way to work with this repository is to use the prepared Docker image.
Follow the official [Docker Documentation](https://docs.docker.com/) to install the required software (note that on Linux, only the Docker Engine is required).
Also, if you have an Nvidia GPU and want to use its computing power within Docker, you should install the [Nvidia Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) (without experimental packages and rootless mode).

> [!NOTE]
> If you do not have an Nvidia GPU card, you need to modify the [devcontainer.json](.devcontainer/devcontainer.json) and set `"dockerComposeFile"` to `compose.nogpu.yaml`.

## Docker run

> [!TIP]
> In Windows, it is recommended to use WSL2 with a native Linux file system.
> Normally directories from Windows are mounted as `/mnt` inside Ubuntu, but this may cause some problems due to the NTFS file system and permissions.
> Therefore, copy repository or clone it directly into `$HOME` directory inside WSL2.

Open the project's directory in VS Code.
In the bottom left corner, click on the icon with the two arrows pointing at each other.
The menu with different options will appear at the top - choose **"Open folder in container... "** and wait, the docker will be created.
Note that this may take some time (depending on your internet connection).

Next time, you can open Docker again in the same way, but it should take considerably less time because of the cached image.

## Reposiory content

### Docker system

Inside the Docker image, all the important files are stored in the `/root` directory.
There are two directories:
1. `/root/CrazySim` - containes the [CrazySim](https://github.com/gtfactslab/CrazySim/tree/8ad9bb8dfe8c827f349b3a224d47f7808c186d06?tab=readme-ov-file) software, which serves the purpose of SITL (*Software-in-the-Loop*) simulation for CrazyFlie drones.
Internally it uses the [Gazebo](https://gazebosim.org/docs/harmonic/getstarted/) simulator.
2. `/root/ros2_ws` - containes the ROS2 workspace where you can use all the ROS2 packages you want.
Note that the `/root/ros2_ws/src` is mounted directly on the local directory and containes the entire repository.
There you also have the [evs_gz_utils](https://github.com/vision-agh/evs_gz_utils) package with some utility functions to exchange data between Gazebo and ROS2.

### How it works (if only it worked)

CrazySim consists of the two main components:
1. [crazyflie-firmware](https://github.com/llanesc/crazyflie-firmware/tree/6a4d2d006ba3c394949582c1c2eedd4b84fce17e) - this is a piece of code that normally runs on the UAV.
Here it is also responsible for running the Gazebo simulator and spawning drones in it.
2. [crazyflie-lib-python](https://github.com/llanesc/crazyflie-lib-python/tree/9f50dce2dbba7d3836a86f6965095dbb43242a07) - this is on the other side of the communication channel, usually running on the so-called 'ground station' (i.e. something that does NOT fly).
With this library you should be able to read all the data from the CrazyFlie and transmit the control signals.

> [!TIP]
> You can easily change the directory to the `/root/CrazySim` using `cd_crazysim` alias.

In order to check if everything is working correctly, firstly spawn the UAV with CrazySim:
``` bash
cd_crazysim && cd crazyflie-firmware
bash tools/crazyflie-simulation/simulator_files/gazebo/launch/sitl_singleagent.sh -m crazyflie -x 0 -y 0
```

Secondly, in the separate terminal, run the [connection_example](./connection_example.py) script.
It should prints some data that is constantly read from the CrazyFlie in the simulation.

> [!TIP]
> Read the [How to use CrazySim](https://github.com/gtfactslab/CrazySim/tree/8ad9bb8dfe8c827f349b3a224d47f7808c186d06?tab=readme-ov-file#how-to-use) to learn how to use CrazySim :smile:.

### Where is ROS?

Yup, as you can see, no ROS is needed to control the CrazyFlie inside CrazySim.
However, one of your goals is to integrate CrazySim with the ROS infrastructure to facilitate further integration with other robotics software.
Before using ROS for the first time, setup the environment with the following command:
``` bash
cd /root/ros2_ws
source ./setup.sh <id>
```
As the `<id>` argument you need to provide the `ROS_DOMAIN_ID` (integer in the range 0-101, both inclusive).
If you are working in the lab, this value must be **original**, just for you.
This way you will only see your ROS topics and will not interfere with the topics of your colleagues.

Remember that before using ROS and after significant changes made in the workspace, you need to build the entire workspace.
To do so, just envoke the [build.sh](.devcontainer/build.sh) script, which is located inside `/root/ros2_ws` directory:
``` bash
cd /root/ros2_ws
./build.sh
```

You will then need to source the `/root/ros2_ws/install/setup.bash` script to make all the changes visible, but this is already done in `.bashrc`, so all you need to do is reopen the terminal.

## Additional features

### Data exchange between Gazebo and ROS2

Natively, Gazebo and ROS have a similar internal structure with topics and services to transport data, but they are not seamlessly interoperable (e.g. different types).
However, there is an additional [ros_gz](https://github.com/gazebosim/ros_gz) package provided by Gazebo developers, which facilitates integration between Gazebo and ROS.
It is already installed in the docker, so you can use all the features you need.

For your convenience, there is also an [evs_gz_utils](./evs_gz_utils/) package in the repository.
You can read its own (not very rich - still under development) documentation to learn more.

### Rosbag

If you are running nodes inside ROS2, you can easily record all the data that is exchanged via topics.
Just use the [rosbag2](https://github.com/ros2/rosbag2) which is already installed in the docker.
Remember that you can manually select the topics you want to record and set the path where all the bags will be stored.

### PlotJuggler

If you've recorded some rosbags, you'd like to be able to read and analyse them now, wouldn't you?
Fortunately, there is a good piece of software called [PlotJuggler](https://plotjuggler.io/) that is already installed in the docker.
You can run it with the following command:

```bash
ros2 run plotjuggler plotjuggler 
```
After some random meme, you will see the main window where you can import and plot data.
Some additional functions can be found in the linked documentation.

## FAQs

### But why?

[📢 Bad joke alert]
Because you want to pass the subject and get your degree, right?

### I started the Gazebo, but simulator window did not pop up

Re-open the folder locally and give additional permissions for Docker:
``` bash
xhost +local:docker
```

Re-open the folder in the container and check that it is now working correctly.