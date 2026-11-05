#引入第三方库
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import load_model
from PIL import Image
import io
import numpy as np
import pandas as pd
from minisom import *
import matplotlib.pyplot as plt
import os
import cv2
import time

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
#其他变量
hapsum=0
sadsum=0
vsum=0
predict_state_chance=[]
predict_max_state=''
predict_max_chance=0
act_detail_list=[]



#设置
print("请进行设置------------------")

#是否进入预设的模式
mode=input("是否进入预设的模式？（不可变模式：1，默认模式：2，自主模式：3，否：0）")
if mode=="1":
    senlist_add_actlist="0"
    randforget="0"
    adjust_hapsadhablist="0"
    adjust_acthablist="0"
elif mode=="2":
    senlist_add_actlist="0"
    randforget="0"
    adjust_hapsadhablist="1"
    hapsum_mem_threshold=2
    sadsum_mem_threshold=2
    adjust_acthablist="1"
    v_acthab_threshold=1
    v_adjustact_threshold=-1
elif mode=="3":
    senlist_add_actlist="0"
    randforget="0"
    adjust_hapsadhablist="1"
    hapsum_mem_threshold=2
    sadsum_mem_threshold=2
    adjust_acthablist="1"
    v_acthab_threshold=1
    v_adjustact_threshold=-1
    sleeptime=int(input("请输入两个回合之间的睡眠时间（单位：秒）："))
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

#加载CNN和SOM模型
base_model = load_model('知觉分类模块/CNN/vgg16_base_model.h5')

sombbh=input("输入要同步的SOM的版本号：")
somwjlj="知觉分类模块/SOM/SOM"+sombbh+".p"
with open(somwjlj, 'rb') as infile:
    som = pickle.load(infile)



print("同步完成--------------")


#各个模块

