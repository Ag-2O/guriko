import numpy as np
import sys
import csv
import os
import copy
import matplotlib.pyplot as plt
import time
import datetime

import guriko
import player.random_player as rp
import player.nash_eq_player as nep
import player.fixed_player as fp
import player.CFR_player as cfrp

#情報セット
class information_set():
    def __init__(self):
        #累積後悔
        self.cumulative_regrets = np.zeros(shape=3)
        #累積戦略
        self.strategy_sum = np.zeros(shape=3)
        #行動の数
        self.num_actions = 3
    
    def normalize(self,strategy:np.array):
        if sum(strategy) > 0:
            strategy /= sum(strategy)
        else:
            #戦略の合計が0以下の時
            strategy = np.array([1.0 / self.num_actions]*self.num_actions)
        return strategy
    
    def get_strategy(self,reach_probability:float):
        #後悔が負の時、０へ
        strategy = list(np.maximum(0,self.cumulative_regrets))
        strategy = self.normalize(strategy)
        self.strategy_sum += strategy * reach_probability 
        return strategy
    
    def get_average_strategy(self):
        cp_ss = copy.copy(self.strategy_sum)
        return self.normalize(cp_ss)

#CFRトレーニング
class CFRTrainer():
    def __init__(self):
        self.infoset_map = {}
        self.state = []
    
    def get_information_set(self,history):
        if history not in self.infoset_map:
            #情報セットが存在しない場合
            self.infoset_map[history] = information_set()
        return self.infoset_map[history]
    
    def cfr(self,
            actions: list,      #行動（グーチョキパー）
            history : str,      #履歴
            reach_probabilities : np.array, #到達確率
            active_player_id : int,         #現在のプレイヤーid
            game_copy : guriko, #ゲームのコピー
            real=0,
            action_0=None, 
            is_rsp=1
            ):

        #敵のid
        if active_player_id == 0:
            opponent_id = 1
        else:
            opponent_id = 0

        #ゴール状態かどうか
        is_goal,game_winer,reward = game_copy.GoalJudge()
        if is_goal == 1:
            if active_player_id in game_winer:
                return reward
            else:
                return -reward
        
        #あいこ状態であるか
        if is_rsp == 0:
            return 0
        
        #情報セットの作成、戦略の取得
        info_set = self.get_information_set(history)
        strategy = info_set.get_strategy(reach_probabilities[active_player_id])
        
        counterfactual_value = np.zeros(len(actions))

    
        for index, action in enumerate(actions):
            #ゲームのコピー
            game_copy2 = copy.deepcopy(game_copy)

            #行動選択確率
            actions_probability = strategy[index]

            #加算する履歴
            add_his = ""

            if active_player_id == 1:
                #お互いの行動list
                action_1 = action
                each_actions = [action_0,action_1]

                #じゃんけんの実行
                is_rsp = 0            
                is_rsp = game_copy2.CFR_RSP(each_actions)
            
                #あいこなら
                if is_rsp == 0:
                    pass
                else:
                    #行動の実行
                    is_goal,_winer = game_copy2.Step(each_actions)

                    #履歴更新
                    add_his = str(each_actions[0])+str(each_actions[1])+"."
            
            else:
                action_0 = action
            
            #状態の到達確率
            new_reach_probabilities = copy.deepcopy(reach_probabilities)
            new_reach_probabilities[active_player_id] *= actions_probability

            #cfrの再帰
            counterfactual_value[index] =  - self.cfr(
                                                    actions=actions,
                                                    history=history+add_his,
                                                    reach_probabilities=new_reach_probabilities,
                                                    active_player_id=opponent_id,
                                                    game_copy=game_copy2,
                                                    real=1,
                                                    action_0=action_0,
                                                    is_rsp = is_rsp
                                                    )

        #現在のゲームの状態は、行動確率によって重みづけされたcounterfactual_value
        node_value = counterfactual_value.dot(strategy)
        #print("counterfactual_value: ",counterfactual_value)
        #print("node_value:",node_value)

        for index, action in enumerate(actions):
            #累積後悔に 到達確率*(cf値-ノードの値)
            info_set.cumulative_regrets[index] += reach_probabilities[opponent_id] * (counterfactual_value[index] - node_value)
        
        return node_value
    
    def train(self,num_iterations : int):
        #プレイヤーの定義など
        guriko_actions = [9,2,4]
        player0 = cfrp.CFRPlayer(pid=0,actions=guriko_actions)
        player1 = cfrp.CFRPlayer(pid=1,actions=guriko_actions)
        players = [player0,player1]

        util = 0

        for i in range(num_iterations):
            game = guriko.Guriko(players)
            history=''
            reach_probabilities = np.ones(2)
            util += self.cfr(actions=guriko_actions,
                             history=history,
                             reach_probabilities=reach_probabilities,
                             active_player_id=0,
                             game_copy=game,
                            )
            
            print("iterations : ",i)

        return util

def save_data(history_strategy):
    now = datetime.datetime.now()
    filename = "./data/"+now.strftime('%Y_%m%d_%H%M%S')+".csv"
    hs_row = {}
    file = os.path.join(os.path.dirname(__file__),filename)

    with open(file,"w") as f:
        writer = csv.DictWriter(f,fieldnames=history_strategy.keys(),delimiter=",",quotechar='"')
        writer.writeheader()
        k1 = list(history_strategy.keys())[0]
        length = len(history_strategy[k1])

        for i in range(length):
            for k, vs in history_strategy.items():
                hs_row[k]  = vs[i]
            writer.writerow(hs_row)

if __name__=="__main__":
    #指数表記させない
    np.set_printoptions(suppress=True)

    if len(sys.argv) < 2:
        num_iterations = 100000
    else:
        num_iterations = int(sys.argv[1])
    
    cfr_trainer = CFRTrainer()
    util = cfr_trainer.train(num_iterations)

    print("--------------------result--------------------")
    print("9:Rock,2:Scissors,4:Paper","               ","   Rock   "," Scissors  ","  Paper   ")

    history_strategy = {}
    for name, info_set in sorted(cfr_trainer.infoset_map.items(),key=lambda s: len(s[0])):
        print("history:",f"{name:20}"," strategy:",info_set.get_average_strategy())
        history_strategy.update([(name,info_set.get_average_strategy())])

    print("平均利得",(util / num_iterations))
    print("----------------------------------------------")
    save_data(history_strategy)
