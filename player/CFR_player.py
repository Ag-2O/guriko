import random
import numpy as np
import csv
import os

class CFRPlayer:
    def __init__(self,pid,actions=None,training=True):
        self.actions = actions
        self.pid = pid
        #行動選択の履歴
        self.history = ""
        #選択した行動
        self.select_action = 0
        #トレーニングするかどうか
        self.training = training
        #戦略
        self.strategy = {}
        #戦略をCSVファイルから読み込またい

        #利得
        self.reward = 0

        #戦略ファイルを開く
        if training == False:
            f = os.path.join(os.path.dirname(__file__),"../strategy/6step_500000times.csv")
            self.strategy = self.read_data(f)

        count = 0
        for his,stg in self.strategy.items():
            print("history:",f"{his:20}","strategy: ",stg)
            count += 1

        print("Infomation_num: ",count)
    
    def act(self):
        #初めて到達する部分なら
        if self.history not in self.strategy:
            self.strategy[self.history] = np.array([1.0/3]*3)

        #現在のもつ戦略からボルツマン選択
        sum_val = 0
        rng = []
        for index in self.strategy[self.history]:
            rng.append(index)
            sum_val += index
        #print("rng",rng)
        
        rand = random.uniform(0,sum_val)

        if rand <= rng[0]:
            self.select_action = self.actions[0]
        elif rng[0] < rand and rand <= rng[1] + rng[0]:
            self.select_action = self.actions[1]
        else:
            self.select_action = self.actions[2]

        return self.select_action
    
    def observe(self,next_state=None,reward=None,opponent_action=None,is_goal=0,winer=None):
        #履歴に自分の行動と相手の行動を追加(文字列)
        self.history += str(self.select_action) + str(opponent_action)+"."     
        
        if is_goal == 1:
            self.history = ""
    
    def read_data(self,file):
        with open(file,newline="") as f:
            read_dict = csv.DictReader(f,delimiter=",",quotechar='"')
            ks = read_dict.fieldnames
            return_dict = {k:[] for k in ks}

            for row in read_dict:
                for k,v in row.items():
                    return_dict[k].append(float(v))
            
            for v in read_dict:
                return_dict[v] = np.array(return_dict[v])
        return return_dict

    

    

        