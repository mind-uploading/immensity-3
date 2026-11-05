#初始化
#上一回合知觉概念列表
psenlist=[]
#上一回合行为概念列表
pactlist=[]
#知觉概念列表
senlist=[]
#行为概念列表
actlist=[]
#学习需求列表
want_learn_list=[]

#设置
print("请进行设置------------------")

#是否进入预设的模式
mode=input("是否进入预设的模式？（不可变模式：1，默认模式：2，否：0）")
if mode=="1":
    senlist_add_actlist="0"
    randforget="0"
    adjust_hapsadhablist="0"
    adjust_acthablist="0"
elif mode=="2":
    senlist_add_actlist="0"
    randforget="1"
    adjust_hapsadhablist="1"
    hapsum_mem_threshold=2
    sadsum_mem_threshold=2
    adjust_acthablist="1"
    v_acthab_threshold=1
    v_adjustact_threshold=2

else:
    #1、将上一回合输出的行为概念加入下一回合的知觉概念列表中
    senlist_add_actlist=input("是否要将上一回合输出的行为概念加入下一回合的知觉概念列表中？（是：1，否：0）")

    #2、随机遗忘机制
    randforget=input("是否要激活随机遗忘机制？（是：1，否：0）")

    #3、调整情绪习惯列表
    adjust_hapsadhablist=input("是否允许调整情绪习惯列表？（是：1，否：0）：")
    if adjust_hapsadhablist=="1":
        #设定价值分类记忆激活阈值
        #（一个新概念引发的情绪发放如果超过阈值则该概念被纳入价值分类记忆）
        print("接下来你将输入价值分类记忆激活阈值（范围0-5，通常为2）\n一个新概念引发的情绪发放如果超过阈值则该概念被纳入价值分类记忆")
        hapsum_mem_threshold=int(input("喜的价值分类记忆激活阈值："))
        
        sadsum_mem_threshold=int(input("哀的价值分类记忆激活阈值："))


    #4、调整行为习惯列表
    adjust_acthablist=input("是否允许调整行为习惯列表？（是：1，否：0）：")
    if adjust_acthablist=="1":
        #行为固定化阈值v_acthab_threshold
        #若vsum>=行为固定化阈值v_acthab_threshold，将当前行为模式固定化（存入acthablist中）
        print("接下来你将输入行为固定化阈值v_acthab_threshold（范围0-5，通常为1）\n若总价值vsum>=行为固定化阈值v_acthab_threshold，将当前行为模式固定化")
        v_acthab_threshold=int(input("行为固定化阈值v_acthab_threshold："))

        #行为调整激活阈值v_adjustact_threshold
        #若总价值vsum<=行为调整激活阈值v_adjustact_threshold，在当前行为模式基础上进行优化
        print("接下来你将输入行为调整激活阈值v_adjustact_threshold（范围0-5，通常为2）\n若总价值vsum<=行为调整激活阈值v_adjustact_threshold，在当前行为模式基础上进行优化")
        v_adjustact_threshold=int(input("行为调整激活阈值v_adjustact_threshold："))

print("设置完成------------------")

#同步
print("请进行同步--------------")
#同步情绪习惯

print("同步情绪习惯列表--------------")
haphablist=[]
hapbbh=input("输入要同步的喜习惯列表的版本号：")
hapwjlj="情绪习惯列表/喜习惯列表/喜习惯列表"+hapbbh+".txt"#喜习惯列表文件路径

with open(hapwjlj,'r',encoding='utf-8') as hapfile:
    hang=hapfile.readline().strip()
    while hang:

        senlisthap1=hang.split("；")#引发喜的知觉概念列表（senlist）和该列表引发的喜的水平（hap）之间用“；”连接
        senlist=senlisthap1[0].split("。")#引发喜的知觉概念列表内部的概念用“。”连接
        hap=int(senlisthap1[1])
        #删除切片出的空内容
        while "" in senlist:
            senlist.remove("")
     
        haphablist.append([senlist,hap])
        hang=hapfile.readline().strip()

