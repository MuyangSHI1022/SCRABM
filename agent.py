import numpy as np
import numpy.random as rnd
import math

#随机赋各项权重，后期可以根据结果具体进行调参
# alpha_D = 0.5
# alpha_P = 0.2
# alpha_S = 0.05

alpha_D = rnd.random()
alpha_P = rnd.random()
alpha_S = rnd.random()

x_policy = [1]
y_policy = [10]


class Leader: 
    def __init__(self, traits, status, influence, risk, rationality):
        self.traits = traits  #智能体特性 [对政策x的偏好，对政策y的偏好，对政策x的显著性权重，对政策y的显著性权重]
        self.status = status  #智能体身份分类：Tier1, Tier2, Tier3（根据权力大小分类）
        self.influence = influence #智能体权力，[i_power, r_power] Tier1:[low, high] Tier2:[normal,normal] Tier3:[high,low]
        self.risk = risk #0,1=['RAO','RTO']
        self.rationality = rationality #0,1=['low','high']
        #actions, heuristics, constraints
        self.preference = [self.traits[0], self.traits[1]]
        self.salience_issue = [self.traits[2], self.traits[3]]

    #计算领导人的效用函数
    def distance_preference_policy(self, x_pol, y_pol):
        x = self.traits[0] - x_pol[0]
        y = self.traits[1] - y_pol[0]
        D = math.sqrt(self.traits[2] * x**2 + self.traits[3] * y**2) 
        return D
    def power_total(self):
        P = self.influence[0] + self.influence[1]
        return P
    def support_aggregate(self, Tier1, Tier2, Tier3, x_pol, y_pol):
        x = self.preference[0] - x_pol[0]
        y = self.preference[1] - y_pol[0]
        S = math.sqrt(self.influence[0] * (10-x)**2 + self.influence[1] * (10-y)**2) 
        S_tiers = 0
        for i in range(len(Tier1)):
            S_tiers += Tier1[i].support()
        for j in range(len(Tier2)):
            S_tiers += Tier2[j].support()
        for k in range(len(Tier3)):
            S_tiers += Tier3[k].support()
        S_total = 0.01*S + S_tiers
        return S_total

    #重新分配权力
    #要么将其中一个agent撤职并换成另一个agent
    def fire_and_hire(self, Tier_fire, Tier_hire):
        Tier_fire.status = 3
        Tier_fire.influence[0] = rnd.uniform(0.67,1)
        Tier_fire.influence[1] = rnd.uniform(0,0.33)

        Tier_hire.status = 2
        Tier_hire.influence[0] = rnd.uniform(0.33, 0.67)
        Tier_hire.influence[1] = rnd.uniform(0.33, 0.67)

    
    #新继任者上位替换旧领导人
    def sucession(self, scenario):
        if scenario == 'A':
            self.risk = 1
            self.rationality = 1
        elif scenario == 'B':
            self.risk = 1
            self.rationality = 0
        else:
            self.risk = 0
            self.rationality = 1
    

class Tier:
    def __init__(self, number, traits, status, influence):
        self.number = number
        self.traits = traits
        self.status = status
        self.influence = influence 
        self.preference = [self.traits[0], self.traits[1]]
        self.salience_issue = [self.traits[2], self.traits[3]]
    
    def power_total(self):
        P = self.influence[0] + self.influence[1]
        return P

    #计算普通agent的效用函数
    def U_A(self):
        x = self.preference[0] - x_policy[0]
        y = self.preference[1] - y_policy[0]
        D = math.sqrt(self.salience_issue[0] * x**2 + self.salience_issue[1] * y**2) 
        P = self.influence[0] + self.influence[1]
        return alpha_D * (D) + alpha_P * P
    
    #计算agent自身对当前政权政策的支持
    def support(self):
        x = self.preference[0] - x_policy[0]
        y = self.preference[1] - y_policy[0]
        support = math.sqrt(self.influence[0] * (10-x)**2 + self.influence[1] * (10-y)**2) 
        return support
    
    #外部冲击以一定概率改变i_power
    def shock(self):
        p = rnd.random()
        if p > 0.5:
            value = rnd.uniform(0, 0.02)
            if self.influence[0] - value > 0:
                self.influence[0] -= value
        else:
            self.influence[0] += rnd.uniform(0, 0.02)

