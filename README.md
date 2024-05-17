# hobot_awareness
# Feature Introduction

This package utilizes the Tongyi Qianwen API to decompose input text into tasks and send requests.

# Usage Instructions

## Preparations

1. Have the RDK suite ready and running properly.
2. Obtain an API KEY from Tongyi Qianwen and replace the `api_key` in the config file.

## Installing the Package

**1. Install the package**

After starting the robot, connect to the robot via terminal SSH or VNC, click the "One-Click Deployment" button at the top right of this page, and copy the following command to run on the RDK system to complete the installation of the relevant Node.

```bash
sudo apt update
sudo apt install -y tros-hobot-awareness
```
**2. Run the Task Decomposition Function**

```shell
source /opt/tros/local_setup.bash
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