sadhablist=[]
sadbbh=input("输入要同步的哀习惯列表的版本号：")
sadwjlj="情绪习惯列表/哀习惯列表/哀习惯列表"+sadbbh+".txt"#哀习惯列表文件路径

with open(sadwjlj,'r',encoding='utf-8') as sadfile:
    hang=sadfile.readline().strip()
    while hang:

        senlistsad1=hang.split("；")#引发哀的知觉概念列表（senlist）和该列表引发的哀的水平（sad）之间用“；”连接
        senlist=senlistsad1[0].split("。")#引发哀的知觉概念列表内部的概念用“。”连接
        sad=int(senlistsad1[1])
        #删除切片出的空内容
        while "" in senlist:
            senlist.remove("")
     
        sadhablist.append([senlist,sad])
        hang=sadfile.readline().strip()

print("情绪习惯列表：")
print("（结构：[[senlist1，hap1/sad1],[senlist2，hap2/sad2],...]）")
print("喜习惯列表：",haphablist)
print("哀习惯列表：",sadhablist)

#同步行为空间（这是一个列表）
print("同步行为空间---------------")
allact=[]
allactbbh=input("输入要同步的行为空间的版本号：")
allactwjlj="行为空间/行为空间"+allactbbh+".txt"


with open(allactwjlj,"r",encoding='utf-8') as allactfile:
    acts=allactfile.readline().strip()
    while acts:
        allact.append(acts)
        acts=allactfile.readline().strip()
print("行为空间：",allact)

#同步行为习惯列表acthablist
print("同步行为习惯列表acthablist----------------")
acthablist=[]
acthabbbh=input("输入要同步的行为习惯列表的版本号：")
acthabwjlj="行为习惯列表/行为习惯列表"+acthabbbh+".txt"

with open(acthabwjlj,"r",encoding='utf-8') as acthabfile:
    hang=acthabfile.readline().strip()
    while hang:

        psav1=hang.split("；")#ps、a、v之间用“；”连接
        psav_p=psav1[0].split("。")#ps内部用“。”连接
        psav_a=psav1[1].split("。")#a内部用“。”连接    
        v=int(psav1[2])
        #删除切片出的空内容
        while "" in psav_p:
            psav_p.remove("")
        while "" in psav_a:
            psav_a.remove("")
        acthablist.append([psav_p,psav_a,v])
        hang=acthabfile.readline().strip()
print("行为习惯列表acthablist:",acthablist)

#同步自传体记忆
print("同步自传体记忆----------------")
memorylist=[]
memorylistbbh=input("输入要同步的自传体记忆的版本号：")
memorylistwjlj="自传体记忆/自传体记忆"+memorylistbbh+".txt"#自传体记忆文件路径

with open(memorylistwjlj,'r',encoding='utf-8') as memorylistfile:
    hang=memorylistfile.readline().strip()
    while hang:

        senlist=hang.split("。")#知觉概念列表内部的概念用“。”连接
        #删除切片出的空内容
        while "" in senlist:
            senlist.remove("")
     
        memorylist.append(senlist)
        hang=memorylistfile.readline().strip()

print("自传体记忆：",memorylist)

#同步状态转移概率矩阵
print("同步状态转移概率矩阵----------------")
transmatrix=[]
transmatrixbbh=input("输入要同步的状态转移概率矩阵的版本号：")
transmatrixwjlj="状态转移概率矩阵/状态转移概率矩阵"+transmatrixbbh+".txt"
with open(transmatrixwjlj,'r',encoding='utf-8') as transmatrixfile:
    hang=transmatrixfile.readline().strip()
    while hang:
        translist=[]
        startstate=hang.split("；")[0].split("。")
        while "" in startstate:
            startstate.remove("")
        translist.append(startstate)

        for i in hang.split("；")[1:]:
            endstateseq=i.split("、")
            while "" in endstateseq:
                endstateseq.remove("")
            endstate=endstateseq[0].split("。")
            while "" in endstate:
                endstate.remove("")
            chance=float(endstateseq[1])
            times=int(endstateseq[2])
            
            translist.append([endstate,chance,times])
        
        transmatrix.append(translist)

        hang=transmatrixfile.readline().strip()

        print("状态转移概率矩阵：",transmatrix)



