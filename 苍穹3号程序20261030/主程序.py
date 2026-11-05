#苍穹3号主程序
import copy
import time

import 公共状态
from 知觉分类模块.知觉分类模块 import 加载知觉模型,初始化摄像头,clear_senlist,vision,input_senlist
from 价值分类记忆与价值系统.价值分类记忆与价值系统 import emo
from 行为与计划模块.行为与计划模块 import ACT,update_v,change_acthablist,choose_act,update_psav_memory,act_detail,output_act
from 记忆模块.记忆模块 import add_memorylist
from 世界模型.世界模型 import update_transmatrix,predict_next_state_chance
from 全局神经工作空间.全局神经工作空间 import 初始化界面,extend_senlist
from 记忆管理.记忆管理 import 同步记忆,保存记忆

#语言模块
from 语言模块.语言模块 import use_dictionary,update_dictionary,generate_sentence,update_word_trans_matrix
#use_dictionary(inputsentence,dictionary)
#update_dictionary(word, meaning,dictionary)#输入某个词和其含义，更新两者的映射关系
#generate_sentence(senset,dictionary,word_trans_matrix)
#update_word_trans_matrix(sentence,word_trans_matrix,dictionary)


#设置
print("请进行设置------------------")

#是否进入预设的模式
公共状态.mode=input("是否进入预设的模式？（不可变模式：1，默认模式：2，自主模式：3，否：0）")
if 公共状态.mode=="1":
    公共状态.senlist_add_actlist="0"
    公共状态.randforget="0"
    公共状态.adjust_hapsadhablist="0"
    公共状态.adjust_acthablist="0"
    公共状态.v_adjustact_threshold=-1
elif 公共状态.mode=="2":
    公共状态.senlist_add_actlist="0"
    公共状态.randforget="0"
    公共状态.adjust_hapsadhablist="1"
    公共状态.hapsum_mem_threshold=2
    公共状态.sadsum_mem_threshold=2
    公共状态.adjust_acthablist="1"
    公共状态.v_acthab_threshold=1
    公共状态.v_adjustact_threshold=-1
elif 公共状态.mode=="3":
    公共状态.senlist_add_actlist="0"
    公共状态.randforget="0"
    公共状态.adjust_hapsadhablist="1"
    公共状态.hapsum_mem_threshold=2
    公共状态.sadsum_mem_threshold=2
    公共状态.adjust_acthablist="1"
    公共状态.v_acthab_threshold=1
    公共状态.v_adjustact_threshold=-1
    公共状态.sleeptime=int(input("请输入两个回合之间的睡眠时间（单位：秒）："))
    公共状态.imgsource=input("请输入图像来源（摄像头：1，截屏（左半边屏幕）：2）：")
else:
    #1、将上一回合输出的行为概念加入下一回合的知觉概念列表中
    公共状态.senlist_add_actlist=input("是否要将上一回合输出的行为概念加入下一回合的知觉概念列表中？（是：1，否：0）")

    #2、随机遗忘机制
    公共状态.randforget=input("是否要激活随机遗忘机制？（是：1，否：0）")

    #3、调整情绪习惯列表
    公共状态.adjust_hapsadhablist=input("是否允许调整情绪习惯列表？（是：1，否：0）：")
    if 公共状态.adjust_hapsadhablist=="1":
        #设定价值分类记忆激活阈值
        #（一个新概念引发的情绪发放如果超过阈值则该概念被纳入价值分类记忆）
        print("接下来你将输入价值分类记忆激活阈值（范围0-5，通常为2）\n一个新概念引发的情绪发放如果超过阈值则该概念被纳入价值分类记忆")
        公共状态.hapsum_mem_threshold=int(input("喜的价值分类记忆激活阈值："))

        公共状态.sadsum_mem_threshold=int(input("哀的价值分类记忆激活阈值："))


    #4、调整行为习惯列表
    公共状态.adjust_acthablist=input("是否允许调整行为习惯列表？（是：1，否：0）：")
    if 公共状态.adjust_acthablist=="1":
        #行为固定化阈值v_acthab_threshold
        #若vsum>=行为固定化阈值v_acthab_threshold，将当前行为模式固定化（存入acthablist中）
        print("接下来你将输入行为固定化阈值v_acthab_threshold（范围0-5，通常为1）\n若总价值vsum>=行为固定化阈值v_acthab_threshold，将当前行为模式固定化")
        公共状态.v_acthab_threshold=int(input("行为固定化阈值v_acthab_threshold："))

        #行为调整激活阈值v_adjustact_threshold
        #若总价值vsum<=行为调整激活阈值v_adjustact_threshold，在当前行为模式基础上进行优化
        print("接下来你将输入行为调整激活阈值v_adjustact_threshold（范围0-5，通常为2）\n若总价值vsum<=行为调整激活阈值v_adjustact_threshold，在当前行为模式基础上进行优化")
        公共状态.v_adjustact_threshold=int(input("行为调整激活阈值v_adjustact_threshold："))

