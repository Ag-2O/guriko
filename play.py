import numpy as np
import player.random_player as rp
import player.nash_eq_player as nep
import player.fixed_player as fp
import guriko

#変数はアンダーバー、関数は大文字でつなげて

actions = [9,2,4]
player0 = rp.RandomPlayer(pid=0,actions=actions)
player1 = rp.RandomPlayer(pid=1,actions=actions)
player2 = nep.NashEqPlayer(pid=2,actions=actions)
players = [player0,player1,player2]

#player2 = nep.NashEqPlayer(pid=2,actions=actions)
#player2 = fp.FixedPlayer(pid=2,actions=actions)

game = guriko.Guriko(players)

result = []

player_pos = game.GetPlayerPos()
game.PrintMap()
is_goal = 0
is_rsp = 0

#じゃんけん
def RSP(players):
    for player in players:
        action = player.act()
        actions.append(action)
    return game.RSPJudge(actions), actions

step_num = 0
while is_goal == 0:
    is_rsp = 0
    while is_rsp == 0:
        actions = []
        is_rsp, actions = RSP(players)
    
    is_goal,winer = game.Step(actions)

    game.PrintMap()
    print("step : ",step_num)
    step_num += 1