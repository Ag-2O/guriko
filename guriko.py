import numpy as np

#表示用
ACTIONS = {
    "Rock"      : 9,
    "Scissors"  : 2,
    "Paper"     : 4
}

#グリコゲーム
class Guriko:
    def __init__(self,players):
        #goal地点
        self.goal = 6
        self.players = players
        #playersの位置
        self.players_pos = [0,0]

        #各playerにおいて
        for player in self.players:
            #pos <- 初期位置
            self.players_pos[player.pid] = 0
    
    def Step(self,actions):
        #勝者が進む
        for wid in self.RSPwiner:
            if actions[wid] == 9:
                self.players_pos[wid] += 3
            elif actions[wid] == 2:
                self.players_pos[wid] += 6
            elif actions[wid] == 4:
                self.players_pos[wid] += 6
            else:
                print("error")
        
        #ゴール判定
        is_goal,game_winer,_reward = self.GoalJudge()
        if is_goal == 1:
            """
            for pid in game_winer:
                print("グリコの勝者はPlayer",pid)
            """
            return is_goal,game_winer

        return is_goal,game_winer


    def RSPJudge(self,actions):
        RSPsum = 0
        #winerの初期化
        self.RSPwiner = []

        for pid,action in enumerate(actions):
            #論理和
            RSPsum |= action
        
        Judge = (RSPsum & RSPsum >> 1)

        #あいこ
        if Judge == 7 or Judge == 0:
            return 0
        #勝ち負け判定
        else:
            for pid,action in enumerate(actions):
                #Trueなら勝利,論理積
                if self.BitCount(actions[pid] & Judge) == 1:
                    self.RSPwiner.append(pid)
            return 1
    
    def BitCount(self,value):
        #ビットが1の数をカウント
        return bin(value).count("1")
    
    def GoalJudge(self):
        #ゴール判定
        is_goal = 0
        game_winer = []
        reward = 0
        for player in self.players:
            if self.players_pos[player.pid] >= self.goal:
                game_winer.append(player.pid)
                is_goal = 1
                reward = 1
        return is_goal,game_winer,reward
    
    def PrintMap(self):
        #現在位置の表示
        all_pos = [["0"]*(self.goal + 1) for i in range(len(self.players))]

        for pid, pos in enumerate(self.players_pos):
            if pos >= self.goal:
                pos = self.goal
            all_pos[pid][pos] = "P"
            print(all_pos[pid])
    
    def GetPlayerPos(self):
        #playerの位置
        return self.players_pos
    
    def GetKeyFromValue(self,dic,val):
        return [k for k,v in dic.items() if v == val]
    
    #じゃんけん
    def RSP(self,players):
        actions = []
        for player in players:
            action = player.act()
            actions.append(action)
        return self.RSPJudge(actions), actions

    #勝利数の合計
    def WinCount(self,win_sum,winer):
        for wid in winer:
            if wid == 0:
                win_sum[0] += 1
            elif wid == 1:
                win_sum[1] += 1
            else:
                win_sum[2] += 1
        return win_sum[0],win_sum[1],win_sum[2]
    
    def CFR_RSP(self,each_actions):
        return self.RSPJudge(each_actions)
