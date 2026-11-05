#行为与计划模块
import copy
import time
import random
import operator
import pyautogui

import 公共状态


# 行为类
class ACT:
    def __init__(self,senlist,hapsum,sadsum,vsum,actlist):
        self.senlist=senlist
        self.hapsum=hapsum
        self.sadsum=sadsum
        self.vsum=vsum
        self.actlist=actlist


    def report_qualia(self):#报告意识体验
        print("意识体验内容：")
        print("当前知觉概念：",self.senlist)
        print("当前喜：",self.hapsum)
        print("当前哀：",self.sadsum)
        print("当前总价值：",self.vsum)
        print("当前行为概念：",self.actlist)
    def increase_art_vigilance(self):#提高ART的警戒值
        公共状态.art_model.vigilance=0.9
    def pressA(self):#按键盘中的A键
        pyautogui.press('a')
    def pressD(self):#按键盘中的D键
        pyautogui.press('d')
    def pressW(self):#按键盘中的W键
        pyautogui.press('w')
    def pressS(self):#按键盘中的S键
        pyautogui.press('s')

    def scrollup(self):#鼠标滚轮向上滚动
        pyautogui.scroll(100)
    def scrolldown(self):#鼠标滚轮向下滚动
        pyautogui.scroll(-100)

    def introspect(self):#内省
        #内省内容包括senlist、hapsum、sadsum和vsum（不包括actlist，因为 函数：扩展知觉概念列表senlist 会将其加入下一回合的知觉概念列表）
        公共状态.introcontent=[]
        for sen in self.senlist:
            公共状态.introcontent.append(sen+"（p）")#知觉概念末尾添加“（p）”，表示对于下一回合的senlist来说，这个知觉概念是上一回合发生的
        公共状态.introcontent.append("喜："+str(self.hapsum))
        公共状态.introcontent.append("哀："+str(self.sadsum))
        公共状态.introcontent.append("总价值："+str(self.vsum))



#根据实践结果更新psav组的v值
def update_v(acthablist):

    #1、计算TD误差
    #TDerror(t)≈vsum-Qpt
    if len(公共状态.psav_memory)==0:
        TDerror=公共状态.vsum
    else:
        #目前psav_memory中每个时间步的psav组的所有的psav的v值相同（也必须相同，这样才能确保每个Qpt都在朝Qt方向更新），故取第一个psav的v值
        TDerror=公共状态.vsum-公共状态.psav_memory[-1][0][2]

    #2、更新所有在前attentive_time_step_count(=5)个时间步内被激活过的psav组（记录在psav_memory中）的v值
    #v值（Qpt） <-- v值（Qpt）+lr*(TDerror(t))

    lr=0.3


    for i in range(len(公共状态.psav_memory)):#获取psav_memory中倒数attentive_time_step_count个时间步内的psav(们)
        psavs=公共状态.psav_memory[-i-1]

        for j in psavs:#对psavs中的每一个psav，在acthablist中查找该psav
            for psav in acthablist:

                if sorted(j[0])==sorted(psav[0]) and sorted(j[1])==sorted(psav[1]):#若psavs中的psav与acthablist中的psav在ps和a上相同
                    psav[2]=round(psav[2]+lr*TDerror,2)


    return acthablist



