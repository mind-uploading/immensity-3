#初始化
#上一回合知觉概念列表
psenlist=[]
#知觉概念列表
senlist=[]

#同步情绪列表
print("同步情绪列表--------------")
haplist=[]
sadlist=[]
haps=input("输入引发喜的知觉、行为分类：（输入完请输入0）")
while haps!="0":
    haplist.append(haps)
    haps=input("输入引发喜的知觉、行为分类：（输入完请输入0）")


sads=input("输入引发悲的知觉、行为分类：（输入完请输入0）")
while sads!="0":
    sadlist.append(sads)
    sads=input("输入引发悲的知觉、行为分类：（输入完请输入0）")


print("引发喜的知觉分类：",haplist)

print("引发哀的知觉分类：",sadlist)

#同步行为空间
print("同步行为空间---------------")
allact=[]
acts=input("输入所有可能的行为：（输入完请输入0）")
while acts!="0":
    allact.append(acts)
    acts=input("输入所有可能的行为：（输入完请输入0）")
print("行为空间：",allact)
#同步好行为列表goodact
print("同步好行为列表goodact----------------")
goodact=[]
print("goodact:",goodact)
i=input("是否还要输入psav:（是：1，否：0）")
while i!="0":
    psav_p=[]
    p=input("知觉分类：（输入完请输入0）")
    while p!="0":
        psav_p.append(p)
        p=input("知觉分类：（输入完请输入0）")
    psav_a=[]
    a=input("行为：（输入完请输入0）")
    while a!="0":
        psav_a.append(a)
        a=input("行为：（输入完请输入0）")
    v=int(input("价值：（取值范围0-5）"))
    print("psav:",[psav_p,psav_a,v])
    goodact.append([psav_p,psav_a,v])
    print("goodact:",goodact)
    i=input("是否还要输入psav:（是：1，否：0）")


#上一回合行为列表
pactlist=[]
#行为列表
actlist=[]


def senpart():#知觉分类模块
    print("知觉分类模块--------------------------------------------------")
    senlist=[]
    sen=input("知觉概念：（输入完请输入0）")
    while sen!="0":
        senlist.append(sen)
        sen=input("知觉概念：（输入完请输入0）")
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
            print(sen,"导致：悲")

    #价值水平不超过5
    if hap>5:
        hap=5
    if sad>5:
        sad=5
    print("喜x",hap)
    print("悲x",sad)    

    #将知觉概念与价值关联起来（将价值发放显著时的知觉概念加入引发该价值的概念列表中）
    if hap>=2:
        haplist.extend(senlist)

       
        
    if sad>=2:
        sadlist.extend(senlist)
    #价值分类记忆随机遗忘（引发该价值的概念列表中的元素每回合有1/10的概率被删除）
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

    newsadlist=[]
    for i in sadlist:
        if i not in newsadlist:
            newsadlist.append(i)
    sadlist=newsadlist


    print("引发喜的知觉分类：",haplist)
   
    print("引发哀的知觉分类：",sadlist)
    vsum=hap-sad
    print("总价值：",vsum)
    return hap,sad,vsum



def actpart(psenlist,pactlist,goodact,allact,senlist,vsum):#行为与计划模块
    print("行为与计划模块--------------------------------------------------")
    import random
    
            
    
    #根据价值调整行为模式

    for i in range(6):
        #若当前行为模式已在goodact中
        if [psenlist,pactlist,i] in goodact:
            #根据实践更新当前行为模式对应的vsum
            goodact.remove([psenlist,pactlist,i])
            vsum=round(0.7*vsum+0.3*i)#新的vsum为70%x当前的vsum+30%x原先的vsum(四舍五入)
            goodact.append([psenlist,pactlist,vsum])

        #若不在，如果vsum>=1，将当前行为模式固定化（存入goodact中）
        elif vsum>=1:
            goodact.append([psenlist,pactlist,vsum])#goodact中存psav(psen-act-value),其中psen存上一回合知觉概念列表，act存上一回合行为概念列表，v存上一回合执行该行为后，本回合的vsum

        #优化行为模式
        #若vsum<=2，在当前行为模式基础上进行优化(往相应的actlist中添加或删除随机行为，对应的vsum+1（对优化后的行为的价值持乐观预期）)
        if vsum<=2:
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
print("意识引擎启动————————————————————")
while True:
    senlist=senpart()
    hap,sad,vsum=valpart(haplist,sadlist,senlist)
    actlist=actpart(psenlist,pactlist,goodact,allact,senlist,vsum)
    psenlist=senlist
    pactlist=actlist
   