print("设置完成------------------")

#同步
print("请进行同步--------------")

#同步心智内容（情绪习惯列表/行为空间/行为习惯列表/自传体记忆/状态转移概率矩阵/词典/词转移概率矩阵）
同步记忆()

#加载CNN和ART
加载知觉模型()

#初始化
#（psenlist/pactlist/senlist/actlist/want_learn_list/hapsum/sadsum/vsum/predict_state_chance/predict_max_state/predict_max_chance/act_detail_list/updatesom/attentive_time_step_count/psav_memory/psav_now/introcontent/inputsentence/learn_new_word/generate_sent/nl_output_buffer的初始值见 公共状态.py）

#摄像头
初始化摄像头()

#可视化界面初始化
初始化界面()


#控制流
while True:

    #更新可视化界面
    公共状态.root.update()

    #清空senlist
    clear_senlist()

    #若进入自主模式，启用视觉
    if 公共状态.mode=='3':
        公共状态.senlist=vision(公共状态.senlist)

    #接收输入句（一句自然语言（由句号分隔的））
    #若进入自主模式，等待用户输入5秒
    if 公共状态.mode=="3":
        for i in range(50):
            公共状态.root.update()
            time.sleep(0.1)
        公共状态.inputsentence=公共状态.entinputsentence.get()
    #若没进入自主模式，等待用户输入直到用户确认输入完毕
    else:
        while True:
            公共状态.root.update()
            if 公共状态.varcbinputsentence1.get()==1 and 公共状态.varcbinputsentence2.get()==1:
                公共状态.inputsentence=公共状态.entinputsentence.get()
                break

            time.sleep(0.1)

    if 公共状态.learn_new_word==False:#本回合不学习生词
        senset,wordbag=use_dictionary(公共状态.inputsentence,公共状态.dictionary)
        公共状态.senlist.extend(senset)#使用词典获取输入句对应的知觉概念列表
        公共状态.word_trans_matrix=update_word_trans_matrix(公共状态.inputsentence,公共状态.word_trans_matrix,公共状态.dictionary)#用输入句更新词转移概率矩阵

    #更新可视化界面
    公共状态.varcbinputsentence1.set(0)
    公共状态.varcbinputsentence2.set(0)

    #接收输入的知觉概念列表
    公共状态.senlist=input_senlist(公共状态.senlist)

    #更新可视化界面
    公共状态.varcbinputsen1.set(0)
    公共状态.varcbinputsen2.set(0)
    senliststr=','.join(公共状态.senlist)
    公共状态.txsenlist.configure(state='normal')
    公共状态.txsenlist.delete(0.0,'end')
    公共状态.txsenlist.insert(0.0,senliststr)
    公共状态.txsenlist.configure(state='disabled')

    #扩展知觉概念列表senlist
    公共状态.senlist=extend_senlist()

    if 公共状态.learn_new_word==True:#本回合学习生词
        for sen in 公共状态.senlist:
            公共状态.dictionary=update_dictionary(公共状态.inputsentence,sen,公共状态.dictionary)#更新词典（用当前输入句作为生词，当前扩展后的知觉概念列表作为其含义）
            print(公共状态.dictionary)
        公共状态.learn_new_word=False#将生词学习标志改为False


    #更新可视化界面

    extended_senliststr=','.join(公共状态.senlist)
    公共状态.txextended_senlist.configure(state='normal')
    公共状态.txextended_senlist.delete(0.0,'end')
    公共状态.txextended_senlist.insert(0.0,extended_senliststr)
    公共状态.txextended_senlist.configure(state='disabled')

    #发放情绪
    公共状态.hapsum,公共状态.sadsum,公共状态.vsum=emo(公共状态.senlist)

    #更新可视化界面
    公共状态.lbhapsum.configure(text="喜的值:"+str(公共状态.hapsum))
    公共状态.lbsadsum.configure(text="哀的值:"+str(公共状态.sadsum))
    公共状态.lbvsum.configure(text="总价值:"+str(公共状态.vsum))

    content=''
    for senlist_hap in 公共状态.haphablist:
        cont_senlist=''
        for i in senlist_hap[0]:
            cont_senlist+=str(i)+"。"

        hap=senlist_hap[1]

        line=cont_senlist+"；"+str(hap)
        content+=str(line)+"\n"*2
    公共状态.txhaphablist.configure(state='normal')
    公共状态.txhaphablist.delete(0.0,'end')
    公共状态.txhaphablist.insert(0.0,content)
    公共状态.txhaphablist.configure(state='disabled')

    content=''
    for senlist_sad in 公共状态.sadhablist:
        cont_senlist=''
        for i in senlist_sad[0]:
            cont_senlist+=str(i)+"。"

        sad=senlist_sad[1]

        line=cont_senlist+"；"+str(sad)
        content+=str(line)+"\n"*2
    公共状态.txsadhablist.configure(state='normal')
    公共状态.txsadhablist.delete(0.0,'end')
    公共状态.txsadhablist.insert(0.0,content)
    公共状态.txsadhablist.configure(state='disabled')

    if 公共状态.adjust_acthablist=="1":#若允许调整行为习惯列表
        #根据实践结果更新psav组的v值
        公共状态.acthablist=update_v(公共状态.acthablist)

        #根据行为的价值（借助情绪习惯列表和状态转移概率矩阵求得）调整行为习惯
        公共状态.acthablist=change_acthablist(公共状态.acthablist)

    #根据知觉概念列表和行为习惯选择将执行的行为概念
    公共状态.acthablist,公共状态.actlist,公共状态.psav_now=choose_act(公共状态.acthablist,公共状态.actlist,公共状态.psav_now)


    #更新psav_memory
    公共状态.psav_memory=update_psav_memory(公共状态.psav_now,公共状态.psav_memory)

    #更新可视化界面
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
        content+=str(line)+"\n"*2

    公共状态.txacthablist.configure(state='normal')
    公共状态.txacthablist.delete(0.0,'end')
    公共状态.txacthablist.insert(0.0,content)
    公共状态.txacthablist.configure(state='disabled')

    公共状态.txactlist.configure(state='normal')
    公共状态.txactlist.delete(0.0,'end')
    公共状态.txactlist.insert(0.0,','.join(公共状态.actlist))
    公共状态.txactlist.configure(state='disabled')

    #对行为进行分解细化
    公共状态.act_detail_list,公共状态.want_learn_list=act_detail(公共状态.want_learn_list)

    #更新可视化界面
    公共状态.txact_detail_list.configure(state='normal')
    公共状态.txact_detail_list.delete(0.0,'end')
    公共状态.txact_detail_list.insert(0.0,','.join(公共状态.act_detail_list))
    公共状态.txact_detail_list.configure(state='disabled')

    #输出行为概念并执行
    output_act(公共状态.actlist)

    公共状态.nl_output_buffer=""#清空自然语言输出缓冲区
    if 公共状态.generate_sent==True:#若本回合生成句子
        #将actlist中除了“生成句子”之外的概念作为senset传给 函数：生成句子 ，生成一句句子并输出到自然语言输出缓冲区nl_output_buffer
        senset=copy.deepcopy(公共状态.actlist)
        if "生成句子" in senset:
            senset.remove("生成句子")
        公共状态.nl_output_buffer+=generate_sentence(senset,公共状态.dictionary,公共状态.word_trans_matrix)
        公共状态.generate_sent=False#将句子生成标志改为False
    #更新可视化界面
    公共状态.txnloutput.configure(state='normal')
    公共状态.txnloutput.delete(0.0,'end')
    公共状态.txnloutput.insert(0.0,''.join(公共状态.nl_output_buffer))
    公共状态.txnloutput.configure(state='disabled')


    #将当前的[senlist,actlist,vsum]加入自传体记忆memorylist中
    公共状态.memorylist=add_memorylist(公共状态.senlist,公共状态.actlist,公共状态.vsum,公共状态.memorylist)

    #更新可视化界面
    memoryliststr=""
    for i in 公共状态.memorylist:
        memoryliststr+=','.join(i[0])+"；"+','.join(i[1])+"；"+str(i[2])+"\n"*2
    公共状态.txmemorylist.configure(state='normal')
    公共状态.txmemorylist.delete(0.0,'end')
    公共状态.txmemorylist.insert(0.0,memoryliststr)
    公共状态.txmemorylist.configure(state='disabled')

    #根据当前状态state更新状态转移概率矩阵
    公共状态.transmatrix=update_transmatrix(公共状态.transmatrix)

    #根据状态转移矩阵预测接下来各状态的发生概率，以及最可能发生的状态
    公共状态.predict_state_chance,公共状态.predict_max_state,公共状态.predict_max_chance=predict_next_state_chance()

    #更新可视化界面
    content=''
    for translist in 公共状态.transmatrix:
        cont_translist=''
        cont_translist+='。'.join(translist[0])
        for i in translist[1:]:
            cont_translist+='；'+'。'.join(i[0])+"、"+str(i[1])+"、"+str(i[2])

        line=cont_translist
        content+=str(line)+"\n"*2
    公共状态.txtransmatrix.configure(state='normal')
    公共状态.txtransmatrix.delete(0.0,'end')
    公共状态.txtransmatrix.insert(0.0,content)
    公共状态.txtransmatrix.configure(state='disabled')

    公共状态.txpredict_state_chance.configure(state='normal')
    公共状态.txpredict_state_chance.delete(0.0,'end')
    if 公共状态.predict_state_chance=="未发现":
        公共状态.txpredict_state_chance.insert(0.0,"未发现")
    else:
        content=''
        for i in 公共状态.predict_state_chance:
            content+='。'.join(i[0])+"、"+str(i[1])+"、"+str(i[2])+"\n"*2
        公共状态.txpredict_state_chance.insert(0.0,content)
    公共状态.txpredict_state_chance.configure(state='disabled')

    if 公共状态.predict_state_chance=="未发现":
        公共状态.lbpredict_max_state.configure(text="接下来最可能发生的状态为:未发现")
    else:
        公共状态.lbpredict_max_state.configure(text="接下来最可能发生的状态为:"+",".join(公共状态.predict_max_state))
    公共状态.lbpredict_max_chance.configure(text="发生概率为:"+str(公共状态.predict_max_chance))


    #将psenlist更新为senlist，pactlist更新为actlist
    公共状态.psenlist=copy.deepcopy(公共状态.senlist)
    公共状态.pactlist=copy.deepcopy(公共状态.actlist)

    #若未进入不可变模式，询问是否保存当前心智内容
    if 公共状态.mode!="0":
        保存记忆()

    #若进入自主模式，睡眠一段时间
    if 公共状态.mode=="3":
        time.sleep(公共状态.sleeptime)
