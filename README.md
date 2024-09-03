# hobot_awareness
# Feature Introduction

This package utilizes the Tongyi Qianwen API to decompose input text into tasks and send requests.

# Usage Instructions

## Preparations

1. Have the RDK suite ready and running properly.
2. Obtain an API KEY from Tongyi Qianwen and replace the `api_key` in the config file.

## Compile and Runs

**1. Compile**

After starting the robot, connect to it via SSH or VNC on the terminal, open the terminal, pull the corresponding code, and compile and install it.

```bash
# Pull task disassembly code
mkdir -p ~/tonypi_ws/src && cd ~/tonypi_ws/src
git clone https://github.com/wunuo1/hobot_awareness.git

# Compile
cd ..
source /opt/tros/setup.bash
colcon build
```
**2. Run the Task Decomposition Function**

```shell
source ~/tonypi_ws/install/setup.bash
cp -r /opt/tros/lib/hobot_awareness/config/ .
# After running, enter the task description in the terminal, for example: put the green ball on the base
ros2 run hobot_awareness hobot_awareness
```

# Interface Description

## Services

### Send Request

|Name  | Type                                  |  Description           |
|------| --------------------------------------| --------------------------------|
|/task |robot_pick_obj_msg::srv::TaskExecution | Receives task execution, performs actions + targets。Request：string target_type string task_type ； Response：bool successful|