# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
import json
from hashlib import md5

class Trans:
    def __init__(self):

        # Set your own appid/appkey.
        self.appid = '20240118001944834'
        self.appkey = 'bhprCuMYbvp9H4C8A5a7'

        self.from_lang = 'zh'
        self.to_lang =  'en'

        endpoint = 'http://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        self.url = endpoint + path

    # Generate salt and sign
    def make_md5(self, s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    def do(self, query):
        salt = random.randint(32768, 65536)
        sign = self.make_md5(self.appid + query + str(salt) + self.appkey)

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': self.appid, 'q': query, 'from': self.from_lang, 'to': self.to_lang, 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(self.url, params=payload, headers=headers)
        result = r.json()

        if 'error_code' in result:
            print("error_code: ", result["error_code"])
            return query
        # Show response
        # print(json.dumps(result, indent=4, ensure_ascii=False))
        results = []
        for res in result["trans_result"]:
            results.append(res["dst"].lower())

        return results

    def doactions(self, actions):
        queue = ''
        for action in actions:
            queue += action[1] + '\n'
        res = self.do(queue)
        new_actions = []
        for i in range(len(actions)):
            order = actions[i][0]
            obj = res[i]
            new_actions.append([order, obj])
        return new_actions

    # 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'

if __name__ == '__main__':
    trans = Trans()
    actions = [['move', '桌'], ['catch', '杯'], ['move', '起点']]

    actions = trans.doactions(actions)
    print(actions)

    # res = trans.do("门")
    # print("result: ", res)