print("同步完成--------------")


#各个模块

def senpart(pactlist,senlist_add_actlist):#知觉分类模块
    print("知觉分类模块--------------------------------------------------")
    senlist=[]
    sen=input("知觉概念：（输入完请输入0）")
    while sen!="0":
        senlist.append(sen)
        sen=input("知觉概念：（输入完请输入0）")

    if senlist_add_actlist=="1":#若启用“将上一回合输出的行为概念加入下一回合的知觉概念列表中”的机制
        senlist.extend(pactlist)


    print("当前知觉概念列表：",senlist)
    return senlist



def valpart(haphablist,sadhablist,senlist,randforget,adjust_hapsadhablist):#价值分类记忆与价值系统
    print("价值分类记忆与价值系统--------------------------------------------------")
    import random
    #清零总的喜/哀的水平hapsum/sadsum

    hapsum=0

    sadsum=0


    
    #输出当前知觉概念列表对应的价值
    for i in haphablist:
        if set(i[0]).issubset(set(senlist)):
            hapsum+=i[1]

    for i in sadhablist:
        if set(i[0]).issubset(set(senlist)):
            sadsum+=i[1]
   
    #各喜/哀的水平hap/sum和总的喜/哀的水平hapsum/sadsum的取值范围：0-5

    if hapsum>5:
        hapsum=5
    if sadsum>5:
        sadsum=5
    print("喜x",hapsum)
    print("哀x",sadsum)    

    vsum=hapsum-sadsum
    print("总价值：",vsum)
    
    #将知觉概念与情绪关联起来

    if adjust_hapsadhablist=="1":#若允许调整情绪习惯列表
        #情绪发放显著时（hapsum/sadsum>=hapsum/sadsum_mem_threshold），将当前的知觉概念列表与4中所有用到过的senlist的差集及当时的hapsum/sadsum作为一组senlist-hap/sad组加入情绪习惯列表
        if hapsum>=hapsum_mem_threshold:
            difflist=senlist.copy()
            for i in haphablist:
                if set(i[0]).issubset(set(difflist)):
                    for j in i[0]:
                        difflist.remove(j)
            if difflist!=[]:
                haphablist.append([difflist,hapsum])

           
            
        if sadsum>=sadsum_mem_threshold:
            difflist=senlist.copy()
            for i in sadhablist:
                if set(i[0]).issubset(set(difflist)):
                    for j in i[0]:
                        difflist.remove(j)
            if difflist!=[]:
                sadhablist.append([difflist,sadsum])

    #价值分类记忆随机遗忘
    #情绪习惯列表中的每个senlist-hap/sad的hap/sad在每回合都有1/10的概率被下调1,若降至0以下则该组senlist-hap/sad被删除
    if randforget=="1":#若启用随机遗忘机制
        for i in haphablist:
            if random.random()<0.1:
                i[1]-=1
                if i[1]<0:
                    haphablist.remove(i)
                    
        for i in sadhablist:
            if random.random()<0.1:
                i[1]-=1
                if i[1]<0:
                    sadhablist.remove(i)
    
    print("情绪习惯列表：")  
    print("（结构：[[senlist1，hap1/sad1],[senlist2，hap2/sad2],...]）")
    print("喜习惯列表：",haphablist)
    print("哀习惯列表：",sadhablist)

    
    return hapsum,sadsum,vsum,haphablist,sadhablist