def senpart(senlist,pactlist,senlist_add_actlist):#知觉分类模块
    print("知觉分类模块--------------------------------------------------")
    
    #清空senlist
    senlist=[]
    

    if mode=="3":#若进入自主模式
        #将摄像头拍摄的图像转化为知觉概念


        #拍摄图像并预处理

        # 如果是调用笔记本自带的摄像头，参数就为0；如果是外置USB摄像头，参数就为1。
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        # 设置一下摄像头窗口的宽高，参数3代表宽度
        cap.set(3, 128)
        # 参数4代表的高度
        cap.set(4, 128)
        # 参数10代表亮度
        cap.set(10, 100)
        success=False
        while success == False:
            success, img = cap.read()
        frame = cv2.flip(img, 1)
        # show a frame
        cv2.imshow('frame', frame)
        # 设置拍摄图像的保存路径，不设置默认为当前目录
        cv2.imwrite("pic.png", frame)
        # 准备图像数据
        img_resized = cv2.resize(cv2.imread("pic.png"), (128, 128))  # 调整图像尺寸为 (128, 128)
        img_array = np.array(img_resized)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)


        # 图片映射为特征

        features = base_model.predict(img_array)
        features = features.flatten()  # 展平特征向量

        
        #特征会激活SOM网络中位于（i，j）的神经元，该神经元会发放概念（i，j）

        # 更新 SOM
        som.train_random(features.reshape(1, -1), num_iteration=1)

        # 获取获胜神经元在SOM网络中的位置（i，j）
        winning_neurons_position = som.winner(features) 


        #把概念（i，j）添加到senlist中
        
        posstr="（"+str(winning_neurons_position[0])+" "+str(winning_neurons_position[1])+"）"
        sen="概念"+posstr
        senlist.append(sen)


    else:#若没进入自主模式
        #接收输入的知觉概念列表
        while True:
            root.update()
            if varcbinputsen1.get()==1 and varcbinputsen2.get()==1:
                senlist=entinputsen.get().split(" ")
                break
            import time
            time.sleep(0.1)
       

    if senlist_add_actlist=="1":#若启用“将上一回合输出的行为概念加入下一回合的知觉概念列表中”的机制
        senlist.extend(pactlist)


    #print("当前知觉概念列表：",senlist)
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
            hapsum+=int(i[1])

    for i in sadhablist:
        if set(i[0]).issubset(set(senlist)):
            sadsum+=int(i[1])
    #各喜/哀的水平hap/sum和总的喜/哀的水平hapsum/sadsum的取值范围：0-5

    if hapsum>5:
        hapsum=5
    if sadsum>5:
        sadsum=5
    #print("喜x",hapsum)
    #print("哀x",sadsum)    

    vsum=hapsum-sadsum
    #print("总价值：",vsum)
    
    
    
    #情绪习惯列表的更新

    if adjust_hapsadhablist=="1":#若允许调整情绪习惯列表

        #价值分类记忆的强化
        #当该情绪习惯被激活，该情绪习惯的情绪值有1/5的概率+1
        for i in haphablist:
            if set(i[0]).issubset(set(senlist)):
                if random.random()<0.2:
                    i[1]+=1
                    if i[1]>5:
                        i[1]=5
            
        for i in sadhablist:
            if set(i[0]).issubset(set(senlist)):
                if random.random()<0.2:
                    i[1]+=1
                    if i[1]>5:
                        i[1]=5    
            
        
        #根据状态转移概率矩阵更新情绪习惯列表
        haphablist1=[]
        for i in haphablist:#对于情绪习惯列表中的每一个senlist，在状态转移概率矩阵中查找其前置状态。
            for j in transmatrix:
                for k in j[1:]:
                    if k[0]==i[0] and k[1]>0.8:#若前置状态引发该senlist的概率大于0.8，将该前置状态加入情绪习惯列表中（该前置状态产生的情绪值为其引起的senlist的情绪值-1）
                        haphablist1.append([j[0],i[1]-1])
        haphablist.extend(haphablist1)
        
        sadhablist1=[]
        for i in sadhablist:#对于情绪习惯列表中的每一个senlist，在状态转移概率矩阵中查找其前置状态。
            for j in transmatrix:
                for k in j[1:]:
                    if k[0]==i[0] and k[1]>0.8:#若前置状态引发该senlist的概率大于0.8，将该前置状态加入情绪习惯列表中（该前置状态产生的情绪值为其引起的senlist的情绪值-1）
                        sadhablist1.append([j[0],i[1]-1])
        sadhablist.extend(sadhablist1)
        

       
    #价值分类记忆随机遗忘
    #情绪习惯列表中的每个senlist-hap/sad的hap/sad在每回合都有1/100的概率被下调1,若降至0以下则该组senlist-hap/sad被删除
    if randforget=="1":#若启用随机遗忘机制
        for i in haphablist:
            if random.random()<0.01:
                i[1]-=1
                if i[1]<0:
                    i[1]=0
                    
        for i in sadhablist:
            if random.random()<0.01:
                i[1]-=1
                if i[1]<0:
                    i[1]=0
    
    
    
    #print("情绪习惯列表：")  
    #print("（结构：[[senlist1，hap1/sad1],[senlist2，hap2/sad2],...]）")
    #print("喜习惯列表：",haphablist)
    #print("哀习惯列表：",sadhablist)

    
    return hapsum,sadsum,vsum,haphablist,sadhablist



