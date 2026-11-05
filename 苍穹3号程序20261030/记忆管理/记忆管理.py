#记忆管理（心智内容的同步与保存）
import pandas as pd

import 公共状态


#同步（从文件加载心智内容）
def 同步记忆():
    #同步情绪习惯
    print("同步情绪习惯列表--------------")
    公共状态.haphablist=[]
    hapbbh=input("输入要同步的喜习惯列表的版本号：")
    hapwjlj="意识数据/情绪习惯列表/喜习惯列表/喜习惯列表"+hapbbh+".txt"#喜习惯列表文件路径

    with open(hapwjlj,'r',encoding='utf-8') as hapfile:
        hang=hapfile.readline().strip()
        while hang:

            senlisthap1=hang.split("；")#引发喜的知觉概念列表（senlist）和该列表引发的喜的水平（hap）之间用“；”连接
            senlist=senlisthap1[0].split("。")#引发喜的知觉概念列表内部的概念用“。”连接
            hap=int(senlisthap1[1])
            #删除切片出的空内容
            while "" in senlist:
                senlist.remove("")

            公共状态.haphablist.append([senlist,hap])
            hang=hapfile.readline().strip()

    公共状态.sadhablist=[]
    sadbbh=input("输入要同步的哀习惯列表的版本号：")
    sadwjlj="意识数据/情绪习惯列表/哀习惯列表/哀习惯列表"+sadbbh+".txt"#哀习惯列表文件路径

    with open(sadwjlj,'r',encoding='utf-8') as sadfile:
        hang=sadfile.readline().strip()
        while hang:

            senlistsad1=hang.split("；")#引发哀的知觉概念列表（senlist）和该列表引发的哀的水平（sad）之间用“；”连接
            senlist=senlistsad1[0].split("。")#引发哀的知觉概念列表内部的概念用“。”连接
            sad=int(senlistsad1[1])
            #删除切片出的空内容
            while "" in senlist:
                senlist.remove("")

            公共状态.sadhablist.append([senlist,sad])
            hang=sadfile.readline().strip()

    print("情绪习惯列表：")
    print("（结构：[[senlist1，hap1/sad1],[senlist2，hap2/sad2],...]）")
    print("喜习惯列表：",公共状态.haphablist)
    print("哀习惯列表：",公共状态.sadhablist)

    #同步行为空间（这是一个列表）
    print("同步行为空间---------------")
    公共状态.allact=[]
    allactbbh=input("输入要同步的行为空间的版本号：")
    allactwjlj="意识数据/行为空间/行为空间"+allactbbh+".txt"


    with open(allactwjlj,"r",encoding='utf-8') as allactfile:
        acts=allactfile.readline().strip()
        while acts:
            公共状态.allact.append(acts)
            acts=allactfile.readline().strip()
    print("行为空间：",公共状态.allact)

    #同步行为习惯列表acthablist
    print("同步行为习惯列表acthablist----------------")
    公共状态.acthablist=[]
    acthabbbh=input("输入要同步的行为习惯列表的版本号：")
    acthabwjlj="意识数据/行为习惯列表/行为习惯列表"+acthabbbh+".txt"

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
            公共状态.acthablist.append([psav_p,psav_a,v])
            hang=acthabfile.readline().strip()
    print("行为习惯列表acthablist:",公共状态.acthablist)

    #同步自传体记忆
    print("同步自传体记忆----------------")
    公共状态.memorylist=[]
    memorylistbbh=input("输入要同步的自传体记忆的版本号：")
    memorylistwjlj="意识数据/自传体记忆/自传体记忆"+memorylistbbh+".txt"#自传体记忆文件路径

    with open(memorylistwjlj,'r',encoding='utf-8') as memorylistfile:
        hang=memorylistfile.readline().strip()
        while hang:

            senlist_actlist_vsum=hang.split("；")#senlist、actlist、vsum之间用“；”连接
            senlist=senlist_actlist_vsum[0].split("。")#senlist内部的概念用“。”连接
            actlist=senlist_actlist_vsum[1].split("。")#actlist内部的概念用“。”连接
            vsum=int(senlist_actlist_vsum[2])
            #删除切片出的空内容
            while "" in senlist:
                senlist.remove("")
            while "" in actlist:
                actlist.remove("")

            公共状态.memorylist.append([senlist,actlist,vsum])
            hang=memorylistfile.readline().strip()

    print("自传体记忆：",公共状态.memorylist)

    #同步状态转移概率矩阵
    print("同步状态转移概率矩阵----------------")
    公共状态.transmatrix=[]
    transmatrixbbh=input("输入要同步的状态转移概率矩阵的版本号：")
    transmatrixwjlj="意识数据/状态转移概率矩阵/状态转移概率矩阵"+transmatrixbbh+".txt"
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

            公共状态.transmatrix.append(translist)

            hang=transmatrixfile.readline().strip()

    print("状态转移概率矩阵：",公共状态.transmatrix)

    #同步词典
    print("同步词典----------------")
    公共状态.dictionary=[]
    dictionarybbh=input("输入要同步的词典的版本号：")
    dictionarywjlj="意识数据/词典/词典"+dictionarybbh+".txt"#词典文件路径

    with open(dictionarywjlj,'r',encoding='utf-8') as dictionaryfile:
        hang=dictionaryfile.readline().strip()
        while hang:

            word_sen_weight=hang.split("；")#word、sen、weight之间用“；”连接
            word=word_sen_weight[0]
            sen=word_sen_weight[1]
            weight=float(word_sen_weight[2])
            公共状态.dictionary.append([word,sen,weight])
            hang=dictionaryfile.readline().strip()

    print("词典：",公共状态.dictionary)

    #同步词转移概率矩阵
    print("同步词转移概率矩阵----------------")
    公共状态.word_trans_matrix=[]
    word_trans_matrixbbh=input("输入要同步的词转移概率矩阵的版本号：")
    word_trans_matrixwjlj="意识数据/词转移概率矩阵/词转移概率矩阵"+word_trans_matrixbbh+".txt"#词转移概率矩阵文件路径
    with open(word_trans_matrixwjlj,'r',encoding='utf-8') as word_trans_matrixfile:
        hang=word_trans_matrixfile.readline().strip()
        while hang:
            word1_word2_weight12=hang.split("；")#word1、word2、weight12之间用“；”连接
            word1=word1_word2_weight12[0]
            word2=word1_word2_weight12[1]
            weight12=float(word1_word2_weight12[2])
            公共状态.word_trans_matrix.append([word1,word2,weight12])
            hang=word_trans_matrixfile.readline().strip()
    print("词转移概率矩阵：",公共状态.word_trans_matrix)



