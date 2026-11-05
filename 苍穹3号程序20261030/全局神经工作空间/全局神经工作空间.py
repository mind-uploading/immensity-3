#全局神经工作空间GW
import copy
from tkinter import *

import 公共状态


#可视化界面初始化
def 初始化界面():
    root=Tk()
    root.title("苍穹3号")
    root.geometry('1000x800')


    lbGW=Label(root,text="全局神经工作空间GW")
    lbGW.grid(row=0,column=1)



    lbsenpart=Label(root,text="知觉分类模块")
    lbsenpart.grid(row=1,column=0)

    lbinputsentence=Label(root,text="输入句（一句自然语言（由句号分隔的））")
    lbinputsentence.grid(row=2,column=0)
    entinputsentence=Entry(root,width=40)
    entinputsentence.grid(row=3,column=0)

    varcbinputsentence1=IntVar()
    varcbinputsentence2=IntVar()
    cbinputsentence1=Checkbutton(root,text="输入句准备完毕",variable=varcbinputsentence1,onvalue=1,offvalue=0)
    cbinputsentence1.grid(row=4,column=0)
    cbinputsentence2=Checkbutton(root,text="提交输入句",variable=varcbinputsentence2,onvalue=1,offvalue=0)
    cbinputsentence2.grid(row=5,column=0)

    lbinputsen=Label(root,text="输入当前知觉概念列表,各知觉概念之间用空格隔开。（若输入：想+某行为，系统将会输出该行为）")
    lbinputsen.grid(row=6,column=0)
    entinputsen=Entry(root,width=40)
    entinputsen.grid(row=7,column=0)

    varcbinputsen1=IntVar()
    varcbinputsen2=IntVar()
    cbinputsen1=Checkbutton(root,text="知觉概念列表准备完毕",variable=varcbinputsen1,onvalue=1,offvalue=0)
    cbinputsen1.grid(row=8,column=0)
    cbinputsen2=Checkbutton(root,text="提交知觉概念列表",variable=varcbinputsen2,onvalue=1,offvalue=0)
    cbinputsen2.grid(row=9,column=0)

    lbsenlist=Label(root,text="知觉概念列表：扩展前（当前从环境中获得的知觉内容）")
    lbsenlist.grid(row=10,column=0)
    txsenlist=Text(root,width=40,height=5)
    txsenlist.grid(row=11,column=0)

    lbextended_senlist=Label(root,text="知觉概念列表：扩展后（既是注意力选择后的结果，也模拟工作记忆的内容）")
    lbextended_senlist.grid(row=12,column=0)
    txextended_senlist=Text(root,width=40,height=5)
    txextended_senlist.grid(row=13,column=0)


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
    txactlist=Text(root,width=40,height=5)
    txactlist.grid(row=5,column=3)
    lbcounts=Label(root,text="行为的分解次数：（输入一个>=0的整数）")
    lbcounts.grid(row=6,column=3)
    entcounts=Entry(root,width=10)
    entcounts.grid(row=7,column=3)
    varcbcounts1=IntVar()
    varcbcounts2=IntVar()
    cbcounts1=Checkbutton(root,text="行为分解次数输入完毕",variable=varcbcounts1,onvalue=1,offvalue=0)
    cbcounts1.grid(row=8,column=3)
    cbcounts2=Checkbutton(root,text="提交行为分解次数",variable=varcbcounts2,onvalue=1,offvalue=0)
    cbcounts2.grid(row=9,column=3)
    lbact_detail_list=Label(root,text="行为细化后：")
    lbact_detail_list.grid(row=10,column=3)
    txact_detail_list=Text(root,width=40,height=5)
    txact_detail_list.grid(row=11,column=3)
    lbnloutput=Label(root,text="自然语言输出：")
    lbnloutput.grid(row=12,column=3)
    txnloutput=Text(root,width=40,height=3)
    txnloutput.grid(row=13,column=3)

    varcbbaocun1=IntVar()
    varcbbaocun2=IntVar()
    cbbaocun1=Checkbutton(root,text="保存当前记忆",variable=varcbbaocun1,onvalue=1,offvalue=0)
    cbbaocun1.grid(row=12,column=1)
    cbbaocun2=Checkbutton(root,text="确认保存当前记忆",variable=varcbbaocun2,onvalue=1,offvalue=0)
    cbbaocun2.grid(row=13,column=1)


    #将控制流中需要访问的控件存入公共状态
    公共状态.root=root
    公共状态.entinputsentence=entinputsentence
    公共状态.varcbinputsentence1=varcbinputsentence1
    公共状态.varcbinputsentence2=varcbinputsentence2
    公共状态.entinputsen=entinputsen
    公共状态.varcbinputsen1=varcbinputsen1
    公共状态.varcbinputsen2=varcbinputsen2
    公共状态.txsenlist=txsenlist
    公共状态.txextended_senlist=txextended_senlist
    公共状态.txmemorylist=txmemorylist
    公共状态.lbhapsum=lbhapsum
    公共状态.lbsadsum=lbsadsum
    公共状态.lbvsum=lbvsum
    公共状态.txhaphablist=txhaphablist
    公共状态.txsadhablist=txsadhablist
    公共状态.txtransmatrix=txtransmatrix
    公共状态.txpredict_state_chance=txpredict_state_chance
    公共状态.lbpredict_max_state=lbpredict_max_state
    公共状态.lbpredict_max_chance=lbpredict_max_chance
    公共状态.txacthablist=txacthablist
    公共状态.txactlist=txactlist
    公共状态.entcounts=entcounts
    公共状态.varcbcounts1=varcbcounts1
    公共状态.varcbcounts2=varcbcounts2
    公共状态.txact_detail_list=txact_detail_list
    公共状态.txnloutput=txnloutput
    公共状态.varcbbaocun1=varcbbaocun1
    公共状态.varcbbaocun2=varcbbaocun2



#扩展知觉概念列表senlist
def extend_senlist():

    #1、extended_senlist=pactlist（上一回合的行为概念列表）+senlist（本回合知觉概念列表）+其他
    #其他包含内省出来的内容
    qita=公共状态.introcontent
    extended_senlist=公共状态.pactlist+公共状态.senlist+qita
    #2、增强或抑制知觉概念
	#1）若pactlist中的行为概念就是知觉概念，表示对该知觉概念的增强
		#在1中已经添加入extended_senlist中了，不需要作额外处理
	#2）若pactlist中的行为概念是知觉概念前面加一个英文减号“-”，表示对该知觉概念的减弱
		#删除该行为概念，在extended_senlist中删除1次其对应的知觉概念
    extended_senlist1=copy.deepcopy(extended_senlist)
    for i in extended_senlist:
        if i[0]=="-":
            extended_senlist1.remove(i)
            if i[1:] in extended_senlist1:
                extended_senlist1.remove(i[1:])
    extended_senlist=extended_senlist1

    #3、若extended_senlist为空列表，往extended_senlist中添加“空闲”
    if extended_senlist==[]:
        extended_senlist.append("空闲")

    return extended_senlist