def actpart(psenlist,pactlist,acthablist,allact,senlist,vsum,adjust_acthablist,transmatrix,want_learn_list,haphablist,sadhablist):#行为与计划模块
    print("行为与计划模块--------------------------------------------------")
    import random
    
            
    if adjust_acthablist=="1":#若允许调整行为习惯列表
        
        #根据实践结果更新acthablist中的psav组

        for psav in acthablist:#若acthablist中原来就有相应的psav组
            if psav[0]==psenlist and psav[1]==pactlist:
                vsum=round(0.7*vsum+0.3*psav[2])#新的vsum为70%x当前的vsum+30%x原先的vsum(四舍五入)
                acthablist.remove(psav)#删除acthablist中原有的psav组
        acthablist.append([psenlist,pactlist,vsum])#将新的psav组添加入acthablist
        
        
        #根据价值调整行为习惯列表

      
        #若总价值vsum<=行为调整激活阈值v_adjustact_threshold，在当前psen-act基础上进行优化：
			
        #在状态转移概率矩阵中搜索当前psen与哪些act结合后，导致的新状态的vsum最高（需高于v_adjustact_threshold，不然不算数），并用这个act更新psen-act中原来那个act，用这个psen-act导致的新状态的vsum更新vsum

        # （往当前psen-act的act（实际上是actlist）中添加或删除随机行为，将对应的vsum改为v_adjustact_threshold+1（对优化后的行为的价值持乐观预期））

        if vsum<=v_adjustact_threshold:

            #在状态转移概率矩阵中搜索当前psen与哪些act结合后，导致的结果的vsum最高（需高于v_adjustact_threshold，不然不算数）
            #并用这个act更新psen-act中原来那个act，用这个psen-act导致的结果的vsum更新vsum
            
            pactlist1=[]#pactlist1是更新后的act
            vsum1=0
            
            for translist in transmatrix:

                #判断translist[0]-psenlist的差集是否被allact包含，即判断translist[0]中除了psenlist外，是否有做不到的行为
                zuobudao=0
                diffset=[]
                for i in translist[0]:
                    if i not in psenlist:
                        diffset.append(i)
                for i in diffset:
                    if i not in allact:
                        zuobudao=1
                        break
                if zuobudao==0:
                    #判断psenlist是否⊂translist[0]
                    for psen in psenlist:
                        if psen not in translist[0]:
                            break
                    else:#没有执行break说明psenlist⊂translist[0]且translist[0]中除了psenlist外，没有做不到的行为
                        
                        #查询导致的结果
                        result=[]
                        for state_chance_times in translist[1:]:
                            next_state=[]
                            if state_chance_times[1]>=0.5:
                                result.extend(state_chance_times[0])
                            
                        #接下来根据情绪习惯列表查询导致的结果的vsum:
                        
                        #清零总的喜/哀的水平hapsum/sadsum
                        hapsum=0
                        sadsum=0
                        #输出当前知觉概念列表对应的价值
                        for i in haphablist:
                            if set(i[0]).issubset(set(result)):
                                hapsum+=int(i[1])

                        for i in sadhablist:
                            if set(i[0]).issubset(set(result)):
                                sadsum+=int(i[1])
                    
                        #各喜/哀的水平hap/sum和总的喜/哀的水平hapsum/sadsum的取值范围：0-5
                        if hapsum>5:
                            hapsum=5
                        if sadsum>5:
                            sadsum=5

                        vsum=hapsum-sadsum

                        #选取导致的结果的vsum最高的那个行为
                        if vsum>vsum1:
                            vsum1=vsum
                            pactlist1=diffset
            
            
            #若搜索到符合要求的act，用这个act更新psen-act中原来那个act，用这个psen-act导致的结果的vsum更新vsum
            if vsum1>v_adjustact_threshold and pactlist1!=[]:
                a=[psenlist,pactlist1,vsum1]
                acthablist.append(a)
               

            #若未搜索到符合要求的act，往当前psen-act的act（实际上是actlist）中添加或删除随机行为，将对应的vsum改为v_adjustact_threshold+1（对优化后的行为的价值持乐观预期）
            if vsum1<=v_adjustact_threshold or pactlist1==[]:
                if random.random()<0.5:
                    pactlist1=pactlist.copy()
                    pactlist1.append(random.choice(list(allact)))
                   
                
                else:
                    if pactlist!=[]:
                        removeact=pactlist[random.randint(0, len(pactlist) - 1)]
            
                        pactlist1=pactlist.copy()
                        pactlist1.remove(removeact)
                       
                    
                a=[psenlist,pactlist1,v_adjustact_threshold+1]
                acthablist.append(a)
                

        #删除自发行为
        acthablist1=[]
        for psav in acthablist:
            if psav[0]!=[]:
                acthablist1.append(psav)
        acthablist=acthablist1
        
    #print("行为习惯列表：",acthablist)



    #根据行为习惯输出行为
    actlist=[]
    find=False
    
    #step0、如果senlist=想+某行为，输出该行为

    for sen in senlist:
        if sen!="":
            if sen[0]=="想":
                actlist.extend([sen[1:]])
                find=True#表示step0中找到了符合要求的行为
                print("step0中找到符合“senlist=想+某行为”要求的行为")

    #step1、遍历acthablist，若其中某些psav组的psen=senlist（知觉概念列表），判断这些psav组的v是否大于0，输出v大于0的那些psav组中的act（行为概念列表）

    if find==False:
        for psav in acthablist:
            if sorted(psav[0])==sorted(senlist):
                if psav[2]>0:
                    actlist.extend(psav[1])
                    find=True#表示step1中找到了符合要求的psav组
                    #print("step1中找到符合“psen=senlist”要求的psav组")
                    
    #step2、若step1中未找到符合要求的psav组，扩大搜索范围：遍历acthablist，若某些psav组的psen⊂senlist，判断这些psav组的v是否大于0，输出v大于0的那些psav组中的act

    if find==False:
        #print("step1中未找到符合“psen=senlist”要求的psav组")
        for psav in acthablist:
            for i in psav[0]:
                if i not in senlist:
                    break
            else:
                actlist.extend(psav[1])
                find=True#表示step2中找到了符合要求的psav组
                #print("step2中找到符合“psen⊂senlist”要求的psav组")

    #step3、若step1和step2中都未找到符合要求的psav组，则不输出行为

    if find==False:
        print("step1和step2中都未找到符合要求的psav组，当前精神图景下最优行为未知，不输出行为")
        

    #行为和负行为相互抵消
    for act in actlist:
        if act!="":
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
        
    #print("当前精神图景下最优行为：",actlist)

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
        content+=str(line)+"\n"*2
    txacthablist.configure(state='normal')
    txacthablist.delete(0.0,'end')
    txacthablist.insert(0.0,content)
    txacthablist.configure(state='disabled')
    
    lbactlist.configure(text="当前精神图景下最优行为："+','.join(actlist))
    txact_detail_list.configure(state='normal')
    txact_detail_list.delete(0.0,'end')
    txact_detail_list.configure(state='disabled')



    


  

    #对行为进行分解细化

    counts=0
    if mode!="3":#若未进入不可变模式
        while True:
            root.update()
            if varcbcounts1.get()==1 and varcbcounts2.get()==1:
                counts=int(entcounts.get())
                varcbcounts1.set(0)
                varcbcounts2.set(0)
                break
            import time
            time.sleep(0.1)
    '''
    counts=0
    if actlist!=[]:
        counts=int(input("分解次数:"))
    '''

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
        
        #print("行为细化后：",act_detail_list)



    #对学习需求列表进行去重
    list1=[]
    for i in want_learn_list:
        if i not in list1:
            list1.append(i)
    want_learn_list=list1

    #输出学习需求列表
    if want_learn_list!=[]:
        print("需要学习以下行为：",want_learn_list)
        





    return actlist,act_detail_list,want_learn_list


