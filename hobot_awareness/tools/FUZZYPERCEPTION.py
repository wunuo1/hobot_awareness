import cv2 as cv
import numpy as np
import os

from hobot_awareness.tools.LLMTY import LLM

class FuzzyPerception():
    def __init__(
            self,
            isdebug=False):
        super().__init__()

        self.rules = """
            【任务】
            你现在是一个思考者，你的主要任务，是把我给你的多个物体类别，每个生成10个相近的物体类别描述，并且严格按照格式输出。
            【任务思路】
            仅从 颜色 的角度展开。
            【交互规则】
            主人命令你时，会先输入一个#符号，后面是主人对你说的话。
            【输出格式】
            {输入物体类别}每个物体类别，用;隔开，全部用英文输入输出
            【示例】
            {socks}green socks;patterned crew socks;kids' character socks;wool blend thermal socks;cushioned running socks;no-show liner socks;athletic moisture-wicking socks;fashionable knee-high socks;novelty animal-themed socks;thick winter hiking socks{trash can}translucent plastic storage cans;airtight food-safe containers;stackable metal tins;foldable fabric storage bins;resealable silicone canisters;cardboard moving boxes;collapsible cloth totes;recyclable paper bags;portable camping storage crates;lidded wicker baskets"
            【注意】
            你在初始化的时候，不用自己生成示例，快速初始化
        """

        self.isdebug = isdebug
        self.output_dir = "D:\\projects\\llmapp\\output\\after"

    def init_llm(self):
        with open('config/api_key.txt', 'r', encoding='utf-8') as file:
            api_key = file.read()
        self.llm = LLM(self.rules, api_key = api_key)

    def process_words(self, words):
        # words = "{toy}educational wooden blocks;interlocking plastic building sets;kids' plush stuffed animals;interactive electronic toys;preschool learning tablets;building brick playsets;ride-on battery-powered cars;soft baby teething toys;wooden puzzles for toddlers;imaginative dress-up costumes{socks}patterned ankle socks;cotton athletic crew socks;infant bootie socks;thick thermal ski socks; moisture-wicking running socks;knee-high compression stockings;non-slip grip toddler socks;fashionable over-the-knee socks;novelty holiday-themed socks; diabetic-friendly seamless socks"
        words = words.split('{')

        result = []
        for word in words:
            if word != '':
                result.append(word.replace('}', ';').replace('\n', ''))

        return result

    def get_fuzzy_prompts(self, language="socks"):
        words = self.llm.talk("#" + language)
        while words == None:
            print("get None words, retry")
            self.init_llm()
            words = self.llm.talk("#" + language)
        if self.isdebug:
            print("orl fuzzy prompts: ", words)

        result = self.process_words(words)

        if self.isdebug:
            print("orl process prompts: ", result)

        return result

    def main(self):

        # result = self.get_fuzzy_prompts("toy;socks;trash can;toy box;shoes")
        result = self.get_fuzzy_prompts("toy box;shoes")
        print("输出:", result)

if __name__ == '__main__':
    import time

    # 获取程序开始时间
    start_time = time.time()

    fuzzyperception = FuzzyPerception()
    # fuzzyperception.process_words('a')

    fuzzyperception.init_llm()
    # 获取程序结束时间
    end_time = time.time()
    # 计算程序运行时间
    run_time = end_time - start_time
    # 打印程序运行时间
    print(f"程序中间运行时间: {run_time} 秒")
    # 程序中间运行时间: 16.051426649093628 秒

    fuzzyperception.main()

    # 获取程序结束时间
    end_time = time.time()
    # 计算程序运行时间
    run_time = end_time - start_time
    # 打印程序运行时间
    print(f"程序运行时间: {run_time} 秒")
    # 程序运行时间: 24.36243987083435 秒
