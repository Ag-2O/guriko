import numpy as np
import player.random_player as rp
import player.nash_eq_player as nep
import player.fixed_player as fp
import guriko

actions = [9,2,4]
player0 = nep.NashEqPlayer(pid=0,actions=actions)
player1 = nep.NashEqPlayer(pid=1,actions=actions)
players = [player0,player1]

nb_episode = 1

for episode in range(nb_episode):
    game = guriko.Guriko(players)

    player_pos = game.GetPlayerPos()
    #game.PrintMap()
    is_goal = 0
    is_rsp = 0

    step_num = 0
    
    for i, p0_action in enumerate(actions):
        for t, p1_action in enumerate(actions):
            each_actions = [p0_action,p1_action]
            print("each_actions:",each_actions)
            is_rsp = 0
            is_rsp,winer = game.CFR_RSP(each_actions)

            if is_rsp == 0:
                print("あいこ")
            else:
                print("勝者は:",winer)
