# 功能介绍

该功能包通过调用通义千问的API，将输入的文本进行任务拆解，并发送请求

# 使用方法

## 准备工作

1. 具备RDK套件，并且能够正常运行。
2. 已申请通义千问的API KEY，并替换config文件中的api_key

## 安装功能包

**1.安装功能包**

启动机器人后，通过终端SSH或者VNC连接机器人，点击本页面右上方的“一键部署”按钮，复制如下命令在RDK的系统上运行，完成相关Node的安装。

```bash
sudo apt update
sudo apt install -y tros-hobot-awareness
```

**2.运行任务拆解功能**

```shell
source /opt/tros/local_setup.bash
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