#根据行为的预期价值（即Qpt）（借助情绪习惯列表和状态转移概率矩阵求得）调整行为习惯
def change_acthablist(acthablist):
    from 价值分类记忆与价值系统.价值分类记忆与价值系统 import emo

    #对行为习惯列表中的每个psav(psen-act-value)组，若value<=行为调整激活阈值v_adjustact_threshold，
    #根据状态转移概率矩阵和情绪习惯列表对该psav组进行优化：
    for psav in acthablist:
        if psav[2]<=公共状态.v_adjustact_threshold:




            bxact=[]#备选act
            Qpt=公共状态.v_adjustact_threshold#Qpt



            #在状态转移概率矩阵中查找包含psen且不包含行为空间外的行为的状态。将此状态中除psen外的部分（肯定在行为空间内）作为备选act
            for translist in 公共状态.transmatrix:

                #判断translist[0]-psenlist的差集是否被allact包含，即判断translist[0]中除了psenlist外，是否有做不到的行为
                zuobudao=0
                diffset=[]
                for i in translist[0]:
                    if i not in psav[0]:
                        diffset.append(i)
                for i in diffset:
                    if i not in 公共状态.allact:
                        zuobudao=1
                        break
                if zuobudao==0:
                    #判断psenlist是否⊂translist[0]
                    for psen in psav[0]:
                        if psen not in translist[0]:
                            break
                    else:#没有执行break说明psenlist⊂translist[0]且translist[0]中除了psenlist外，没有做不到的行为

                        #对每个备选act：将其与psen结合作为初始状态，然后将这个初始状态导入状态转移概率矩阵中，预测出接下来attentive_time_step_count个时间步的状态及其发生概率。
                        allresult=[]#所有时间步的状态及其发生概率
                        result=[]#某一时间步的状态及其发生概率

                        result=sorted(translist[1:], key=operator.itemgetter(1), reverse=True)[0:3]#获取translist中发生概率前三大的状态及其发生概率
                        allresult.extend(result)
                        for i in range(公共状态.attentive_time_step_count-1):#对attentive_time_step_count-1个时间步进行预测
                            for state_chance_times in result:
                                for translist in 公共状态.transmatrix:
                                    if translist[0]==state_chance_times[0]:
                                        result=sorted(translist[1:], key=operator.itemgetter(1), reverse=True)[0:3]#获取translist中发生概率前三大的状态及其发生概率
                                        allresult.extend(result)


                        #对这attentive_time_step_count个时间步的状态，先根据 函数：发放情绪 求出每个状态的价值，再将状态的价值与状态发生的概率相乘，最后对这些乘积求和，以此作为这个备选act的Qpt
                        vsum1=0
                        for state_chance_times in allresult:
                            hapsum2,sadsum2,vsum2=emo(state_chance_times[0])
                            vsum1+=vsum2*state_chance_times[1]

                        #选出Qpt最高的备选act
                        if vsum1>Qpt:
                            Qpt=vsum1
                            bxact=diffset

            #1、若其Qpt高于v_adjustact_threshold，将其记作newact，将其Qpt记作newvalue
            if Qpt>公共状态.v_adjustact_threshold:
                newact=bxact
                newvalue=Qpt
                #往行为习惯列表中添加一个新的psav组：psen-newact-newvalue
                acthablist.append([psav[0],newact,round(newvalue,2)])
            #2、若其Qpt不高于v_adjustact_threshold，往原psav组的act（实际上是actlist）中随机地添加或删除行为，将结果作为newact，newvalue则为v_adjustact_threshold+1（对优化后的行为的价值持乐观预期）
            else:
                if random.random()<0.5:
                    newact=copy.deepcopy(psav[1])
                    newact.append(random.choice(list(公共状态.allact)))
                    newvalue=公共状态.v_adjustact_threshold+1

                    #往行为习惯列表中添加一个新的psav组：psen-newact-newvalue
                    acthablist.append([psav[0],newact,newvalue])


                else:
                    if psav[1]!=[]:
                        removeact=psav[1][random.randint(0, len(psav[1]) - 1)]
                        newact=copy.deepcopy(psav[1])
                        newact.remove(removeact)
                        newvalue=公共状态.v_adjustact_threshold+1
                        #往行为习惯列表中添加一个新的psav组：psen-newact-newvalue
                        acthablist.append([psav[0],newact,newvalue])


    #若该psav组已是attentive_time_step_count个时间步之前发生的了，且其value<=v_adjustact_threshold，将其移除
    senlist_actlist_vsum=公共状态.memorylist[-公共状态.attentive_time_step_count]
    for psav in copy.deepcopy(acthablist):
        if psav[0]==senlist_actlist_vsum[0] and psav[1]==senlist_actlist_vsum[1] and psav[2]<=公共状态.v_adjustact_threshold:
            acthablist.remove(psav)




    #删除自发行为
    acthablist1=[]
    for psav in acthablist:
        if psav[0]!=[]:
            acthablist1.append(psav)
    acthablist=acthablist1


    return acthablist


#根据知觉概念列表和行为习惯选择将执行的行为概念（若允许调整行为习惯列表，添加psav组）
def choose_act(acthablist,actlist,psav_now):
    #注：
    #1、若整理好的行为概念（actlist）与senlist构成的ps-a在acthablist中没有与之对应的psav组，则将其作为新的psav组添加入acthablist
    #2、被激活过的psav组会被记录到此回合用到的psav（psav_now）中

    psav_now=[]
    actlist=[]
    find=False

    #step1、遍历acthablist，若其中某些psav组的psen=senlist，输出v最大的那个psav组中的act

    vmax=float("-inf")
    for psav in acthablist:
        if sorted(psav[0])==sorted(公共状态.senlist):
            if psav[2]>vmax:
                vmax=psav[2]
                actlist=psav[1]
                find=True#表示step1中找到了符合要求的psav组
                #psav_now中添加该psav组
                psav_now.append(psav.copy())

    #step2（模糊匹配）、若step1中未找到符合要求的psav组，扩大搜索范围：遍历acthablist，若某些psav组的psen⊂senlist，输出v最大（需大于v_adjustact_threshold）的那个psav组中的act

    vmax=公共状态.v_adjustact_threshold
    if find==False:
        for psav in acthablist:
            for i in psav[0]:
                if i not in 公共状态.senlist:
                    break
            else:
                if psav[2]>vmax:
                    vmax=psav[2]
                    actlist=psav[1]
                    find=True#表示step2中找到了符合要求的psav组
                    #psav_now中添加该psav组
                    psav_now.append(psav.copy())
                    #psav_now中添加psav组：senlist-actlist-被模糊匹配到的那个psav组的v值
                    psav_now.append([公共状态.senlist,actlist,psav[2]])
                    #acthablist中添加psav组：senlist-actlist-被模糊匹配到的那个psav组的v值
                    if 公共状态.adjust_acthablist=="1":#若允许调整行为习惯列表
                        acthablist.append([公共状态.senlist,actlist,psav[2]])

    #step3、若step1和step2中都未找到符合要求的psav组，则不输出行为

    if find==False:
        #acthablist中添加psav组：senlist-[]-0
        if 公共状态.adjust_acthablist=="1":#若允许调整行为习惯列表
            acthablist.append([公共状态.senlist,actlist,0])
		#psav_now中添加psav组：senlist-[]-0
        psav_now.append([公共状态.senlist,actlist,0])



    return acthablist,actlist,psav_now