def memorypart(senlist,memorylist):#记忆模块
    print("记忆模块--------------------------------------------------")
    memorylist.append(senlist)
    #print("截至目前的自传体记忆为：",memorylist)

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


    #print("截至目前的状态转移概率矩阵为：",transmatrix)
    
    
    #根据状态转移概率矩阵预测接下来各状态的发生概率，以及最可能发生的状态
    predict_state_chance=[]
    predict_max_chance=0
    predict_max_state="未发现"
    
    for translist in transmatrix:
        if translist[0]==senlist:
            predict_state_chance=translist[1:]#接下来各状态的发生概率
            #print("接下来各状态发生概率为：",predict_state_chance)
            
            
            for i in translist[1:]:
                if i[1]>predict_max_chance:
                    predict_max_chance=i[1]
                    predict_max_state=i[0]
            #print("接下来最可能发生的状态为：",predict_max_state,"发生概率为：",predict_max_chance)

            break
    else:
        #print("未在状态转移概率矩阵中发现当前知觉概念列表所对应的接下来的状态")
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

            from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
            from sparkai.core.messages import ChatMessage

            #星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
            SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
            #星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
            SPARKAI_APP_ID = '6453e52c'
            SPARKAI_API_SECRET = 'MDYzMGRjMzNlNDU0YzM1MzRiYTlkYWVj'
            SPARKAI_API_KEY = 'ffa30420efed3f39f266221e36863873'
            #星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
            SPARKAI_DOMAIN = 'generalv3.5'

            if __name__ == '__main__':
                spark = ChatSparkLLM(
                    spark_api_url=SPARKAI_URL,
                    spark_app_id=SPARKAI_APP_ID,
                    spark_api_key=SPARKAI_API_KEY,
                    spark_api_secret=SPARKAI_API_SECRET,
                    spark_llm_domain=SPARKAI_DOMAIN,
                    streaming=False,
                )
                messages = [ChatMessage(
                    role="user",
                    content='请列出'+act+'前的所有必要步骤，并用中文逗号隔开每个步骤，回答中不要出现其他任何内容，回答的末尾不要加句号'
                )]
                handler = ChunkPrintHandler()
                response = spark.generate([messages], callbacks=[handler]).generations[0][0].text
                print("大模型的回答：",response)

            #处理大模型的回答
            response=response.split(sep="，")
            



            
           
            
            # 更新状态转移概率矩阵
           

            pre_state=response
        
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

        #更新学习需求列表
        want_learn_list=want_learn_list1
    
        print("经过学习后，状态转移概率矩阵变为：",transmatrix)
    
    return transmatrix,want_learn_list

        
    
    


