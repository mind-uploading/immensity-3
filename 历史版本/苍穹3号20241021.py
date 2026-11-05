#初始化
#上一回合知觉概念列表
psenlist=[]
#上一回合行为概念列表
pactlist=[]
#知觉概念列表
senlist=[]
#行为概念列表
actlist=[]


#设置
print("请进行设置------------------")

#是否进入不可变模式
unchange=input("是否进入不可变模式？（是：1，否：0）")
if unchange=="1":
    senlist_add_actlist="0"
    randforget="0"
    adjust_hapsadhablist="0"
    adjust_acthablist="0"
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

        senlisthap1=hang.split("；")#引发喜的概念列表（senlist）和该列表引发的喜的水平（hap）之间用“；”连接
        senlist=senlisthap1[0].split("。")#引发喜的概念列表内部的概念用“。”连接
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

        senlistsad1=hang.split("；")#引发哀的概念列表（senlist）和该列表引发的哀的水平（sad）之间用“；”连接
        senlist=senlistsad1[0].split("。")#引发哀的概念列表内部的概念用“。”连接
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



def actpart(psenlist,pactlist,acthablist,allact,senlist,vsum,adjust_acthablist):#行为与计划模块
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


    #若行为习惯列表中某些psen-a的psen是知觉概念列表的子集（这一步需要把列表转换成集合然后进行判断），输出这些psen-a下导致价值发放最大的a（行为概念列表）

    bestactlist=[]
    bestv=0
    for i in acthablist:
        psav=i
       
        if set(psav[0]).issubset(set(senlist)):
            actlist=psav[1]
            v=psav[2]
            if v>bestv:
                bestactlist=actlist
                bestv=v
            
    if bestv==0:#若不存在，随机输出行为
        act=random.choice(allact)
        actlist=[]
        actlist.append(act)
        print("当前精神图景下最优行为未知，输出随机行为：",actlist)

    else:
        actlist=bestactlist
        print("当前精神图景下最优行为：",actlist)


    return actlist



#主程序
print("苍穹3号已启动————————————————————")
while True:
        
    senlist=senpart(pactlist,senlist_add_actlist)
    hapsum,sadsum,vsum,haphablist,sadhablist=valpart(haphablist,sadhablist,senlist,randforget,adjust_hapsadhablist)
    actlist=actpart(psenlist,pactlist,acthablist,allact,senlist,vsum,adjust_acthablist)
    psenlist=senlist
    pactlist=actlist
    
    #若未进入不可变模式，询问是否保存当前心智内容
    if unchange=="0":
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


            print("保存成功——————————————")