#保存记忆
def 保存记忆():
    if 公共状态.varcbbaocun1.get()==1 and 公共状态.varcbbaocun2.get()==1:
        #保存情绪习惯列表
        #保存喜习惯列表
        hapbbh=input("输入要保存的喜习惯列表的版本号：")
        hapwjlj="意识数据/情绪习惯列表/喜习惯列表/喜习惯列表"+hapbbh+".txt"#喜习惯列表文件路径
        content=''
        for senlist_hap in 公共状态.haphablist:
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
        sadwjlj="意识数据/情绪习惯列表/哀习惯列表/哀习惯列表"+sadbbh+".txt"#哀习惯列表文件路径
        content=''
        for senlist_sad in 公共状态.sadhablist:
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
        acthabwjlj="意识数据/行为习惯列表/行为习惯列表"+acthabbbh+".txt"
        content=''

        cont_ps=''
        cont_a=''

        for psav in 公共状态.acthablist:
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
        memorywjlj="意识数据/自传体记忆/自传体记忆"+memorybbh+".txt"
        content=''
        for senlist_actlist_vsum in 公共状态.memorylist:
            senlist=senlist_actlist_vsum[0]
            actlist=senlist_actlist_vsum[1]
            vsum=senlist_actlist_vsum[2]
            cont_senlist=''
            cont_actlist=''
            for i in senlist:
                cont_senlist+=str(i)+"。"
            for i in actlist:
                cont_actlist+=str(i)+"。"
            line=cont_senlist+"；"+cont_actlist+"；"+str(vsum)
            content+=str(line)+"\n"
        with open(memorywjlj,"w",encoding='utf-8') as memoryfile:
            memoryfile.write(content)

        #保存状态转移概率矩阵
        transbbh=input("输入要保存的状态转移概率矩阵的版本号：")
        transwjlj="意识数据/状态转移概率矩阵/状态转移概率矩阵"+transbbh+".txt"
        content=''
        for translist in 公共状态.transmatrix:
            cont_translist=''
            cont_translist+='。'.join(translist[0])
            for i in translist[1:]:
                cont_translist+='；'+'。'.join(i[0])+"、"+str(i[1])+"、"+str(i[2])

            line=cont_translist
            content+=str(line)+"\n"

        with open(transwjlj,"w",encoding='utf-8') as transfile:
            transfile.write(content)


        #保存词典
        dictionarybbh=input("输入要保存的词典的版本号：")
        dictionarywjlj="意识数据/词典/词典"+dictionarybbh+".txt"
        content=''
        for i in 公共状态.dictionary:
            line=i[0]+"；"+i[1]+"；"+str(i[2])
            content+=str(line)+"\n"
        with open(dictionarywjlj,"w",encoding='utf-8') as dictionaryfile:
            dictionaryfile.write(content)

        #保存词转移概率矩阵
        word_trans_matrixbbh=input("输入要保存的词转移概率矩阵的版本号：")
        word_trans_matrixwjlj="意识数据/词转移概率矩阵/词转移概率矩阵"+word_trans_matrixbbh+".txt"
        content=''
        for i in 公共状态.word_trans_matrix:
            line=i[0]+"；"+i[1]+"；"+str(i[2])
            content+=str(line)+"\n"
        with open(word_trans_matrixwjlj,"w",encoding='utf-8') as word_trans_matrixfile:
            word_trans_matrixfile.write(content)

        #保存ART
        artbbh=input("输入要保存的ART模型的版本号：")
        artwjlj="意识数据/ART/ART"+artbbh+".csv"
        df = pd.DataFrame(公共状态.art_model.prototypes)# 将prototypes转换为DataFrame
        # 保存为CSV文件，不包含标题行，每行之间没有空行
        df.to_csv(artwjlj, index=False, header=False)


        print("保存成功——————————————")
        公共状态.varcbbaocun1.set(0)
        公共状态.varcbbaocun2.set(0)