#主程序
print("苍穹3号已启动————————————————————")


#全局神经工作空间GW及其内容的可视化（GUI）
from tkinter import *
root=Tk()
root.title("苍穹3号")
root.geometry('1000x800')


lbGW=Label(root,text="全局神经工作空间GW")
lbGW.grid(row=0,column=1)



lbsenpart=Label(root,text="知觉分类模块")
lbsenpart.grid(row=1,column=0)
lbinputsen=Label(root,text="输入当前知觉概念列表,各知觉概念之间用空格隔开。（若输入：想+某行为，系统将会输出该行为）")
lbinputsen.grid(row=2,column=0)
entinputsen=Entry(root,width=40)
entinputsen.grid(row=3,column=0)

varcbinputsen1=IntVar()
varcbinputsen2=IntVar()
cbinputsen1=Checkbutton(root,text="知觉概念列表准备完毕",variable=varcbinputsen1,onvalue=1,offvalue=0)
cbinputsen1.grid(row=4,column=0)
cbinputsen2=Checkbutton(root,text="提交知觉概念列表",variable=varcbinputsen2,onvalue=1,offvalue=0)
cbinputsen2.grid(row=5,column=0)

lbsenlist=Label(root,text="当前知觉概念列表")
lbsenlist.grid(row=6,column=0)
txsenlist=Text(root,width=40,height=5)
txsenlist.grid(row=7,column=0)

varcbbaocun1=IntVar()
varcbbaocun2=IntVar()
cbbaocun1=Checkbutton(root,text="保存当前记忆",variable=varcbbaocun1,onvalue=1,offvalue=0)
cbbaocun1.grid(row=8,column=0)
cbbaocun2=Checkbutton(root,text="确认保存当前记忆",variable=varcbbaocun2,onvalue=1,offvalue=0)
cbbaocun2.grid(row=9,column=0)


lbmemorypart=Label(root,text="记忆模块")
lbmemorypart.grid(row=1,column=1)
lbmemorylist=Label(root,text="自传体记忆")
lbmemorylist.grid(row=2,column=1)
txmemorylist=Text(root,width=20,height=5)
txmemorylist.grid(row=3,column=1)



