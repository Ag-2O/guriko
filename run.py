import numpy as np
import csv
import os

import player.random_player as rp
import player.nash_eq_player as nep
import player.fixed_player as fp
import player.CFR_player as cfrp

import guriko
import matplotlib.pyplot as plt

#変数はアンダーバー、関数は大文字でつなげて

actions = [9,2,4]
#player0 = rp.RandomPlayer(pid=0,actions=actions)
#player1 = rp.RandomPlayer(pid=1,actions=actions)
#player2 = rp.RandomPlayer(pid=2,actions=actions)
#player0 = nep.NashEqPlayer(pid=0,actions=actions)
#player1 = nep.NashEqPlayer(pid=1,actions=actions)
#player2 = nep.NashEqPlayer(pid=2,actions=actions)
#player2 = fp.FixedPlayer(pid=2,actions=actions)
player1 = fp.FixedPlayer(pid=1,actions=actions)
#player0 = fp.FixedPlayer(pid=0,actions=actions)
player0 = cfrp.CFRPlayer(pid=0,actions=actions,training=False)
#player1 = cfrp.CFRPlayer(pid=1,actions=actions)

#players = [player0,player1,player2]
players = [player0,player1]

result0 = []
result1 = []
result2 = []
horizontal = []
    
nb_episode = 1000
win_sum = [0,0,0]
for episode in range(nb_episode):
    game = guriko.Guriko(players)

    player_pos = game.GetPlayerPos()
    #game.PrintMap()
    is_goal = 0
    is_rsp = 0

    step_num = 0
    while is_goal == 0:
        is_rsp = 0
        while is_rsp == 0:
            is_rsp, actions = game.RSP(players)
        
        #print("actions",actions)
        is_goal,winer = game.Step(actions)
        player0.observe(opponent_action=actions[1],is_goal=is_goal,winer=winer)
        player1.observe(opponent_action=actions[0],is_goal=is_goal,winer=winer)

        #game.PrintMap()
        #print("step : ",step_num)
        step_num += 1
    game.WinCount(win_sum,winer)
    
    result0.append(win_sum[0])
    result1.append(win_sum[1])
    result2.append(win_sum[2])
    horizontal.append(episode)

print("勝利の合計",win_sum,"/対戦回数",nb_episode)

plt.plot(horizontal,result0,color='red')
plt.plot(horizontal,result1,color='blue')
#plt.plot(horizontal,result2,color='green')
plt.xlabel("Episodes")
plt.ylabel("win")
plt.legend()
plt.show()
