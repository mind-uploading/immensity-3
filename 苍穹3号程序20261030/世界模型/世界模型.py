#世界模型
import 公共状态


#根据当前状态state更新状态转移概率矩阵
def update_transmatrix(transmatrix):

    #更新状态转移概率矩阵中的状态和次数
    for translist in transmatrix:
        if translist[0]==公共状态.psenlist+公共状态.pactlist:

            cunzai=False

            for i in translist[1:]:
                if i[0]==公共状态.senlist+公共状态.actlist:
                    i[2]+=1
                    i[1]=i[1]*0.8+1*0.2
                    cunzai=True
                else:
                    i[1]=i[1]*0.8+0*0.2

            if cunzai==False:
                translist.append([公共状态.senlist+公共状态.actlist,1,1])

            break
    else:
        transmatrix.append([公共状态.psenlist+公共状态.pactlist,[公共状态.senlist+公共状态.actlist,1,1]])


    #print("截至目前的状态转移概率矩阵为：",transmatrix)

    return transmatrix




#根据状态转移矩阵预测接下来各状态的发生概率，以及最可能发生的状态
def predict_next_state_chance():
    predict_state_chance=[]
    predict_max_chance=-1
    predict_max_state="未发现"

    for translist in 公共状态.transmatrix:
        if translist[0]==公共状态.senlist+公共状态.actlist:
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

    return predict_state_chance,predict_max_state,predict_max_chance
