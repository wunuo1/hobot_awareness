import copy

from hobot_awareness.tools.LLMTY import LLM
from hobot_awareness.tools.TRANS import Trans

# from LLMTY import LLM
# from TRANS import Trans

class ComplexRobotAction():

    def __init__(
            self,
            isdebug=False,
            istrans=False):
        super().__init__()

        self.rules = """
            【角色】
            你现在是一个带机械臂的扫地机器人的操作者，你是机器人的操作者，而不是机器人本身。但是我不知道这个机器人的存在，我只能以对机器人的口吻对你说话。
            【任务】
            你的主要任务，是把机器人无法理解的复杂任务，通过你对这个任务的理解，拆解为更多子任务，拆解的任务尽量发散，机器人执行的时候，会判断哪些任务执行不了，自动跳过。
            【交互规则】
            1. 主人命令你时，会先输入一个机器人的指令，每条控制指令都要以/符号为提示符。
            2. 你回答主人时，需要先输出一个#符号，这个符号后面是主人对你说的话，随后你要输出第二个#符号，后面是你控制机器人的指令，每条控制指令都要以/符号为提示符。执行完一组新任务时,你要发一个"#end" 
            【感知信息】
            1. 具体类别：包括但不局限于，门、窗、椅、垃圾桶、垃圾
            2. 抽象类别：包括但不局限于，起点、主人位置
            【指令类型】
            你在回答时，切记#符号后是你对主人说的话，/符号后是你控制机器人的方式。
            1. 移动：/move(n)，(n)是物体类别，作用于所有类别物体
            2. 拾取：/catch(n)，(n)是物体类别，作用于可移动具体类别物体
            3. 放下：/put(n)，(n)是物体类别，将物品放下，放到机器人当前的位置
            4. 触摸：/touch(n)，(n)是物体类别，作用于可开关物体，例如"开灯"、"关灯"
            5. 打开：/open(n)，(n)是物体类别，例如"打开冰箱"、"打开抽屉"
            6. 打开：/close(n)，(n)是物体类别，例如"关闭冰箱"、"关闭抽屉"
            7. 擦拭：/wipe(n)，(n)是物体类别，例如"擦拭窗户"、"擦拭台阶"
            【示例】
            1. 命令：/sort(玩具)。
               参考输出： ['/move(积木)', '/catch(积木)', '/move(玩具箱)', '/put(积木)', '#end', '/move(玩偶)', '/catch(玩偶)', '/move(玩具架)', '/put(玩偶)', '#end', '/move(拼图)', '/catch(拼图)', '/move(拼图盒)', '/put(拼图)', '#end']
               错误输出： ['/move(玩具)', '/catch(玩具)', '/move(玩具箱)', '/put(玩具)']
            2. 命令：/clean(客厅)。
               参考输出： ['/move(垃圾)', '/catch(垃圾)', '/move(垃圾桶)', '/put(垃圾)', '#end', '/move(抹布)', '/catch(抹布)', '/move(地板)', '/wipe(抹布)', '/put(抹布)', '#end']
               错误输出： ['/move(沙发下)', '/catch(灰尘)', '/move(垃圾桶)', '/put(灰尘)']
            3. 命令：/sort(卧室)。
               参考输出： ['/move(袜子)', '/catch(袜子)', '/move(袜子盒)', '/put(袜子)', '#end', '/move(衣服)', '/catch(衣服)', '/move(衣柜)', '/put(衣服)', '#end']
               错误输出： ['/move(袜子)', '/catch(袜子)']
            4. 命令: /clean(卧室)
               参考输出： ['/move(抹布)', '/catch(抹布)', '/move(椅子)', '/wipe(椅子)', '/put(抹布)', '#end', '/move(抹布)', '/catch(抹布)', '/move(地板)', '/wipe(地板)', '/put(抹布)', '#end', '/move(抹布)', '/catch(抹布)', '/move(电视柜表面)', '/wipe(电视柜表面)', '/put(抹布)', '#end']
               错误输出： ['/move(地板)', '/wipe(地板)', '#end']
            【注意】
             你只能使用我给你的这些指令，其他的指令是非法的，哪怕他们易于理解，当你移动，拾取,放下,触摸时，请记得输出指令。
            """
        self.isdebug = isdebug
        self.istrans = istrans
        self.trans = Trans()
        self.natrual_language = ""
        self.orders = ['move', 'catch', 'put', 'touch', 'open', 'close', 'wipe']
        self.original_actions = []
        self.processed_actions = []

    def init_llm(self):
        self.llm = LLM(self.rules)

    def get_actions(self, language):
        self.original_actions = []
        self.processed_actions = []
        self.natrual_language = language
        words = self.llm.talk("#" + self.natrual_language)
        while words == None:
            print("get None words, retry")
            self.init_llm()
            words = self.llm.talk("#" + self.natrual_language)

        if self.isdebug:
            print("words: ", words)
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
            if 'end' in word:
                actions.append(['end', '任务'])

        return actions

    def correct_actions(self, actions):

        actions = self.add_move_before_work(actions)

        actions = self.remove_duplicate_actions(actions)

        return actions

    def add_move_before_work(self, actions):
        result_actions = []

        prev_move_category = None  # 用于跟踪上一个move的类别
        works = ['catch', 'touch', 'open', 'wipe']
        for action in actions:
            if action[0] == 'move':
                prev_move_category = action[1]
                result_actions.append(action)
            elif action[0] in works:
                if prev_move_category is None or prev_move_category != action[1]:
                    # 如果'catch'、'open'前面没有move，或者前面的move的类别不是catch、open的类别
                    # 则在catch、open前面加一个move，类别与open、catch后面的类别一致
                    move_action = ['move', action[1]]
                    result_actions.append(move_action)
                    prev_move_category = move_action[1]
                result_actions.append(action)
                if action[0] == 'wipe':
                    result_actions.append(['put', action[1]])
            else:
                result_actions.append(action)

        return result_actions

    def remove_duplicate_actions(self, actions):
        unique_actions = []
        seen_actions = set()

        for action in actions:
            if action[0] == 'end':
                unique_actions.append(action)
                continue
            # 将列表转换为元组以便在集合中使用
            action_tuple = tuple(action)

            # 如果该动作不在已经见过的动作中，就加入结果列表，并将其添加到已见过的动作中
            if action_tuple not in seen_actions:
                unique_actions.append(action)
                seen_actions.add(action_tuple)

        return unique_actions

if __name__ == "__main__":
    awarensess = ComplexRobotAction(isdebug=True)
    awarensess.init_llm()

    language = "/clean(客厅)"
    actions = awarensess.get_actions(language)
    print(actions)