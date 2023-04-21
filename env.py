import numpy.random as rnd
from agent import *
from utils import *
import sys 
sys.setrecursionlimit(1000000000)

'''实验1开始, 初始化一些变量'''
#智能体特性 [对政策x的偏好，对政策y的偏好，对政策x的显著性权重，对政策y的显著性权重]
alpha_x = rnd.random()
alpha_y = rnd.random()
#实例化：{1个leader}, {2个tier1，3个tier(formal positions)，5个tier3(elites)}
leader = Leader([10, 10, alpha_x, alpha_y], 1, [1,1], 0, 1)

tier1_1 = Tier(1, [rnd.uniform(6,9), rnd.uniform(6,9), rnd.random(), rnd.random()], 1, [rnd.uniform(0, 0.33), rnd.uniform(0.67, 1)])
tier1_2 = Tier(2, [rnd.uniform(6,9), rnd.uniform(6,9), rnd.random(), rnd.random()], 1, [rnd.uniform(0, 0.33), rnd.uniform(0.67, 1)])

#实验2
# leader = Leader([10, 10, rnd.random(), rnd.random()], 1, [2,1], 0, 1)
# tier1_1 = Tier(1, [rnd.uniform(6,9), rnd.uniform(6,9), rnd.random(), rnd.random()], 1, [1, 0.5])
# tier1_2 = Tier(2, [rnd.uniform(6,9), rnd.uniform(6,9), rnd.random(), rnd.random()], 1, [1, 0.5])

tier2_1 = Tier(3, [rnd.uniform(0,5), rnd.uniform(0,5), rnd.random(), rnd.random()], 2, [rnd.uniform(0.33,0.67), rnd.uniform(0.33,0.67)])
tier2_2 = Tier(4, [rnd.uniform(0,5), rnd.uniform(0,5), rnd.random(), rnd.random()], 2, [rnd.uniform(0.33,0.67), rnd.uniform(0.33,0.67)])
tier2_3 = Tier(5, [rnd.uniform(0,5), rnd.uniform(0,5), rnd.random(), rnd.random()], 2, [rnd.uniform(0.33,0.67), rnd.uniform(0.33,0.67)])

tier3_1 = Tier(6, [rnd.uniform(0,5), rnd.uniform(0,5), rnd.random(), rnd.random()], 3, [rnd.uniform(0.67,1), rnd.uniform(0,0.33)])
tier3_2 = Tier(7, [rnd.uniform(0,5), rnd.uniform(0,5), rnd.random(), rnd.random()], 3, [rnd.uniform(0.67,1), rnd.uniform(0,0.33)])
tier3_3 = Tier(8, [rnd.uniform(0,5), rnd.uniform(0,5), rnd.random(), rnd.random()], 3, [rnd.uniform(0.67,1), rnd.uniform(0,0.33)])
tier3_4 = Tier(9, [rnd.uniform(0,5), rnd.uniform(0,5), rnd.random(), rnd.random()], 3, [rnd.uniform(0.67,1), rnd.uniform(0,0.33)])
tier3_5 = Tier(10, [rnd.uniform(0,5), rnd.uniform(0,5), rnd.random(), rnd.random()], 3, [rnd.uniform(0.67,1), rnd.uniform(0,0.33)])

tiers = [tier1_1, tier1_2, tier2_1, tier2_2, tier2_3, tier3_1, tier3_2, tier3_3, tier3_4, tier3_5]

#给3个梯队分类
def classify():
      global tier1, tier2, tier3
      tier1 = []
      tier2 = [] 
      tier3 = []
      for tier in tiers:
            if tier.status == 1:
                  tier1.append(tier)
            elif tier.status == 2:
                  tier2.append(tier)
            else:
                  tier3.append(tier)
      

'''领导人每个时间步长可以发生的行为'''
#计算领导人的效用函数
def U_L(x_policy, y_policy):
      D = leader.distance_preference_policy(x_policy, y_policy)
      P = leader.power_total()
      S = leader.support_aggregate(tier1, tier2, tier3, x_policy, y_policy)
      U = alpha_D * D + alpha_P * P + alpha_S * S
      return U

#选择改变政策(能使个人效用更大!!)
i = 0
def change_policy():
    global x_policy, y_policy 
    u_old = U_L(x_policy, y_policy)
    N = 5 #每次只能考虑N个替代政策
    for i in range(N):
      x_policy_new = [rnd.uniform(0,10)]
      y_policy_new = [rnd.uniform(0,10)]
      u_new = U_L(x_policy_new, y_policy_new)
      if u_new > u_old:
            x_policy = x_policy_new
            y_policy = y_policy_new
            print("3 - change policy")
            break
      elif i==4:
            add = rnd.randint(0,10)
            tiers[add].influence[1] += rnd.uniform(0,0.01)
            print("4 - allocate r_power")


#选择改变政策(使更贴近自己偏好)
def policy_interest():
      global x_policy, y_policy
      x = rnd.random()
      y = rnd.random()
      if x_policy[0] + x <= 10:
            x_policy[0] += x
      if y_policy[0] + y <= 10:
            y_policy[0] += y

      