lbvalpart=Label(root,text="价值分类记忆与价值系统")
lbvalpart.grid(row=1,column=2)
lbhapsum=Label(root,text="喜的值:")
lbhapsum.grid(row=2,column=2)
lbsadsum=Label(root,text="哀的值:")
lbsadsum.grid(row=3,column=2)
lbvsum=Label(root,text="总价值:")
lbvsum.grid(row=4,column=2)
lbhapsadhablist=Label(root,text="情绪习惯列表")
lbhapsadhablist.grid(row=5,column=2)
lbhaphablist=Label(root,text="喜习惯列表")
lbhaphablist.grid(row=6,column=2)
txhaphablist=Text(root,width=20,height=5)
txhaphablist.grid(row=7,column=2)
lbsadhablist=Label(root,text="哀习惯列表")
lbsadhablist.grid(row=8,column=2)
txsadhablist=Text(root,width=20,height=5)
txsadhablist.grid(row=9,column=2)



lbworldmodel=Label(root,text="世界模型")
lbworldmodel.grid(row=4,column=1)
lbtransmatrix=Label(root,text="状态转移概率矩阵")
lbtransmatrix.grid(row=5,column=1)
txtransmatrix=Text(root,width=40,height=5)
txtransmatrix.grid(row=6,column=1)
lbpredict_state_chance=Label(root,text="接下来各状态发生概率为：")
lbpredict_state_chance.grid(row=7,column=1)
txpredict_state_chance=Text(root,width=20,height=5)
txpredict_state_chance.grid(row=8,column=1)
lbpredict_max_state=Label(root,text="接下来最可能发生的状态为:")
lbpredict_max_state.grid(row=9,column=1)
lbpredict_max_chance=Label(root,text="发生概率为:")
lbpredict_max_chance.grid(row=10,column=1)



lbactpart=Label(root,text="行为与计划模块")
lbactpart.grid(row=1,column=3)
lbacthablist=Label(root,text="行为习惯列表")
lbacthablist.grid(row=2,column=3)
txacthablist=Text(root,width=40,height=10)
txacthablist.grid(row=3,column=3)
lbactlist=Label(root,text="当前精神图景下最优行为：")
lbactlist.grid(row=4,column=3)
lbcounts=Label(root,text="行为的分解次数：（输入一个>=0的整数）")
lbcounts.grid(row=5,column=3)
entcounts=Entry(root,width=10)
entcounts.grid(row=6,column=3)
varcbcounts1=IntVar()
varcbcounts2=IntVar()
cbcounts1=Checkbutton(root,text="行为分解次数输入完毕",variable=varcbcounts1,onvalue=1,offvalue=0)
cbcounts1.grid(row=7,column=3)
cbcounts2=Checkbutton(root,text="提交行为分解次数",variable=varcbcounts2,onvalue=1,offvalue=0)
cbcounts2.grid(row=8,column=3)
lbact_detail_list=Label(root,text="行为细化后：")
lbact_detail_list.grid(row=9,column=3)
txact_detail_list=Text(root,width=40,height=5)
txact_detail_list.grid(row=10,column=3)


