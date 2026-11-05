#语言模块


#使用词典
def use_dictionary(inputsentence,dictionary):

    #输入句的拷贝
    inputsentence_copy1=inputsentence[:]#在扫描输入句根据词典匹配时使用
    inputsentence_copy2=inputsentence[:]#在记录并输出不认识的词时使用
    #知觉概念集合
    senset=[]
    #词袋
    wordbag=[]
    #不清楚含义的词
    unclear_words=[]
    #不认识的词
    unknown_words=[]
    unknown_word=""#用于暂存不认识的词的字符


    #从前往后扫描输入句，根据词典进行正向最大匹配
    while len(inputsentence_copy1)>0:

        #遍历词典中所有的词，按词的长度降序匹配
        word=""
        wordlen=-1
        matchflag=False
        for wsw in dictionary:
            bxword=wsw[0]#备选的词
            if len(bxword)>len(inputsentence_copy1): 
                continue
            elif len(bxword)>wordlen and bxword==inputsentence_copy1[0:len(bxword)]:
                word=bxword
                wordlen=len(bxword)
                matchflag=True
        #一旦匹配到
        if matchflag==True:
            #将其加入词袋中并从输入句中删除
            wordbag.append(word)
            inputsentence_copy1=inputsentence_copy1[len(word):]
        #若词典中没有词能匹配上，删除句首的字重新尝试匹配
        else:
            inputsentence_copy1=inputsentence_copy1[1:]


    #对词袋中的每个词
    for word in wordbag:
        #输出其对应的各个知觉概念（仅输出权重大于0.5的）
        #记录不清楚含义的词（所有对应的权重都小于等于0.5的词）
        unclear=True
        for wsw in dictionary:
            if wsw[0]==word:
                if wsw[2]>0.5:
                    unclear=False
                    if(wsw[1]!=""):
                        senset.append(wsw[1])
        if unclear==True:
            unclear_words.append(word)
    if unclear_words!=[]: 
        senset.append("不清楚含义的词："+"。".join(unclear_words))


    #记录不认识的词（不能根据词典匹配的字符串）

    for word in wordbag:
        while inputsentence_copy2[0:len(word)]!=word:
            unknown_word+=inputsentence_copy2[0]
            inputsentence_copy2=inputsentence_copy2[1:]
        inputsentence_copy2=inputsentence_copy2[len(word):]
        unknown_words.append(unknown_word)
        unknown_word=""
    if len(inputsentence_copy2)>0: 
        unknown_words.append(inputsentence_copy2)#不能匹配的剩余字符串
    #删除unknown_words中的空字符串
    unknown_words1=[]
    for i in unknown_words:
        if i!="":
            unknown_words1.append(i)
    unknown_words=unknown_words1


    #将不清楚含义或不认识的词作为生词输出，以激活后续学习生词的行为
    new_words=unknown_words+unclear_words
    if new_words!=[]: 
        #把生词加入senset中
        #输出生词标记
        senset.append("有生词")
        for i in new_words:
            senset.append(i+"@生词")#每个生词后标记


    return senset



#更新词典
def update_dictionary(word, meaning,dictionary):#输入某个词和其含义，更新两者的映射关系

    ##新含义逐渐覆盖旧含义

    for wsw in dictionary:
        if wsw[0]==word:
            wsw[2]*=0.9#旧含义对应的知觉概念的权重x0.9

    for wsw in dictionary:        
        if wsw[0]==word and wsw[1]==meaning:#若已存在该映射关系
            wsw[2]+=1#新的含义对应的知觉概念的权重+1
            break
    else:
        dictionary.append([word, meaning, 1])#将两者的映射关系添加到词典中，权重初始化为1


    return dictionary





if __name__=="__main__":
    dictionary1=[
        ["我", "1", 1],
        ["你", "2", 1],
        ["他", "3", 1],
        ["你们", "4", 1],
        ["他们", "5", 1],
        ["今天","6",0.6],
        ["天气","7",1],
        ["真好","8",0.4]

    ]
    print(use_dictionary("今天天气真好",dictionary1))
