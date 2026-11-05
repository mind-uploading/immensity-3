#价值分类记忆与价值系统
import 公共状态


#发放情绪
def emo(senlist):
    from 行为与计划模块.行为与计划模块 import choose_act
    #清零总的喜/哀的水平hapsum/sadsum
    hapsum=0
    sadsum=0


    #根据状态转移概率矩阵发放情绪

    #1、创建一个状态-概率堆（包括状态及其发生概率（相对于当前状态而言））
    state_chance_heap=[]

    #2、根据行为习惯列表确定当前知觉概念列表引发的行为概念列表，将两者合并为当前状态（发生概率为1），将其加入状态-概率堆中
    acthablist_predict,actlist_predict,psav_now_predict=choose_act(公共状态.acthablist,公共状态.actlist,[])
    state_chance_heap.append([senlist+actlist_predict,1])

    #5、重复3、4两步直到预测到attentive_time_step_count（该参数的含义见行为与计划模块）个回合后
    for j in range(公共状态.attentive_time_step_count):

        #3、对状态-概率堆中所有状态，若状态包含某个senlist-hap/sad组的senlist，则发放这个senlist对应的hap/sad与概率的乘积
        for state_chance in state_chance_heap:
            for i in 公共状态.haphablist:
                if set(i[0]).issubset(set(state_chance[0])):
                    hapsum+=int(i[1])*state_chance[1]
            for i in 公共状态.sadhablist:
                if set(i[0]).issubset(set(state_chance[0])):
                    sadsum+=int(i[1])*state_chance[1]

        #4、根据状态转移概率矩阵预测下一回合的状态及其概率，并用他们替换状态-概率堆中原先的内容
        state_chance_heap1=[]
        for state_chance in state_chance_heap:
            for translist in 公共状态.transmatrix:
                if translist[0]==state_chance[0]:
                    for i in translist[1:]:
                        state_chance_heap1.append([i[0],i[1]*state_chance[1]])
        state_chance_heap=state_chance_heap1



    #将hapsum和sadsum的值限制在0-5这一范围内，并保留小数点后1位


    if hapsum>5:
        hapsum=5
    if sadsum>5:
        sadsum=5
    hapsum=round(hapsum,1)
    sadsum=round(sadsum,1)
    #print("喜x",hapsum)
    #print("哀x",sadsum)

    #总价值vsum=hapsum-sadsum

    vsum=hapsum-sadsum
    #print("总价值：",vsum)

    return hapsum,sadsum,vsum