'''领导人通过启发法和理性水平来选择行为'''
def heruistics():
      global x_policy, y_policy
      trigger = 0
      random = rnd.random()
      if leader.risk == 0: #风险类型属于RAO
            for tier in tiers:
                  if tier.influence[0] + tier.influence[1] >= 1: 
                        trigger = 1
                        if tier.status == 1:
                              tier.status = 2
                              tier.influence[0] = rnd.uniform(0.33,0.67)
                              tier.influence[1] = rnd.uniform(0.33,0.67)
                              print("1.1 - demote")
                              break
                        elif tier.status == 2:
                              tier_hire = tiers[rnd.randint(5,10)]
                              leader.fire_and_hire(tier, tier_hire)            
                              print("1.2 - fire and hire")
                              break
                        else:
                              minus = rnd.uniform(0,0.02)
                              if tier.influence[1] - minus > 0:
                                    tier.influence[1] -= minus
                              print("1.3 - cut r_power")
                              break
      else: #风险类型属于RTO
            if leader.distance_preference_policy(x_policy, y_policy) > 1: #仅凭自己喜好来改变政策（如果政策离自己的喜好太远，则让政策更贴近自己的喜好） -->设置一个阈值确定什么时候需要做出改变
                  policy_interest()
                  trigger = 1
                  print("2 - change with interest")

      #如果启发式规则未被激活，则由理性水平进行决定 
      if trigger == 0:
            if leader.rationality == 1: #如果理性水平高，则会考虑能使效用更大化的替代政策
                  change_policy()
            else: #如果理性水平低，则随机做出一个选择
                  if random > 0.5:
                        x_policy = [rnd.uniform(0,10)]
                        y_policy = [rnd.uniform(0,10)] #随机指定一个policy，或者
                        print("5 - change policy randomly")
                  else:
                        pick1 = rnd.randint(0,5)
                        pick2 = rnd.randint(5,10) #随机挑选两个agent进行f&h操作
                        leader.fire_and_hire(tiers[pick1], tiers[pick2]) 
                        print("6 - fire/hire an agent")
                  
'''普通agent在每个时间步长可以发生的行为'''
#计算自己当前的效用，以及对当前政策的支持
#计算展示图表所需元素
def calculate():
      u_l = U_L(x_policy, y_policy)
      u_a = tier1_1.U_A() + tier1_2.U_A() + tier2_1.U_A() + tier2_2.U_A() + tier2_3.U_A() + tier3_1.U_A() + tier3_2.U_A() + tier3_3.U_A() + tier3_4.U_A() + tier3_5.U_A() 
      u_avg = (u_a + u_l) / 10
      s_all = leader.support_aggregate(tier1, tier2, tier3, x_policy, y_policy) 
      s_tier1 = tier1_1.support() + tier1_2.support()
      return u_l, u_avg, s_all, s_tier1


'''运行中'''
def run(steps):
      u_l = []
      u_avg = []
      s_all = []
      s_tier1 = []
      x_policy_list = []
      y_policy_list = []
      x_no = []
      y_no = []
      for i in range(steps):
            print("run " + str(i))
            print("(", x_policy,", ", y_policy,")")
            classify()
            heruistics()
            shock = rnd.randint(0,9)
            tiers[shock].shock()
            x_leader, y_leader = leader.preference[0], leader.preference[1]
            x_tier1 = [tier.preference[0] for tier in tier1]
            y_tier1 = [tier.preference[1] for tier in tier1]
            x_tier2 = [tier.preference[0] for tier in tier2]
            y_tier2 = [tier.preference[1] for tier in tier2]
            x_tier3 = [tier.preference[0] for tier in tier3]
            y_tier3 = [tier.preference[1] for tier in tier3]

            i_tier1 = [tier.influence[0] for tier in tier1]
            
            for tier in tiers:
                  if tier.number == 1:
                        x_no.append(tier.preference[0])
                        y_no.append(tier.preference[1])
                  if tier.number == 2:
                        x_no.append(tier.preference[0])
                        y_no.append(tier.preference[1])
            
            u_l.append(calculate()[0])
            u_avg.append(calculate()[1])
            s_all.append(calculate()[2])
            s_tier1.append(calculate()[3])
            x_policy_list.append(x_policy)
            y_policy_list.append(y_policy)
            #print(x_tier1,  y_tier1)
            #画图
            if(i==0 or i==100 or i==199):
                  power_display(x_leader, y_leader, x_tier1, y_tier1, x_tier2, y_tier2, x_tier3, y_tier3, x_policy, y_policy, x_no, y_no)
                  # agent_stats(u_l, u_avg, s_all, s_tier1)
                  # utility_3D(x,y,z)
                  # utility_3D(x,y,k)
                  
            #在step 100更换领导人
            if(i==99): 
                  leader.sucession("A")
                  power_display(x_leader, y_leader, x_tier1, y_tier1, x_tier2, y_tier2, x_tier3, y_tier3, x_policy, y_policy, x_no, y_no)
      print(alpha_D, alpha_P, alpha_S)  
      print(alpha_x, alpha_y)
      print(np.mean(u_l[90:99]))
      print(np.mean(u_l[100:109]))
      print(np.mean(u_l[190:199]))
      print(np.mean(s_all[90:99]))
      print(np.mean(s_all[100:109]))
      print(np.mean(s_all[190:199]))
      # 画3D图
      x,y = np.meshgrid(x_policy_list, y_policy_list)
      z,z1 = np.meshgrid(u_l,u_l)
      k, k1 = np.meshgrid(s_all, s_all)
      #utility_3D(x,y,z)
      # utility_3D(x,y,k)

      s_all = [s * 0.2 for s in s_all]
      #agent_stats(u_l, s_all)
      

'''实验1-A'''
run(200)


'''test'''
