import random

class RandomPlayer:
    def __init__(self,pid,actions=None):
        #行動
        self.actions = actions
        #id
        self.pid = pid
    
    #ランダムに行動
    def act(self):
        return random.choice(self.actions)
    
    #観測のスキップ
    def observe(self,next_state=None,reward=None,opponent_action=None,is_goal=0,winer=None):
        pass