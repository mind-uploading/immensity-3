#初始化
#上一回合知觉概念列表
psenlist=[]
#上一回合行为概念列表
pactlist=[]
#知觉概念列表
senlist=[]

#设置
#1、随机遗忘机制
randforget=input("是否要激活随机遗忘机制？（是：1，否：0）")
if randforget=="1":
    print("【设置】随机遗忘机制已被激活")

#2、价值分类记忆激活阈值
#（一个新概念引发的价值发放如果超过阈值则该概念被纳入价值分类记忆）
print("接下来你将输入价值分类记忆激活阈值（范围0-5，通常为2）\n一个新概念引发的价值发放如果超过阈值则该概念被纳入价值分类记忆")
v_mem_threshold_hap=int(input("喜的价值分类记忆激活阈值："))
print("【设置】喜的价值分类记忆激活阈值：",v_mem_threshold_hap)
v_mem_threshold_sad=int(input("哀的价值分类记忆激活阈值："))
print("【设置】哀的价值分类记忆激活阈值：",v_mem_threshold_sad)


#3、行为固定化阈值v_goodact
#若vsum>=行为固定化阈值v_goodact，将当前行为模式固定化（存入goodact中）
print("接下来你将输入行为固定化阈值v_goodact（范围0-5，通常为1）\n若总价值vsum>=行为固定化阈值v_goodact，将当前行为模式固定化")
v_goodact=int(input("行为固定化阈值v_goodact："))
print("【设置】行为固定化阈值v_goodact：",v_goodact)

#4、行为调整激活阈值v_adjustact_threshold
#若总价值vsum<=行为调整激活阈值v_adjustact_threshold，在当前行为模式基础上进行优化
print("接下来你将输入行为调整激活阈值v_adjustact_threshold（范围0-5，通常为2）\n若总价值vsum<=行为调整激活阈值v_adjustact_threshold，在当前行为模式基础上进行优化")
v_adjustact_threshold=int(input("行为调整激活阈值v_adjustact_threshold："))
print("【设置】行为调整激活阈值v_adjustact_threshold：",v_adjustact_threshold)


#同步

#同步情绪列表

print("同步情绪列表--------------")
haplist=[]
hapbbh=input("输入要同步的喜列表的版本号：")
hapwjlj="情绪列表/喜列表/喜列表"+hapbbh+".txt"#喜列表文件路径

with open(hapwjlj,'r',encoding='utf-8') as hapfile:
    haps=hapfile.readline().strip()
    while haps:
        haplist.append(haps)
        haps=hapfile.readline().strip()
   
sadlist=[]
sadbbh=input("输入要同步的哀列表的版本号：")
sadwjlj="情绪列表/哀列表/哀列表"+sadbbh+".txt"#哀列表文件路径

with open(sadwjlj,'r',encoding='utf-8') as sadfile:
    sads=sadfile.readline().strip()
    while sads:
        sadlist.append(sads)
        sads=sadfile.readline().strip()



print("引发喜的知觉分类：",haplist)
print("引发哀的知觉分类：",sadlist)

#同步行为空间
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

#同步好行为列表goodact
print("同步好行为列表goodact----------------")
goodact=[]
goodactbbh=input("输入要同步的好行为列表的版本号：")
goodactwjlj="好行为列表/好行为列表"+goodactbbh+".txt"

with open(goodactwjlj,"r",encoding='utf-8') as goodactfile:
    hang=goodactfile.readline().strip()
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
        goodact.append([psav_p,psav_a,v])
        hang=goodactfile.readline().strip()
print("goodact:",goodact)


#上一回合行为列表
pactlist=[]
#行为列表
actlist=[]


def senpart(pactlist):#知觉分类模块
    print("知觉分类模块--------------------------------------------------")
    senlist=[]
    sen=input("知觉概念：（输入完请输入0）")
    while sen!="0":
        senlist.append(sen)
        sen=input("知觉概念：（输入完请输入0）")
    senlist+=pactlist  
    print("当前知觉概念列表：",senlist)
    return senlist



def valpart(haplist,sadlist,senlist):#价值分类记忆与价值系统
    print("价值分类记忆与价值系统--------------------------------------------------")
    import random
    #清零价值水平
    hap=0

    sad=0


    
    #输出当前知觉概念对应的价值
    for sen in senlist:
    
        if sen in haplist:
            hap+=1
            print(sen,"导致：喜")
        
        if sen in sadlist:
            sad+=1
            print(sen,"导致：哀")

    #价值水平不超过5
    if hap>5:
        hap=5
    if sad>5:
        sad=5
    print("喜x",hap)
    print("哀x",sad)    

    #将知觉概念与价值关联起来（将价值发放显著时的知觉概念加入引发该价值的概念列表中）
    if hap>=v_mem_threshold_hap:
        haplist.extend(senlist)

       
        
    if sad>=v_mem_threshold_sad:
        sadlist.extend(senlist)

        
    #价值分类记忆随机遗忘（引发该价值的概念列表中的元素每回合有1/10的概率被删除）
    if randforget=="1":
        for i in range(len(haplist)):
            if random.random()<0.1:
                haplist[i]=0
        nlst=[]
        for i in haplist:
            if i!=0:
                nlst.append(i)
        haplist=nlst

        for i in range(len(sadlist)):
            if random.random()<0.1:
                sadlist[i]=0
        nlst=[]
        for i in sadlist:
            if i!=0:
                nlst.append(i)
        sadlist=nlst

    #haplist、sadlist列表去重
    newhaplist=[]
    for i in haplist:
        if i not in newhaplist:
            newhaplist.append(i)
    haplist=newhaplist
    print(haplist)

    newsadlist=[]
    for i in sadlist:
        if i not in newsadlist:
            newsadlist.append(i)
    sadlist=newsadlist


    print("引发喜的知觉分类：",haplist)
   
    print("引发哀的知觉分类：",sadlist)
    vsum=hap-sad
    print("总价值：",vsum)
    return hap,sad,vsum,haplist,sadlist



