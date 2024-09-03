# 功能介绍

该功能包通过调用通义千问的API，将输入的文本进行任务拆解，并发送请求

# 使用方法

## 准备工作

1. 具备RDK套件，并且能够正常运行。
2. 已申请通义千问的API KEY，并替换config文件中的api_key

## 编译与运行

**1.编译**

启动机器人后，通过终端SSH或者VNC连接机器人，打开终端拉取相应代码并编译安装


```bash
# 任务拆解代码
mkdir -p ~/tonypi_ws/src && cd ~/tonypi_ws/src
git clone https://github.com/wunuo1/hobot_awareness.git

# 编译
cd ..
source /opt/tros/setup.bash
colcon build
```

**2.运行任务拆解功能**

```shell
source ~/tonypi_ws/install/setup.bash
cp -r /opt/tros/lib/hobot_awareness/config/ .
# 运行后，在终端输入任务描述，比如：把绿球放到圆盘里
ros2 run hobot_awareness hobot_awareness
```


# 接口说明

## 服务

### 发送请求

|名称  | 类型                                    | 说明            |
|------| -------------------------------------------| --------------------------------|
|/task |robot_pick_obj_msg::srv::TaskExecution      | 接收执行任务，执行动作+目标。请求：string target_type string task_type ；回复：bool successful|