while True:
    
    root.update()
    senlist=senpart(senlist,pactlist,senlist_add_actlist)

    varcbinputsen1.set(0)
    varcbinputsen2.set(0)
    senliststr=','.join(senlist)
    txsenlist.configure(state='normal')
    txsenlist.delete(0.0,'end')
    txsenlist.insert(0.0,senliststr)
    txsenlist.configure(state='disabled')


    memorylist=memorypart(senlist,memorylist)

    memoryliststr=""
    for i in memorylist:
        memoryliststr+=','.join(i)+"\n"*2
    txmemorylist.configure(state='normal')
    txmemorylist.delete(0.0,'end')
    txmemorylist.insert(0.0,memoryliststr)
    txmemorylist.configure(state='disabled')


    hapsum,sadsum,vsum,haphablist,sadhablist=valpart(haphablist,sadhablist,senlist,randforget,adjust_hapsadhablist)

    lbhapsum.configure(text="喜的值:"+str(hapsum))
    lbsadsum.configure(text="哀的值:"+str(sadsum))
    lbvsum.configure(text="总价值:"+str(vsum))
    
    content=''
    for senlist_hap in haphablist:
        cont_senlist=''
        for i in senlist_hap[0]:
            cont_senlist+=str(i)+"。"
        
        hap=senlist_hap[1]

        line=cont_senlist+"；"+str(hap)
        content+=str(line)+"\n"*2
    txhaphablist.configure(state='normal')
    txhaphablist.delete(0.0,'end')
    txhaphablist.insert(0.0,content)
    txhaphablist.configure(state='disabled')
    
    content=''
    for senlist_sad in sadhablist:
        cont_senlist=''
        for i in senlist_sad[0]:
            cont_senlist+=str(i)+"。"
        
        sad=senlist_sad[1]

        line=cont_senlist+"；"+str(sad)
        content+=str(line)+"\n"*2
    txsadhablist.configure(state='normal')
    txsadhablist.delete(0.0,'end')
    txsadhablist.insert(0.0,content)
    txsadhablist.configure(state='disabled')


    transmatrix,predict_state_chance,predict_max_state,predict_max_chance=worldmodel(transmatrix,psenlist,senlist)

    content=''
    for translist in transmatrix:
        cont_translist=''
        cont_translist+='。'.join(translist[0])
        for i in translist[1:]:
            cont_translist+='；'+'。'.join(i[0])+"、"+str(i[1])+"、"+str(i[2])

        line=cont_translist
        content+=str(line)+"\n"*2
    txtransmatrix.configure(state='normal')
    txtransmatrix.delete(0.0,'end')
    txtransmatrix.insert(0.0,content)
    txtransmatrix.configure(state='disabled')

    txpredict_state_chance.configure(state='normal')
    txpredict_state_chance.delete(0.0,'end')
    if predict_state_chance=="未发现":
        txpredict_state_chance.insert(0.0,"未发现")
    else:
        content=''
        for i in predict_state_chance:
            content+='。'.join(i[0])+"、"+str(i[1])+"、"+str(i[2])+"\n"*2
        txpredict_state_chance.insert(0.0,content)
    txpredict_state_chance.configure(state='disabled')
    
    if predict_state_chance=="未发现":
        lbpredict_max_state.configure(text="接下来最可能发生的状态为:未发现")
    else:
        lbpredict_max_state.configure(text="接下来最可能发生的状态为:"+",".join(predict_max_state))
    lbpredict_max_chance.configure(text="发生概率为:"+str(predict_max_chance))
    

    actlist,act_detail_list,want_learn_list=actpart(psenlist,pactlist,acthablist,allact,senlist,vsum,adjust_acthablist,transmatrix,want_learn_list,haphablist,sadhablist)
    
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
        content+=str(line)+"\n"*2
    txacthablist.configure(state='normal')
    txacthablist.delete(0.0,'end')
    txacthablist.insert(0.0,content)
    txacthablist.configure(state='disabled')
    
    lbactlist.configure(text="当前精神图景下最优行为："+','.join(actlist))
    txact_detail_list.configure(state='normal')
    txact_detail_list.delete(0.0,'end')
    txact_detail_list.insert(0.0,','.join(act_detail_list))
    txact_detail_list.configure(state='disabled')



    
    transmatrix,want_learn_list=learnpart(transmatrix,actlist,want_learn_list)


    psenlist=senlist
    pactlist=actlist


    
    #若未进入不可变模式，询问是否保存当前心智内容
    if mode!="0":
        from pathlib import Path
        #baocun=input("是否要保存当前记忆？（是：1，否：0）")
        if varcbbaocun1.get()==1 and varcbbaocun2.get()==1:
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


            #保存SOM模型
            sombbh=input("输入要保存的SOM模型的版本号：")
            somwjlj="知觉分类模块/SOM/SOM"+sombbh+".p"
            with open(somwjlj, 'wb') as outfile:
                pickle.dump(som, outfile)




            print("保存成功——————————————")
            varcbbaocun1.set(0)
            varcbbaocun2.set(0)
    
    if mode=="3":
        time.sleep(sleeptime)