def actpart(psenlist,pactlist,goodact,allact,senlist,vsum):#行为与计划模块
    print("行为与计划模块--------------------------------------------------")
    import random
    
            
    
    #根据价值调整行为模式

    #若当前行为模式已在goodact中
    zai=0
    for i in range(6):
        if [psenlist,pactlist,i] in goodact:
            #根据实践更新当前行为模式对应的vsum
            goodact.remove([psenlist,pactlist,i])
            vsum=round(0.7*vsum+0.3*i)#新的vsum为70%x当前的vsum+30%x原先的vsum(四舍五入)
            goodact.append([psenlist,pactlist,vsum])
            zai=1
    #若不在，如果vsum>=1，将当前行为模式固定化（存入goodact中）
    if zai==0:
        if vsum>=1:
            goodact.append([psenlist,pactlist,vsum])#goodact中存psav(psen-act-value),其中psen存上一回合知觉概念列表，act存上一回合行为概念列表，v存上一回合执行该行为后，本回合的vsum

    #优化行为模式
    #若vsum<=v_adjustact_threshold，在当前行为模式基础上进行优化(往相应的actlist中添加或删除随机行为，对应的vsum+1（对优化后的行为的价值持乐观预期）)
    if vsum<=v_adjustact_threshold:
        if random.random()<0.5:
            pactlist1=pactlist.copy()
            pactlist1.append(allact[random.randint(0, len(allact) - 1)])
            a=[psenlist,pactlist1,vsum+1]
            goodact.append(a)
           
        else:
            removeact=allact[random.randint(0, len(allact) - 1)]
            if removeact in pactlist:
                pactlist1=pactlist.copy()
                pactlist1.remove(removeact)
                a=[psenlist,pactlist1,vsum+1]
                goodact.append(a)
                

    #goodact列表去重
    newgoodact=[]
    for i in goodact:
        if i not in newgoodact:
            newgoodact.append(i)
    goodact=newgoodact


    print("行为模式列表：",goodact)



    #根据行为模式输出行为


    #若知觉概念组合存在于好行为列表中，输出这种知觉概念下导致价值发放最大的行为
    bestactlist=[]
    bestv=0
    for i in range(len(goodact)):
        psav=goodact[i]
       
        if senlist==psav[0]:
            actlist=psav[1]
            v=psav[2]
            if v>bestv:
                bestactlist=actlist
                bestv=v
            
    if bestv==0:#若不存在，随机输出行为
        act=allact[random.randint(0, len(allact) - 1)]
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
        
    senlist=senpart(pactlist)
    hap,sad,vsum,haplist,sadlist=valpart(haplist,sadlist,senlist)
    actlist=actpart(psenlist,pactlist,goodact,allact,senlist,vsum)
    psenlist=senlist
    pactlist=actlist
    
    #保存当前心智内容
    from pathlib import Path
    baocun=input("是否要保存当前记忆？（是：1，否：0）")
    if baocun=="1":
        #保存情绪列表
        #保存喜列表
        print(haplist)
        hapbbh=input("输入要保存的喜列表的版本号：")
        hapwjlj="情绪列表/喜列表/喜列表"+hapbbh+".txt"#喜列表文件路径
        content=''
        for i in haplist:
            content+=str(i)+"\n"
        with open(hapwjlj,"w",encoding='utf-8') as hapfile:
            hapfile.write(content)
        #保存哀列表
        sadbbh=input("输入要保存的哀列表的版本号：")
        sadwjlj="情绪列表/哀列表/哀列表"+sadbbh+".txt"#哀列表文件路径
        content=''
        for i in sadlist:
            content+=str(i)+"\n"
        with open(sadwjlj,"w",encoding='utf-8') as sadfile:
            sadfile.write(content)

        #保存行为空间
        allactbbh=input("输入要保存的行为空间的版本号：")
        allactwjlj="行为空间/行为空间"+allactbbh+".txt"
        content=''
        for i in allact:
            content+=str(i)+"\n"
        with open(allactwjlj,"w",encoding='utf-8') as allactfile:
            allactfile.write(content)

        #保存好行为列表
        goodactbbh=input("输入要保存的好行为列表的版本号：")
        goodactwjlj="好行为列表/好行为列表"+goodactbbh+".txt"
        content=''
        
        cont_ps=''
        cont_a=''
        
        for psav in goodact:
            cont_ps=''
            cont_a=''
            for i in psav[0]:
                cont_ps+=str(i)+"。"
            for i in psav[1]:
                cont_a+=str(i)+"。"
            v=psav[2]

            line=cont_ps+"；"+cont_a+"；"+str(v)
            content+=str(line)+"\n"
        with open(goodactwjlj,"w",encoding='utf-8') as goodactfile:
            goodactfile.write(content)


        print("保存成功——————————————")
