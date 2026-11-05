#语言模块











#自然语言理解NLU




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


    return senset,wordbag



#更新词典
def update_dictionary(word, meaning,dictionary):#输入某个词和其含义，更新两者的映射关系

    #新含义逐渐覆盖旧含义

    for wsw in dictionary:
        if wsw[0]==word:
            wsw[2]*=0.9#旧含义对应的知觉概念的权重w=wx0.9+0x0.1=w+(0-w)x0.1（即学习率为0.1）

    for wsw in dictionary:        
        if wsw[0]==word and wsw[1]==meaning:#若已存在该映射关系
            wsw[2]=wsw[2]+1*0.1#新的含义对应的知觉概念的权重w=wx0.9+1x0.1=w+(1-w)x0.1
            break
    else:
        dictionary.append([word, meaning, 1])#将两者的映射关系添加到词典中，权重初始化为1


    return dictionary





#自然语言生成NLG



#生成句子
def generate_sentence(senset,dictionary,word_trans_matrix):

    #根据词典，将内部表征（概念集合）中的概念全部翻译成其对应的词，并添加入词集合中（{s1,s2,s3}->{word1,word2,word3}）
    wordset=[]
    for i in senset:
        #翻译时，找所有wsw中，sen符合且weight最大的那个wsw的word
        word=""
        weight=-1
        for wsw in dictionary:
            if wsw[1]==i and wsw[2]>weight:
                word=wsw[0]
                weight=wsw[2]
        #若不存在对应的词，则跳过这个概念
        if weight!=-1:
            wordset.append(word)

    #输出句列表初始化为仅一个句首符号：[“<sent_start>”]
    output_sentence_list=["<sent_start>"]

    #贪心转移
    #对词集合中所有的词，找出输出句列表末尾的词转移到其的概率最大的那个词（假设是word2），将其移入输入句末尾，输出句列表变成[“<sent_start>”，word2]
    #重复直至词集合为空
    while wordset!=[]:
        pre_word=output_sentence_list[-1]

        next_word=""
        weight=-1
        for www in word_trans_matrix:
            if www[0]==pre_word and www[1] in wordset and www[2]>weight:
                next_word=www[1]
                weight=www[2]
        if weight==-1:#若不存在对应的词，取词集合第一个词
            next_word=wordset[0]

        output_sentence_list.append(next_word)
        wordset.remove(next_word)

    #将输出句列表（假设是[“<sent_start>”,word2,word3,word1]）变为输出句“word2word3word1”
    output_sentence="".join(output_sentence_list[1:])

    return output_sentence




#更新词转移概率矩阵
def update_word_trans_matrix(sentence,word_trans_matrix,dictionary):
    #输入一句句子


    #对给定句子，统计句中每个词之间的转移概率，更新词转移概率矩阵word_trans_matrix

    #使用 函数：使用词典 进行分词，分出来的词放入词序列中
    senset,wordseq=use_dictionary(sentence,dictionary)
    #在词序列最前方放入句首符号“<sent_start>”
    wordseq.insert(0,"<sent_start>")
    #遍历词序列，更新相邻的词的转移概率
    for i in range(len(wordseq)-1):
        #pre_word：前一个词
        pre_word=wordseq[i]
        #next_word：后一个词
        next_word=wordseq[i+1]

        #对词转移概率矩阵的所有www
        for www in word_trans_matrix:
            #若www[0]==pre_word且www[1]!=next_word，则www[2]=www[2]x0.9+0x0.1=www[2]+(0-www[2])x0.1（即学习率为0.1）
            if www[0]==pre_word and www[1]!=next_word:
                    www[2]=www[2]*0.9+0*0.1
        for www in word_trans_matrix:
            #若www[0]==pre_word且www[1]==next_word，则www[2]=www[2]x0.9+1x0.1=www[2]+(1-www[2])x0.1
            if www[0]==pre_word and www[1]==next_word:
                www[2]=www[2]*0.9+1*0.1
                break
        else:#若词转移概率矩阵中没有这种www
            word_trans_matrix.append([pre_word,next_word,1])#将pre_word和next_word的转移关系添加到词转移概率矩阵中，权重初始化为1


    return word_trans_matrix

























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
    word_trans_matrix1=[]

    import random
    for i in range(1000):
        rand=random.randint(0, 4)
        if rand==0:
            word_trans_matrix1=update_word_trans_matrix("我今天真好",word_trans_matrix1,dictionary1)
        if rand==1:
            word_trans_matrix1=update_word_trans_matrix("你们真好",word_trans_matrix1,dictionary1)
        if rand==2:
            word_trans_matrix1=update_word_trans_matrix("我今天天气",word_trans_matrix1,dictionary1)
        if rand==3:
            word_trans_matrix1=update_word_trans_matrix("他真好",word_trans_matrix1,dictionary1)
        if rand==4:
            word_trans_matrix1=update_word_trans_matrix("天气他们你",word_trans_matrix1,dictionary1)

    senset=["1","6","8"]
    sent=generate_sentence(senset,dictionary1,word_trans_matrix1)
    print(sent)

    senset=["4","8"]
    sent=generate_sentence(senset,dictionary1,word_trans_matrix1)
    print(sent)

    senset=["1","6","7"]
    sent=generate_sentence(senset,dictionary1,word_trans_matrix1)
    print(sent)

    senset=["3","8"]
    sent=generate_sentence(senset,dictionary1,word_trans_matrix1)
    print(sent)

    senset=["7","5","2"]
    sent=generate_sentence(senset,dictionary1,word_trans_matrix1)
    print(sent)

    senset=["2","5","7"]
    sent=generate_sentence(senset,dictionary1,word_trans_matrix1)
    print(sent)

    senset=["7","2","5"]
    sent=generate_sentence(senset,dictionary1,word_trans_matrix1)
    print(sent)

    senset=["5","2","7"]
    sent=generate_sentence(senset,dictionary1,word_trans_matrix1)
    print(sent)