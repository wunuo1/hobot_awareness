import copy

from hobot_awareness.tools.LLMTY import LLM
from hobot_awareness.tools.TRANS import Trans

class RobotAction():

    def __init__(
            self,
            isdebug=False,
            istrans=False):
        super().__init__()

        with open('config/rules.txt', 'r', encoding='utf-8') as file:
            rules = file.read()
        self.rules = rules
        self.isdebug = isdebug
        self.istrans = istrans
        self.trans = Trans()
        self.natrual_language = ""
        self.orders = ['catch', 'put']
        self.original_actions = []
        self.processed_actions = []

    def init_llm(self):
        with open('config/api_key.txt', 'r', encoding='utf-8') as file:
            api_key = file.read()
        self.llm = LLM(self.rules, api_key= api_key)

    def get_actions(self, language):
        self.original_actions = []
        self.processed_actions = []
        self.natrual_language = language
        words = self.llm.talk("#" + self.natrual_language)
        while words == None:
            print("get None words, retry")
            self.init_llm()
            words = self.llm.talk("#" + self.natrual_language)

        words = words.replace("\n", "").split("/")
        actions = self.process_words(words)
        self.original_actions = copy.deepcopy(actions)

        if actions == None:
            print("wrong input, please re input, get words: ", words)
            return None, None

        if self.isdebug:
            print("before correct: ", actions)

        actions = self.correct_actions(actions)
        self.processed_actions = copy.deepcopy(actions)

        if self.isdebug:
            print("after correct: ", actions)

        return actions

    def check_orders(self, word):
        for order in self.orders:
            if order in word:
                return order
        return None

    def process_words(self, words):
        actions = []
        for word in words:
            if word == "" or "已" in word:
                print("pass word: ", word)
                continue

            order = self.check_orders(word)
            if order != None:
                if len(word.split('(')) == 1:
                    obj = word.split(' ')[1]
                else:
                    obj = word.split('(')[1].split(')')[0]

                if obj == '':
                    continue

                obj = obj.replace('位置', '')

                if self.isdebug:
                    print("指令：\033[32m" + word + "\033[0m")
                actions.append([order, obj])
            else:
                if self.isdebug:
                    print("RoBot: " + word.replace("#", ""))

        return actions

    def correct_actions(self, actions):

        # actions = self.add_move_before_work(actions)

        actions = self.remove_duplicate_actions(actions)

        return actions

    # def add_move_before_work(self, actions):
    #     result_actions = []

    #     prev_move_category = None  # 用于跟踪上一个move的类别
    #     works = ['catch', 'touch', 'open', 'wipe']
    #     for action in actions:
    #         if action[0] == 'move':
    #             prev_move_category = action[1]
    #             result_actions.append(action)
    #         elif action[0] in works:
    #             if prev_move_category is None or prev_move_category != action[1]:
    #                 # 如果'catch'、'open'前面没有move，或者前面的move的类别不是catch、open的类别
    #                 # 则在catch、open前面加一个move，类别与open、catch后面的类别一致
    #                 move_action = ['move', action[1]]
    #                 result_actions.append(move_action)
    #                 prev_move_category = move_action[1]
    #             result_actions.append(action)
    #             if action[0] == 'wipe':
    #                 result_actions.append(['put', action[1]])
    #         else:
    #             result_actions.append(action)

    #     return result_actions

    def remove_duplicate_actions(self, actions):
        unique_actions = []
        seen_actions = set()

        for action in actions:
            # 将列表转换为元组以便在集合中使用
            action_tuple = tuple(action)

            # 如果该动作不在已经见过的动作中，就加入结果列表，并将其添加到已见过的动作中
            if action_tuple not in seen_actions:
                unique_actions.append(action)
                seen_actions.add(action_tuple)

        return unique_actions

    def prepare_before_work(self, actions, isget=True):
        if self.istrans:
            actions = self.trans.doactions(actions)

        objs = []
        abstract_objs = []
        for action in actions:
            if action[0] in ["start", "end"]:
                continue
            elif action[1] in ["master"] and action[1] not in abstract_objs:
                abstract_objs.append(action[1])
            elif action[1] not in objs:
                objs.append(action[1])

        if isget and abstract_objs != []:
            actions.insert(0, ["get", abstract_objs[0]])
        if objs != []:
            actions.insert(0, ["set", objs])

        return actions

if __name__ == "__main__":
    awarensess = RobotAction(isdebug=True, istrans=True)
    awarensess.init_llm()

    # language = "去拿一块抹布，去放到我这里"
    language = input("你：")

    actions = awarensess.get_actions(language)
    actions = awarensess.prepare_before_work(actions)
    print(actions)
