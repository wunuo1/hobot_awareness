import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.executors import MultiThreadedExecutor

from robot_pick_obj_msg.srv import TaskExecution
import threading
from hobot_awareness.tools.ACTION import RobotAction
from hobot_awareness.tools.COMPLEX_ACTION import ComplexRobotAction
from hobot_awareness.tools.FUZZYPERCEPTION import FuzzyPerception

class LLMBrainer(Node):

    def __init__(self, isInitBegin=True, isComplex=True, isFuzzy=True, isRetry=True, isRepeat=False):
        super().__init__('LLMBrainer')


        self.client = self.create_client(TaskExecution, 'task')
        
        self.robotaction = RobotAction(isdebug=False, istrans=True)
        self.complex_robotaction = ComplexRobotAction(isdebug=False, istrans=True)
        self.fuzzy_perception = FuzzyPerception(isdebug=False)
        self.isInitBegin = isInitBegin
        self.isComplex = isComplex
        self.isFuzzy = isFuzzy
        self.isRetry = isRetry
        self.isRepeat = isRepeat
        self.RetryTime = 0


        self.start_time = time.time()
        if self.isInitBegin:
            self.robotaction.init_llm()
        if self.isComplex:
            self.complex_robotaction.init_llm()
        if self.isFuzzy:
            self.fuzzy_perception.init_llm()
        run_time = time.time() - self.start_time
        print(f"大模型初始化共计用时: {run_time} 秒")

        self.actions = []

        self.get_logger().info('LLMBrainer Node has been initialized.')


    def do_action_groups(self, action):
        # for actions in self.action_groups:
        request = TaskExecution.Request()
        request.target_type = action[1]
        request.task_type = action[0]
        print(request.target_type)
        self.future = self.client.call_async(request)

    def run_node(self):
        start_time = time.time()

        if not self.isInitBegin:
            self.robotaction.init_llm()
        language = input("你：")

        start_time = time.time()

        if language == "exit":
            return 
        actions = self.robotaction.get_actions(language)
        print(actions)
        run_time = time.time() - start_time
        print(f"指令一级拆解耗时: {run_time} 秒")
        # actions = [['move', 'socks'], ['sort', 'toy']]

        if self.isFuzzy:
            actions = self.add_fuzzy_objs(actions)
        run_time = time.time() - start_time
        print(f"感知大模型发散提示词生成耗时: {run_time} 秒")

        self.action_groups = self.split_action_groups(actions)
        
        for actions in self.action_groups:
            print("actions: ", actions, '\n')

        run_time = time.time() - start_time
        print(f"大模型共计推理耗时: {run_time} 秒")

    def split_action_groups(self, actions):
        result = []
        current_sublist = []

        for action in actions:
            result.append(action)
        return result

    def add_fuzzy_objs(self, actions):
        for action in actions:
            if action[0] == 'set':
                objs = action[1]
                combine_str = ';'.join(action[1])
                prompts = self.fuzzy_perception.get_fuzzy_prompts(combine_str)
                newobjs = []

                print("objs: ", objs)
                if len(objs) != len(prompts):
                    print(f"fuzzy 生成的prompt长度与objs不一致, objs: {len(objs)}, prompts: {len(prompts)}")
                for i in range(len(prompts)):
                    obj = prompts[i]
                    newobjs.append(obj)
                action[1] = newobjs
                return actions
        return actions

def main(args=None):
    rclpy.init(args=args)
    llm_brainer = LLMBrainer(isInitBegin=True, isComplex=False, isFuzzy=True)
    while rclpy.ok():
        llm_brainer.run_node()
        for action in llm_brainer.action_groups:
            llm_brainer.do_action_groups(action)
            while rclpy.ok():
                rclpy.spin_once(llm_brainer)
                if llm_brainer.future.done():
                    print(llm_brainer.future.result().successful)
                    break


    llm_brainer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()