def actpart(psenlist,pactlist,acthablist,allact,senlist,vsum,adjust_acthablist,transmatrix,want_learn_list):#行为与计划模块
    print("行为与计划模块--------------------------------------------------")
    import random
    
            
    if adjust_acthablist=="1":#若允许调整行为习惯列表
        #根据价值调整行为习惯列表

        #若当前psen-a已在acthablist中
        zai=0
        for i in range(6):
            if [psenlist,pactlist,i] in acthablist:
                #根据实践更新当前psen-a对应的vsum
                acthablist.remove([psenlist,pactlist,i])
                vsum=round(0.7*vsum+0.3*i)#新的vsum为70%x当前的vsum+30%x原先的vsum(四舍五入)
                acthablist.append([psenlist,pactlist,vsum])
                zai=1
        #若不在，如果vsum>=v_acthab_threshold，将当前psen-a固定化（存入acthablist中）
        if zai==0:
            if vsum>=v_acthab_threshold:
                #acthablist中存psav(psen-act-value),其中psen存上一回合知觉概念列表，act存上一回合行为概念列表，v存上一回合执行该行为概念列表后，本回合的vsum
                acthablist.append([psenlist,pactlist,vsum])
                    

        #优化行为习惯
        #若vsum<=v_adjustact_threshold，在当前行为模式基础上进行优化(往相应的acthablist中添加或删除随机行为，对应的vsum+1（对优化后的行为的价值持乐观预期）)
        if vsum<=v_adjustact_threshold:
            if random.random()<0.5:
                pactlist1=pactlist.copy()
                pactlist1.append(random.choice(list(allact)))
                a=[psenlist,pactlist1,vsum+1]
                acthablist.append(a)
               
            else:
                if pactlist!=[]:
                    removeact=pactlist[random.randint(0, len(pactlist) - 1)]
          
                    pactlist1=pactlist.copy()
                    pactlist1.remove(removeact)
                    a=[psenlist,pactlist1,vsum+1]
                    acthablist.append(a)
                    

        #删除自发行为
        for psav in acthablist:
            if psav[0]==[]:
                acthablist.remove(psav)

    print("行为习惯列表：",acthablist)



    #根据行为习惯输出行为
    actlist=[]
    find=False
    
    #step1、遍历acthablist，若其中某些psav组的psen=senlist（知觉概念列表），判断这些psav组的v是否大于0，输出v大于0的那些psav组中的act（行为概念列表）

    for psav in acthablist:
        if sorted(psav[0])==sorted(senlist):
            if psav[2]>0:
                actlist.extend(psav[1])
                find=True#表示step1中找到了符合要求的psav组
                print("step1中找到符合“psen=senlist”要求的psav组")
                
    #step2、若step1中未找到符合要求的psav组，扩大搜索范围：遍历acthablist，若某些psav组的psen⊂senlist，判断这些psav组的v是否大于0，输出v大于0的那些psav组中的act

    if find==False:
        print("step1中未找到符合“psen=senlist”要求的psav组")
        for psav in acthablist:
            for i in psav[0]:
                if i not in senlist:
                    break
            else:
                actlist.extend(psav[1])
                find=True#表示step2中找到了符合要求的psav组
                print("step2中找到符合“psen⊂senlist”要求的psav组")

    #step3、若step1和step2中都未找到符合要求的psav组，则随机输出行为

    if find==False:
        print("step1和step2中都未找到符合要求的psav组，当前精神图景下最优行为未知，输出随机行为")
        act=random.choice(allact)
        actlist.append(act)

    #行为和负行为相互抵消
    for act in actlist:
        if act[0]=="-":
            minusact=act[1:]#获取负行为中“-”后的内容
            actlist.remove(act)#在行为列表中删除该负行为
            if minusact in actlist:
                actlist.remove(minusact)#在行为列表中删除该负行为中“-”后的内容
    
    #合并相同的行为
    actlist1=[]
    for act in actlist:
        if act not in actlist1:
            actlist1.append(act)
    actlist=actlist1
        
    print("当前精神图景下最优行为：",actlist)


    #对行为进行分解细化
    counts=int(input("分解次数:"))
    
    act_detail_list=actlist
    act_detail_list1=[]

    if counts>=1:
        for i in range(counts):
           
            for act in act_detail_list:
            #在状态转移概率矩阵中寻找要做的行为的前置状态，若未搜索到，将该行为添加入学习需求列表want_learn_list中
                find=False
                for translist in transmatrix:
                    for state_chance_times in translist[1:]:
                        if act in state_chance_times[0] and state_chance_times[1]>=0.5:
                            act_detail_list1.extend(translist[0])
                            find=True
                            print("要做",act,"先做",translist[0])

                if find==False:        
                    print("未搜索到",act,"的前置状态")
                    want_learn_list.append(act)
            
            act_detail_list=act_detail_list1
            act_detail_list1=[]
        
        print("行为细化后：",act_detail_list)



    #对学习需求列表进行去重
    list1=[]
    for i in want_learn_list:
        if i not in list1:
            list1.append(i)
    want_learn_list=list1

    #输出学习需求列表
    if want_learn_list!=[]:
        print("需要学习以下行为：",want_learn_list)
        
  

 


    return actlist,want_learn_list


