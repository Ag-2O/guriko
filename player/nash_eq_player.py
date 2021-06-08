import random

class NashEqPlayer:
    def __init__(self,pid,actions=None):
        #行動
        self.actions = actions
        #id
        self.pid = pid
    
    def act(self):
        #ナッシュ均衡戦略に従って行動
        strategy = [0.25,0.5,0.25]
        rand_value = random.uniform(0,1)
        if strategy[0] > rand_value:
            return self.actions[0]
        elif strategy[0]+strategy[1] > rand_value and strategy[0] <= rand_value:
            return self.actions[1]
        else:
            return self.actions[2]
    
    #観測のスキップ
    def observe(self,next_state=None,reward=None,opponent_action=None,is_goal=0,winer=None):
        pass