#更新psav_memory
def update_psav_memory(psav_now,psav_memory):
    #psav_memory是一个列表，其中按从旧到新的先后顺序存储了最近attentive_time_step_count个时间步用过的psav（们）
    #在psav_memory中添加psav_now，并移除psav_memory中最旧的psav（们）
    if len(psav_memory) >= 公共状态.attentive_time_step_count:
        psav_memory.pop(0)
    psav_memory.append(psav_now)

    return psav_memory




#对行为进行分解细化
def act_detail(want_learn_list):
    counts=0
    if 公共状态.mode!="3":#若未进入自主模式
        while True:
            公共状态.root.update()
            if 公共状态.varcbcounts1.get()==1 and 公共状态.varcbcounts2.get()==1:
                counts=int(公共状态.entcounts.get())
                公共状态.varcbcounts1.set(0)
                公共状态.varcbcounts2.set(0)
                break
            import time
            time.sleep(0.1)
    '''
    counts=0
    if actlist!=[]:
        counts=int(input("分解次数:"))
    '''

    act_detail_list=copy.deepcopy(公共状态.actlist)
    act_detail_list1=[]

    if counts>=1:
        for i in range(counts):

            for act in act_detail_list:
            #在状态转移概率矩阵中寻找要做的行为的前置状态，若未搜索到，将该行为添加入学习需求列表want_learn_list中
                find=False
                for translist in 公共状态.transmatrix:
                    for state_chance_times in translist[1:]:
                        if act in state_chance_times[0] and state_chance_times[1]>=0.5:
                            act_detail_list1.extend(translist[0])
                            find=True
                            print("要做",act,"先做",translist[0])

                if find==False:
                    print("未搜索到",act,"的前置状态")
                    want_learn_list.append(act)

            act_detail_list=copy.deepcopy(act_detail_list1)
            act_detail_list1=[]



    #对学习需求列表进行去重
    list1=[]
    for i in want_learn_list:
        if i not in list1:
            list1.append(i)
    want_learn_list=list1

    #输出学习需求列表
    if want_learn_list!=[]:
        print("需要学习以下行为：",want_learn_list)

    return act_detail_list,want_learn_list


#输出行为概念并执行
def output_act(actlist):
    if "报告意识体验" in actlist:
        ACT(公共状态.senlist,公共状态.hapsum,公共状态.sadsum,公共状态.vsum,actlist).report_qualia()
    if "更新SOM" in actlist:
        ACT(公共状态.senlist,公共状态.hapsum,公共状态.sadsum,公共状态.vsum,actlist).update_som()
    if "pressA" in actlist:
        ACT(公共状态.senlist,公共状态.hapsum,公共状态.sadsum,公共状态.vsum,actlist).pressA()
    if "pressD" in actlist:
        ACT(公共状态.senlist,公共状态.hapsum,公共状态.sadsum,公共状态.vsum,actlist).pressD()
    if "pressW" in actlist:
        ACT(公共状态.senlist,公共状态.hapsum,公共状态.sadsum,公共状态.vsum,actlist).pressW()
    if "pressS" in actlist:
        ACT(公共状态.senlist,公共状态.hapsum,公共状态.sadsum,公共状态.vsum,actlist).pressS()
    if "scrollup" in actlist:
        ACT(公共状态.senlist,公共状态.hapsum,公共状态.sadsum,公共状态.vsum,actlist).scrollup()
    if "scrolldown" in actlist:
        ACT(公共状态.senlist,公共状态.hapsum,公共状态.sadsum,公共状态.vsum,actlist).scrolldown()
    if "内省" in actlist:
        ACT(公共状态.senlist,公共状态.hapsum,公共状态.sadsum,公共状态.vsum,actlist).introspect()
    if "在下一回合学习生词" in actlist:
        公共状态.learn_new_word=True
    if "生成句子" in actlist:
        公共状态.generate_sent=True