def memorypart(senlist,memorylist):#记忆模块
    print("记忆模块--------------------------------------------------")
    memorylist.append(senlist)
    print("截至目前的自传体记忆为：",memorylist)

    return memorylist

def worldmodel(transmatrix,psenlist,senlist):#世界模型
    print("世界模型--------------------------------------------------")

    #根据当前知觉概念更新状态转移概率矩阵
    
    #更新状态转移概率矩阵中的状态和次数
    for translist in transmatrix:
        if translist[0]==psenlist:
            
            cunzai=False
            
            for i in translist[1:]:
                if i[0]==senlist:
                    i[2]+=1
                    i[1]=i[1]*0.8+1*0.2
                    cunzai=True
                else:
                    i[1]=i[1]*0.8+0*0.2 
                    
            if cunzai==False:
                translist.append([senlist,1,1])
            
            break
    else:
        transmatrix.append([psenlist,[senlist,1,1]])


    print("截至目前的状态转移概率矩阵为：",transmatrix)
    
    
    #根据状态转移概率矩阵预测接下来各状态的发生概率，以及最可能发生的状态
    predict_state_chance=[]
    predict_max_chance=0
    predict_max_state="未发现"
    
    for translist in transmatrix:
        if translist[0]==senlist:
            predict_state_chance=translist[1:]#接下来各状态的发生概率
            print("接下来各状态发生概率为：",predict_state_chance)
            
            
            for i in translist[1:]:
                if i[1]>predict_max_chance:
                    predict_max_chance=i[1]
                    predict_max_state=i[0]
                    print("接下来最可能发生的状态为：",predict_max_state,"发生概率为：",predict_max_chance)

            break
    else:
        print("未在状态转移概率矩阵中发现当前知觉概念列表所对应的接下来的状态")
        predict_state_chance="未发现"
    
    return transmatrix,predict_state_chance,predict_max_state,predict_max_chance
    
def learnpart(transmatrix,actlist,want_learn_list):#学习模块
    print("学习模块--------------------------------------------------")
    
    #检测行为与计划模块是否发放了“学习”指令
    if "学习" in actlist:
        actlist.remove("学习")#删除actlist中的“学习”指令

        want_learn_list1=want_learn_list.copy()

        #对每个want_learn_list中的act
        for act in want_learn_list:

            #询问大模型，获知act的前置状态

            print(act," 的前置状态是否已被获知？（是：1，否：0）")
            huozhi=input()

            # 更新状态转移概率矩阵
            if huozhi=="1":#若已获知act的前置状态

                pre_state=[]
                
                pre_state_act=input("请输入前置状态包含的行为（输入完请输入0）：")
                while pre_state_act!="0":
                    pre_state.append(pre_state_act)
                    pre_state_act=input("请输入前置状态包含的行为（输入完请输入0）：")

                
                for translist in transmatrix:
                    if translist[0]==pre_state:
                        for i in translist[1:]:
                            if i[0]==[act]:
                                i[1]=1
                                break
                        else:
                            translist.append([[act],1,0])
            
                        break
            
                else:
                    transmatrix.append([pre_state,[[act],1,0]])

                want_learn_list1.remove(act)#在学习需求列表中删除已学习过的行为

        want_learn_list=want_learn_list1
    
        print("经过学习后，状态转移概率矩阵变为：",transmatrix)
    
    return transmatrix,want_learn_list

        
    
    


