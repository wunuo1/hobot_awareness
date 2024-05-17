import dashscope

from http import HTTPStatus
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role

import re

class LLM:
    def __init__(
            self,
            rules,
            api_key):
        self.api_key = api_key
        dashscope.api_key = self.api_key  # 通义千问API
        self.rules = rules  # 通义千问规则，设定机器人身份

        self.messages = [{'role': Role.SYSTEM, 'content': self.rules},
                    {'role': Role.USER, 'content': self.rules}]
        # 执行第一条对话并打印结果
        self.first_conversation()
    def first_conversation(self):
        response = Generation.call(
            # model='qwen-max-longcontext',
            Generation.Models.qwen_max,
            messages=self.messages,
            result_format='message',  # set the result to be "message" format.
        )
        if response.status_code == HTTPStatus.OK:
            print(response["output"]["choices"][0]["message"]["content"])
            # append result to messages.
            self.messages.append({'role': response.output.choices[0]['message']['role'],
                            'content': response.output.choices[0]['message']['content']})
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
    def talk(self, natrual_language):
        self.messages.append({'role': Role.USER, 'content': natrual_language})
        # make second round call
        response = Generation.call(
            # model='qwen-max-longcontext',
            Generation.Models.qwen_max,
            messages=self.messages,
            result_format='message',  # set the result to be "message" format.
        )
        if response.status_code == HTTPStatus.OK:
            return(response["output"]["choices"][0]["message"]["content"])
            print(response["output"]["choices"][0]["message"]["content"])
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
    def convert_split(self, input_string):
        # 提取所有以 '#' 开头并以空格结尾的子串
        return re.findall(r"#(.+?)\s", input_string), re.findall(r"/(.+?)\s", input_string)