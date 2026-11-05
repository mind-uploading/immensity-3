def worldmodel(transmatrix,psenlist,senlist):#世界模型

    #根据当前知觉概念更新状态转移概率矩阵
    
    #更新状态转移矩阵中的状态和次数
    for translist in transmatrix:
        if translist[0]==psenlist:
            for i in translist[1:]:
                if i[0]==senlist:
                    i[2]+=1
                    break
            else:
                translist.append([senlist,0,1])
        break
    else:
        transmatrix.append([psenlist,[senlist,1,1]])

    #更新状态转移矩阵中的概率
    for translist in transmatrix:
        totaltimes=0
        for i in translist[1:]:
            totaltimes+=i[2]
        for i in translist[1:]:
            i[1]=i[2]/totaltimes

    print("截至目前的状态转移矩阵为：",transmatrix)
    
    
    #根据状态转移矩阵预测接下来各状态的发生概率，以及最可能发生的状态
    
    probability=[]
    for translist in transmatrix:
        if translist[0]==senlist:
            predict_state_chance=translist[1:]#接下来各状态的发生概率
            print("接下来各状态发生概率为：",predict_state_chance)
            
            predict_max_chance=0
            predict_max_state=[]
            for i in translist[1:]:
                if i[1]>predict_max_chance:
                    predict_max_chance=i[1]
                    predict_max_state=i[0]
                    print("接下来最可能发生的状态为：",predict_max_state)

            break
    else:
        print("未在状态转移矩阵中发现当前知觉概念列表所对应的接下来的状态")
    
    return predict_state_chance,predict_max_state
    
    
import random

def predict_next_state(current_state):
    # 获取当前状态的转移概率
    probabilities = transitions[current_state]
    # 选择下一个状态
    next_state = random.choices(list(probabilities.keys()), list(probabilities.values()))[0]
    return next_state
def simulate_weather(start_state, days=10):
    weather_sequence = [start_state]
    current_state = start_state
    
    for _ in range(1, days):
        current_state = predict_next_state(current_state)
        weather_sequence.append(current_state)
    
    return weather_sequence

# 示例：从晴天开始，模拟10天的天气
print(simulate_weather('Sunny'))