#主程序
print("苍穹3号已启动————————————————————")
while True:
        
    senlist=senpart(pactlist,senlist_add_actlist)
    memorylist=memorypart(senlist,memorylist)
    hapsum,sadsum,vsum,haphablist,sadhablist=valpart(haphablist,sadhablist,senlist,randforget,adjust_hapsadhablist)
    transmatrix,predict_state_chance,predict_max_state,predict_max_chance=worldmodel(transmatrix,psenlist,senlist)
    actlist,want_learn_list=actpart(psenlist,pactlist,acthablist,allact,senlist,vsum,adjust_acthablist,transmatrix,want_learn_list)
    transmatrix,want_learn_list=learnpart(transmatrix,actlist,want_learn_list)
    psenlist=senlist
    pactlist=actlist
    
    
    #若未进入不可变模式，询问是否保存当前心智内容
    if mode!="0":
        from pathlib import Path
        baocun=input("是否要保存当前记忆？（是：1，否：0）")
        if baocun=="1":
            #保存情绪习惯列表
            #保存喜习惯列表
            hapbbh=input("输入要保存的喜习惯列表的版本号：")
            hapwjlj="情绪习惯列表/喜习惯列表/喜习惯列表"+hapbbh+".txt"#喜习惯列表文件路径
            content=''
            for senlist_hap in haphablist:
                cont_senlist=''
                for i in senlist_hap[0]:
                    cont_senlist+=str(i)+"。"
                
                hap=senlist_hap[1]

                line=cont_senlist+"；"+str(hap)
                content+=str(line)+"\n"
            with open(hapwjlj,"w",encoding='utf-8') as hapfile:
                hapfile.write(content)
                
        
            #保存哀习惯列表
            sadbbh=input("输入要保存的哀习惯列表的版本号：")
            sadwjlj="情绪习惯列表/哀习惯列表/哀习惯列表"+sadbbh+".txt"#哀习惯列表文件路径
            content=''
            for senlist_sad in sadhablist:
                cont_senlist=''
                for i in senlist_sad[0]:
                    cont_senlist+=str(i)+"。"
                
                sad=senlist_sad[1]

                line=cont_senlist+"；"+str(sad)
                content+=str(line)+"\n"
            with open(sadwjlj,"w",encoding='utf-8') as sadfile:
                sadfile.write(content)

            #保存行为习惯列表
            acthabbbh=input("输入要保存的行为习惯列表的版本号：")
            acthabwjlj="行为习惯列表/行为习惯列表"+acthabbbh+".txt"
            content=''
            
            cont_ps=''
            cont_a=''
            
            for psav in acthablist:
                cont_ps=''
                cont_a=''
                for i in psav[0]:
                    cont_ps+=str(i)+"。"
                for i in psav[1]:
                    cont_a+=str(i)+"。"
                v=psav[2]

                line=cont_ps+"；"+cont_a+"；"+str(v)
                content+=str(line)+"\n"
            with open(acthabwjlj,"w",encoding='utf-8') as acthabfile:
                acthabfile.write(content)

            #保存自传体记忆
            memorybbh=input("输入要保存的自传体记忆的版本号：")
            memorywjlj="自传体记忆/自传体记忆"+memorybbh+".txt"
            content=''
            for senlist in memorylist:
                cont_senlist=''
                for i in senlist:
                    cont_senlist+=str(i)+"。"
                    
                line=cont_senlist
                content+=str(line)+"\n"
            with open(memorywjlj,"w",encoding='utf-8') as memoryfile:
                memoryfile.write(content)
            
            #保存状态转移概率矩阵
            transbbh=input("输入要保存的状态转移概率矩阵的版本号：")
            transwjlj="状态转移概率矩阵/状态转移概率矩阵"+transbbh+".txt"
            content=''
            for translist in transmatrix:
                cont_translist=''
                cont_translist+='。'.join(translist[0])
                for i in translist[1:]:
                    cont_translist+='；'+'。'.join(i[0])+"、"+str(i[1])+"、"+str(i[2])

                line=cont_translist
                content+=str(line)+"\n"
            
            with open(transwjlj,"w",encoding='utf-8') as transfile:
                transfile.write(content)



            print("保存成功——————————————")
