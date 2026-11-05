# -*- coding: utf-8 -*-n
"""
苍穹3号 · Flask后端服务（完整业务逻辑，支持版本切换）
"""

import copy
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import load_model
import PIL.Image
import numpy as np
import pandas as pd
import cv2
import time
import random
from scipy.spatial import distance
import operator
import pyautogui
import threading
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os

# ============================
# 1. 全局变量
# ============================
psenlist = ["初始值"]
pactlist = ["初始值"]
senlist = []
actlist = []
want_learn_list = []
hapsum = 0.0
sadsum = 0.0
vsum = 0.0
predict_state_chance = []
predict_max_state = ''
predict_max_chance = 0
act_detail_list = []
attentive_time_step_count = 5
psav_memory = []
psav_now = []
introcontent = []
inputsentence = ""
learn_new_word = False
generate_sent = False
nl_output_buffer = ""
mode = "2"
senlist_add_actlist = "0"
randforget = "0"
adjust_hapsadhablist = "1"
hapsum_mem_threshold = 2
sadsum_mem_threshold = 2
adjust_acthablist = "1"
v_acthab_threshold = 1
v_adjustact_threshold = -1
sleeptime = 1
imgsource = "1"

current_step = ""

# 数据容器
haphablist = []
sadhablist = []
allact = []
acthablist = []
memorylist = []
transmatrix = []
dictionary = []
word_trans_matrix = []
base_model = None
art_model = None

# 前端输入缓存
input_senlist_received = None
input_sentence_received = None
frontend_mode = "2"
current_version = "请在右侧加载个体数据"

# ============================
# 2. 语言模块函数
# ============================
def use_dictionary(inputsentence, dictionary):
    inputsentence_copy1 = inputsentence[:]
    inputsentence_copy2 = inputsentence[:]
    senset = []
    wordbag = []
    unclear_words = []
    unknown_words = []
    unknown_word = ""
    while len(inputsentence_copy1) > 0:
        word = ""
        wordlen = -1
        matchflag = False
        for wsw in dictionary:
            bxword = wsw[0]
            if len(bxword) > len(inputsentence_copy1):
                continue
            elif len(bxword) > wordlen and bxword == inputsentence_copy1[0:len(bxword)]:
                word = bxword
                wordlen = len(bxword)
                matchflag = True
        if matchflag:
            wordbag.append(word)
            inputsentence_copy1 = inputsentence_copy1[len(word):]
        else:
            inputsentence_copy1 = inputsentence_copy1[1:]
    for word in wordbag:
        unclear = True
        for wsw in dictionary:
            if wsw[0] == word:
                if wsw[2] > 0.5:
                    unclear = False
                    if wsw[1] != "":
                        senset.append(wsw[1])
        if unclear:
            unclear_words.append(word)
    if unclear_words:
        senset.append("不清楚含义的词：" + "。".join(unclear_words))
    for word in wordbag:
        while inputsentence_copy2[0:len(word)] != word:
            unknown_word += inputsentence_copy2[0]
            inputsentence_copy2 = inputsentence_copy2[1:]
        inputsentence_copy2 = inputsentence_copy2[len(word):]
        unknown_words.append(unknown_word)
        unknown_word = ""
    if len(inputsentence_copy2) > 0:
        unknown_words.append(inputsentence_copy2)
    unknown_words1 = []
    for i in unknown_words:
        if i != "":
            unknown_words1.append(i)
    unknown_words = unknown_words1
    new_words = unknown_words + unclear_words
    if new_words:
        senset.append("有生词")
        for i in new_words:
            senset.append(i + "@生词")
    return senset, wordbag

def update_dictionary(word, meaning, dictionary):
    for wsw in dictionary:
        if wsw[0] == word:
            wsw[2] *= 0.9
    for wsw in dictionary:
        if wsw[0] == word and wsw[1] == meaning:
            wsw[2] = wsw[2] + 1 * 0.1
            break
    else:
        dictionary.append([word, meaning, 1])
    return dictionary

def generate_sentence(senset, dictionary, word_trans_matrix):
    wordset = []
    for i in senset:
        word = ""
        weight = -1
        for wsw in dictionary:
            if wsw[1] == i and wsw[2] > weight:
                word = wsw[0]
                weight = wsw[2]
        if weight != -1:
            wordset.append(word)
    output_sentence_list = ["<sent_start>"]
    while wordset:
        pre_word = output_sentence_list[-1]
        next_word = ""
        weight = -1
        for www in word_trans_matrix:
            if www[0] == pre_word and www[1] in wordset and www[2] > weight:
                next_word = www[1]
                weight = www[2]
        if weight == -1:
            next_word = wordset[0]
        output_sentence_list.append(next_word)
        wordset.remove(next_word)
    output_sentence = "".join(output_sentence_list[1:])
    return output_sentence

def update_word_trans_matrix(sentence, word_trans_matrix, dictionary):
    senset, wordseq = use_dictionary(sentence, dictionary)
    wordseq.insert(0, "<sent_start>")
    for i in range(len(wordseq) - 1):
        pre_word = wordseq[i]
        next_word = wordseq[i+1]
        for www in word_trans_matrix:
            if www[0] == pre_word and www[1] != next_word:
                www[2] = www[2] * 0.9 + 0 * 0.1
        for www in word_trans_matrix:
            if www[0] == pre_word and www[1] == next_word:
                www[2] = www[2] * 0.9 + 1 * 0.1
                break
        else:
            word_trans_matrix.append([pre_word, next_word, 1])
    return word_trans_matrix

# ============================
# 3. ART 类
# ============================
class ART:
    def __init__(self, num_categories, vigilance, learning_rate, prototypes):
        self.num_categories = num_categories
        self.vigilance = vigilance
        self.learning_rate = learning_rate
        self.prototypes = prototypes
        self.cate_use_list = [0] * self.num_categories

    def calculate_similarity(self, input_pattern, prototype):
        return np.dot(input_pattern, prototype) / (np.linalg.norm(input_pattern) * np.linalg.norm(prototype) + 1e-8)

    def match(self, input_pattern):
        matched_category = None
        matched_similarity = 0
        for i in range(self.num_categories):
            similarity = self.calculate_similarity(input_pattern, self.prototypes[i])
            if similarity >= self.vigilance:
                if similarity > matched_similarity:
                    matched_category = i
                    matched_similarity = similarity
        return matched_category

    def update_prototype(self, input_pattern, category):
        self.prototypes[category] += self.learning_rate * (input_pattern - self.prototypes[category])

    def add_category(self, input_pattern):
        for i in range(self.num_categories):
            if np.all(self.prototypes[i] == 1) == True:
                self.prototypes[i] = input_pattern
                break
        else:
            print("ART 网络的所有类别已满，新类别将覆盖原有类别中最不活跃的那个类别")
            least_active_index = self.cate_use_list.index(min(self.cate_use_list))
            self.prototypes[least_active_index] = input_pattern

    def fit(self, data):
        for input_pattern in data:
            matched_category = self.match(input_pattern)
            if matched_category is not None:
                self.cate_use_list[matched_category] += 100
            for j in range(len(self.cate_use_list)):
                self.cate_use_list[j] = int(self.cate_use_list[j] * 0.9)
            if matched_category is None:
                self.add_category(input_pattern)
            else:
                self.update_prototype(input_pattern, matched_category)

# ============================
# 4. ACT 类
# ============================
class ACT:
    def __init__(self, senlist, hapsum, sadsum, vsum, actlist):
        self.senlist = senlist
        self.hapsum = hapsum
        self.sadsum = sadsum
        self.vsum = vsum
        self.actlist = actlist

    def report_qualia(self):
        print("意识体验内容：", self.senlist, self.hapsum, self.sadsum, self.vsum, self.actlist)

    def increase_art_vigilance(self):
        global art_model
        art_model.vigilance = 0.9

    def pressA(self):
        print("执行 pressA")
    def pressD(self):
        print("执行 pressD")
    def pressW(self):
        print("执行 pressW")
    def pressS(self):
        print("执行 pressS")
    def scrollup(self):
        print("执行 scrollup")
    def scrolldown(self):
        print("执行 scrolldown")

    def introspect(self):
        global introcontent
        introcontent = []
        for sen in self.senlist:
            introcontent.append(sen + "（p）")
        introcontent.append("喜：" + str(self.hapsum))
        introcontent.append("哀：" + str(self.sadsum))
        introcontent.append("总价值：" + str(self.vsum))

# ============================
# 5. 核心功能函数（视觉简化）
# ============================
def clear_senlist():
    global senlist
    senlist = []

def vision(senlist):
    return senlist

def input_senlist(senlist):
    global input_senlist_received
    if input_senlist_received is not None:
        senlist.extend(input_senlist_received)
        input_senlist_received = None
    return senlist

def emo(senlist):
    global hapsum, sadsum, vsum
    hapsum = 0
    sadsum = 0
    state_chance_heap = []
    acthablist_predict, actlist_predict, psav_now_predict = choose_act(acthablist, [], [])
    state_chance_heap.append([senlist + actlist_predict, 1])
    for j in range(attentive_time_step_count):
        for state_chance in state_chance_heap:
            for i in haphablist:
                if set(i[0]).issubset(set(state_chance[0])):
                    hapsum += int(i[1]) * state_chance[1]
            for i in sadhablist:
                if set(i[0]).issubset(set(state_chance[0])):
                    sadsum += int(i[1]) * state_chance[1]
        state_chance_heap1 = []
        for state_chance in state_chance_heap:
            for translist in transmatrix:
                if translist[0] == state_chance[0]:
                    for i in translist[1:]:
                        state_chance_heap1.append([i[0], i[1] * state_chance[1]])
        state_chance_heap = state_chance_heap1
    if hapsum > 5: hapsum = 5
    if sadsum > 5: sadsum = 5
    hapsum = round(hapsum, 1)
    sadsum = round(sadsum, 1)
    vsum = hapsum - sadsum
    return hapsum, sadsum, vsum

def update_v(acthablist):
    global psav_memory, vsum
    if len(psav_memory) == 0:
        TDerror = vsum
    else:
        TDerror = vsum - psav_memory[-1][0][2]
    lr = 0.3
    for i in range(len(psav_memory)):
        psavs = psav_memory[-i - 1]
        for j in psavs:
            for psav in acthablist:
                if sorted(j[0]) == sorted(psav[0]) and sorted(j[1]) == sorted(psav[1]):
                    psav[2] = round(psav[2] + lr * TDerror, 2)
    return acthablist

def change_acthablist(acthablist):
    global v_adjustact_threshold, attentive_time_step_count, memorylist, allact
    for psav in acthablist:
        if psav[2] <= v_adjustact_threshold:
            bxact = []
            Qpt = v_adjustact_threshold
            for translist in transmatrix:
                zuobudao = 0
                diffset = []
                for i in translist[0]:
                    if i not in psav[0]:
                        diffset.append(i)
                for i in diffset:
                    if i not in allact:
                        zuobudao = 1
                        break
                if zuobudao == 0:
                    for psen in psav[0]:
                        if psen not in translist[0]:
                            break
                    else:
                        allresult = []
                        result = sorted(translist[1:], key=operator.itemgetter(1), reverse=True)[0:3]
                        allresult.extend(result)
                        for i in range(attentive_time_step_count - 1):
                            for state_chance_times in result:
                                for translist2 in transmatrix:
                                    if translist2[0] == state_chance_times[0]:
                                        result = sorted(translist2[1:], key=operator.itemgetter(1), reverse=True)[0:3]
                                        allresult.extend(result)
                        vsum1 = 0
                        for state_chance_times in allresult:
                            hapsum2, sadsum2, vsum2 = emo(state_chance_times[0])
                            vsum1 += vsum2 * state_chance_times[1]
                        if vsum1 > Qpt:
                            Qpt = vsum1
                            bxact = diffset
            if Qpt > v_adjustact_threshold:
                newact = bxact
                newvalue = Qpt
                acthablist.append([psav[0], newact, round(newvalue, 2)])
            else:
                if random.random() < 0.5:
                    newact = copy.deepcopy(psav[1])
                    newact.append(random.choice(list(allact)))
                    newvalue = v_adjustact_threshold + 1
                    acthablist.append([psav[0], newact, newvalue])
                else:
                    if psav[1] != []:
                        removeact = psav[1][random.randint(0, len(psav[1]) - 1)]
                        newact = copy.deepcopy(psav[1])
                        newact.remove(removeact)
                        newvalue = v_adjustact_threshold + 1
                        acthablist.append([psav[0], newact, newvalue])
    if len(memorylist) >= attentive_time_step_count:
        senlist_actlist_vsum = memorylist[-attentive_time_step_count]
        for psav in copy.deepcopy(acthablist):
            if psav[0] == senlist_actlist_vsum[0] and psav[1] == senlist_actlist_vsum[1] and psav[2] <= v_adjustact_threshold:
                acthablist.remove(psav)
    acthablist1 = []
    for psav in acthablist:
        if psav[0] != []:
            acthablist1.append(psav)
    acthablist = acthablist1
    return acthablist

def choose_act(acthablist, actlist, psav_now):
    global senlist, v_adjustact_threshold, adjust_acthablist
    psav_now = []
    actlist = []
    find = False
    vmax = float("-inf")
    for psav in acthablist:
        if sorted(psav[0]) == sorted(senlist):
            if psav[2] > vmax:
                vmax = psav[2]
                actlist = psav[1]
                find = True
                psav_now.append(psav.copy())
    vmax = v_adjustact_threshold
    if find == False:
        for psav in acthablist:
            for i in psav[0]:
                if i not in senlist:
                    break
            else:
                if psav[2] > vmax:
                    vmax = psav[2]
                    actlist = psav[1]
                    find = True
                    psav_now.append(psav.copy())
                    psav_now.append([senlist, actlist, psav[2]])
                    if adjust_acthablist == "1":
                        acthablist.append([senlist, actlist, psav[2]])
    if find == False:
        if adjust_acthablist == "1":
            acthablist.append([senlist, actlist, 0])
        psav_now.append([senlist, actlist, 0])
    return acthablist, actlist, psav_now

def update_psav_memory(psav_now, psav_memory):
    if len(psav_memory) >= attentive_time_step_count:
        psav_memory.pop(0)
    psav_memory.append(psav_now)
    return psav_memory

def act_detail(want_learn_list):
    global actlist, act_detail_list
    counts = 0
    act_detail_list = copy.deepcopy(actlist)
    act_detail_list1 = []
    if counts >= 1:
        for i in range(counts):
            for act in act_detail_list:
                find = False
                for translist in transmatrix:
                    for state_chance_times in translist[1:]:
                        if act in state_chance_times[0] and state_chance_times[1] >= 0.5:
                            act_detail_list1.extend(translist[0])
                            find = True
                            print("要做", act, "先做", translist[0])
                if find == False:
                    print("未搜索到", act, "的前置状态")
                    want_learn_list.append(act)
            act_detail_list = copy.deepcopy(act_detail_list1)
            act_detail_list1 = []
    list1 = []
    for i in want_learn_list:
        if i not in list1:
            list1.append(i)
    want_learn_list = list1
    if want_learn_list != []:
        print("需要学习以下行为：", want_learn_list)
    return act_detail_list, want_learn_list

def output_act(actlist):
    global learn_new_word, generate_sent, nl_output_buffer
    if "报告意识体验" in actlist:
        ACT(senlist, hapsum, sadsum, vsum, actlist).report_qualia()
    if "pressA" in actlist:
        ACT(senlist, hapsum, sadsum, vsum, actlist).pressA()
    if "pressD" in actlist:
        ACT(senlist, hapsum, sadsum, vsum, actlist).pressD()
    if "pressW" in actlist:
        ACT(senlist, hapsum, sadsum, vsum, actlist).pressW()
    if "pressS" in actlist:
        ACT(senlist, hapsum, sadsum, vsum, actlist).pressS()
    if "scrollup" in actlist:
        ACT(senlist, hapsum, sadsum, vsum, actlist).scrollup()
    if "scrolldown" in actlist:
        ACT(senlist, hapsum, sadsum, vsum, actlist).scrolldown()
    if "内省" in actlist:
        ACT(senlist, hapsum, sadsum, vsum, actlist).introspect()
    if "在下一回合学习生词" in actlist:
        learn_new_word = True
    if "生成句子" in actlist:
        generate_sent = True

def add_memorylist(senlist, actlist, vsum, memorylist):
    memorylist.append([senlist, actlist, vsum])
    return memorylist

def update_transmatrix(transmatrix):
    global psenlist, pactlist, senlist, actlist
    for translist in transmatrix:
        if translist[0] == psenlist + pactlist:
            cunzai = False
            for i in translist[1:]:
                if i[0] == senlist + actlist:
                    i[2] += 1
                    i[1] = i[1] * 0.8 + 1 * 0.2
                    cunzai = True
                else:
                    i[1] = i[1] * 0.8 + 0 * 0.2
            if cunzai == False:
                translist.append([senlist + actlist, 1, 1])
            break
    else:
        transmatrix.append([psenlist + pactlist, [senlist + actlist, 1, 1]])
    return transmatrix

def predict_next_state_chance():
    global senlist, actlist, predict_state_chance, predict_max_state, predict_max_chance
    predict_state_chance = []
    predict_max_chance = -1
    predict_max_state = "未发现"
    for translist in transmatrix:
        if translist[0] == senlist + actlist:
            predict_state_chance = translist[1:]
            for i in translist[1:]:
                if i[1] > predict_max_chance:
                    predict_max_chance = i[1]
                    predict_max_state = i[0]
            break
    else:
        predict_state_chance = "未发现"
    return predict_state_chance, predict_max_state, predict_max_chance

def extend_senlist():
    global pactlist, senlist, introcontent
    qita = introcontent
    extended_senlist = pactlist + senlist + qita
    extended_senlist1 = copy.deepcopy(extended_senlist)
    for i in extended_senlist:
        if i[0] == "-":
            extended_senlist1.remove(i)
            if i[1:] in extended_senlist1:
                extended_senlist1.remove(i[1:])
    extended_senlist = extended_senlist1
    if extended_senlist == []:
        extended_senlist.append("空闲")
    return extended_senlist

# ============================
# 6. 数据加载
# ============================
def load_data(version="李旻恒"):
    global haphablist, sadhablist, allact, acthablist, memorylist, transmatrix, dictionary, word_trans_matrix, art_model, base_model, current_version

    haphablist.clear()
    sadhablist.clear()
    allact.clear()
    acthablist.clear()
    memorylist.clear()
    transmatrix.clear()
    dictionary.clear()
    word_trans_matrix.clear()

    try:
        base_model = load_model('知觉分类模块/CNN/vgg16_base_model.h5')
    except:
        print("CNN模型加载失败，请检查路径")
        base_model = None

    try:
        art_path = f'意识数据/ART/ART{version}.csv'
        prototypes_df = pd.read_csv(art_path, header=None)
        prototypes = prototypes_df.to_numpy()
        art_model = ART(num_categories=100, vigilance=0.5, learning_rate=0, prototypes=prototypes)
    except Exception as e:
        print(f"ART文件不存在或加载失败: {e}，使用默认空模型")
        prototypes = np.ones((100, 512))
        art_model = ART(num_categories=100, vigilance=0.5, learning_rate=0, prototypes=prototypes)

    try:
        with open(f'意识数据/情绪习惯列表/喜习惯列表/喜习惯列表{version}.txt', 'r', encoding='utf-8') as hapfile:
            hang = hapfile.readline().strip()
            while hang:
                senlisthap1 = hang.split("；")
                senlist = senlisthap1[0].split("。")
                hap = int(senlisthap1[1])
                while "" in senlist: senlist.remove("")
                haphablist.append([senlist, hap])
                hang = hapfile.readline().strip()
    except:
        print(f"喜习惯列表版本{version}不存在，使用空列表")

    try:
        with open(f'意识数据/情绪习惯列表/哀习惯列表/哀习惯列表{version}.txt', 'r', encoding='utf-8') as sadfile:
            hang = sadfile.readline().strip()
            while hang:
                senlistsad1 = hang.split("；")
                senlist = senlistsad1[0].split("。")
                sad = int(senlistsad1[1])
                while "" in senlist: senlist.remove("")
                sadhablist.append([senlist, sad])
                hang = sadfile.readline().strip()
    except:
        print(f"哀习惯列表版本{version}不存在，使用空列表")

    try:
        with open(f"意识数据/行为空间/行为空间{version}.txt", "r", encoding='utf-8') as allactfile:
            acts = allactfile.readline().strip()
            while acts:
                allact.append(acts)
                acts = allactfile.readline().strip()
    except:
        print(f"行为空间版本{version}不存在，使用空列表")

    try:
        with open(f"意识数据/行为习惯列表/行为习惯列表{version}.txt", "r", encoding='utf-8') as acthabfile:
            hang = acthabfile.readline().strip()
            while hang:
                psav1 = hang.split("；")
                psav_p = psav1[0].split("。")
                psav_a = psav1[1].split("。")
                v = int(psav1[2])
                while "" in psav_p: psav_p.remove("")
                while "" in psav_a: psav_a.remove("")
                acthablist.append([psav_p, psav_a, v])
                hang = acthabfile.readline().strip()
    except:
        print(f"行为习惯列表版本{version}不存在，使用空列表")

    try:
        with open(f"意识数据/自传体记忆/自传体记忆{version}.txt", 'r', encoding='utf-8') as memorylistfile:
            hang = memorylistfile.readline().strip()
            while hang:
                senlist_actlist_vsum = hang.split("；")
                senlist = senlist_actlist_vsum[0].split("。")
                actlist2 = senlist_actlist_vsum[1].split("。")
                vsum2 = int(senlist_actlist_vsum[2])
                while "" in senlist: senlist.remove("")
                while "" in actlist2: actlist2.remove("")
                memorylist.append([senlist, actlist2, vsum2])
                hang = memorylistfile.readline().strip()
    except:
        print(f"自传体记忆版本{version}不存在，使用空列表")

    try:
        with open(f"意识数据/状态转移概率矩阵/状态转移概率矩阵{version}.txt", 'r', encoding='utf-8') as transmatrixfile:
            hang = transmatrixfile.readline().strip()
            while hang:
                translist = []
                startstate = hang.split("；")[0].split("。")
                while "" in startstate: startstate.remove("")
                translist.append(startstate)
                for i in hang.split("；")[1:]:
                    endstateseq = i.split("、")
                    while "" in endstateseq: endstateseq.remove("")
                    endstate = endstateseq[0].split("。")
                    while "" in endstate: endstate.remove("")
                    chance = float(endstateseq[1])
                    times = int(endstateseq[2])
                    translist.append([endstate, chance, times])
                transmatrix.append(translist)
                hang = transmatrixfile.readline().strip()
    except:
        print(f"状态转移概率矩阵版本{version}不存在，使用空列表")

    try:
        with open(f"意识数据/词典/词典{version}.txt", 'r', encoding='utf-8') as dictionaryfile:
            hang = dictionaryfile.readline().strip()
            while hang:
                word_sen_weight = hang.split("；")
                word = word_sen_weight[0]
                sen = word_sen_weight[1]
                weight = float(word_sen_weight[2])
                dictionary.append([word, sen, weight])
                hang = dictionaryfile.readline().strip()
    except:
        print(f"词典版本{version}不存在，使用空列表")

    try:
        with open(f"意识数据/词转移概率矩阵/词转移概率矩阵{version}.txt", 'r', encoding='utf-8') as word_trans_matrixfile:
            hang = word_trans_matrixfile.readline().strip()
            while hang:
                word1_word2_weight12 = hang.split("；")
                word1 = word1_word2_weight12[0]
                word2 = word1_word2_weight12[1]
                weight12 = float(word1_word2_weight12[2])
                word_trans_matrix.append([word1, word2, weight12])
                hang = word_trans_matrixfile.readline().strip()
    except:
        print(f"词转移概率矩阵版本{version}不存在，使用空列表")

    current_version = version
    print(f"数据加载完成，版本号 {version}")

# ============================
# 7. 核心步进函数
# ============================
def run_one_step():
    global senlist, actlist, hapsum, sadsum, vsum, psenlist, pactlist
    global learn_new_word, generate_sent, nl_output_buffer, inputsentence
    global input_sentence_received, input_senlist_received
    global memorylist, transmatrix, acthablist, psav_memory, psav_now
    global introcontent, want_learn_list
    global dictionary, word_trans_matrix
    global current_step

    step_history = []

    print("=== run_one_step 被调用 ===")

    clear_senlist()
    current_step = "清空知觉列表"
    step_history.append(current_step)
    print("步骤:", current_step)

    if mode == "3":
        senlist = vision(senlist)
        current_step = "视觉感知"
        step_history.append(current_step)
        print("步骤:", current_step)

    if input_sentence_received is not None:
        inputsentence = input_sentence_received
        if learn_new_word == False:
            senset, wordbag = use_dictionary(inputsentence, dictionary)
            senlist.extend(senset)
            word_trans_matrix = update_word_trans_matrix(inputsentence, word_trans_matrix, dictionary)
            current_step = "语言理解"
            step_history.append(current_step)
            print("步骤:", current_step)
        input_sentence_received = None

    if input_senlist_received is not None:
        senlist.extend(input_senlist_received)
        input_senlist_received = None
        current_step = "接收知觉输入"
        step_history.append(current_step)
        print("步骤:", current_step)

    senlist = extend_senlist()
    current_step = "工作记忆扩展"
    step_history.append(current_step)
    print("步骤:", current_step)

    if learn_new_word == True:
        for sen in senlist:
            dictionary = update_dictionary(inputsentence, sen, dictionary)
        learn_new_word = False
        current_step = "学习生词"
        step_history.append(current_step)
        print("步骤:", current_step)

    hapsum, sadsum, vsum = emo(senlist)
    current_step = "情绪发放"
    step_history.append(current_step)
    print("步骤:", current_step)

    if adjust_acthablist == "1":
        acthablist = update_v(acthablist)
        current_step = "更新预期价值"
        step_history.append(current_step)
        print("步骤:", current_step)
        acthablist = change_acthablist(acthablist)
        current_step = "调整行为习惯"
        step_history.append(current_step)
        print("步骤:", current_step)

    acthablist, actlist, psav_now = choose_act(acthablist, actlist, psav_now)
    current_step = "行为选择"
    step_history.append(current_step)
    print("步骤:", current_step)
    psav_memory = update_psav_memory(psav_now, psav_memory)
    current_step = "更新行为记忆"
    step_history.append(current_step)
    print("步骤:", current_step)

    act_detail_list, want_learn_list = act_detail(want_learn_list)
    current_step = "行为分解"
    step_history.append(current_step)
    print("步骤:", current_step)

    output_act(actlist)
    current_step = "行为执行"
    step_history.append(current_step)
    print("步骤:", current_step)

    nl_output_buffer = ""
    if generate_sent == True:
        senset = copy.deepcopy(actlist)
        if "生成句子" in senset:
            senset.remove("生成句子")
        nl_output_buffer += generate_sentence(senset, dictionary, word_trans_matrix)
        generate_sent = False
        current_step = "语言生成"
        step_history.append(current_step)
        print("步骤:", current_step)

    memorylist = add_memorylist(senlist, actlist, vsum, memorylist)
    current_step = "记忆存储"
    step_history.append(current_step)
    print("步骤:", current_step)

    transmatrix = update_transmatrix(transmatrix)
    current_step = "更新世界模型"
    step_history.append(current_step)
    print("步骤:", current_step)

    predict_next_state_chance()
    current_step = "预测下一状态"
    step_history.append(current_step)
    print("步骤:", current_step)

    psenlist = copy.deepcopy(senlist)
    pactlist = copy.deepcopy(actlist)
    current_step = "回合结束"
    step_history.append(current_step)
    print("步骤:", current_step)

    return {
        'round': len(memorylist),
        'senlist': senlist,
        'actlist': actlist,
        'hapsum': hapsum,
        'sadsum': sadsum,
        'vsum': vsum,
        'memory': memorylist[-5:],
        'transmatrix': transmatrix,
        'nl_output': nl_output_buffer,
        'dictionary_count': len(dictionary),
        'step_history': step_history
    }

# ============================
# 8. Flask 应用
# ============================
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        'round': len(memorylist),
        'senlist': senlist,
        'actlist': actlist,
        'hapsum': hapsum,
        'sadsum': sadsum,
        'vsum': vsum,
        'memory': [{'senlist': m[0], 'actlist': m[1], 'vsum': m[2]} for m in memorylist[-5:]],
        'transmatrix': transmatrix,
        'nl_output': nl_output_buffer,
        'current_version': current_version,
        'dictionary_count': len(dictionary),
        'predict_next_state': predict_max_state,
        'predict_next_chance': predict_max_chance,
        'current_step': current_step
    })

@app.route('/api/step', methods=['POST'])
def do_step():
    try:
        status = run_one_step()
        return jsonify({
            'round': status['round'],
            'log': '步进完成',
            'step_history': status['step_history']
        })
    except Exception as e:
        print(f"step 异常: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/set_mode', methods=['POST'])
def set_mode():
    global mode
    data = request.get_json()
    mode = data.get('mode', '2')
    return jsonify({'mode': mode})

@app.route('/api/load_data', methods=['POST'])
def load_data_api():
    global current_version
    data = request.get_json()
    version = data.get('version', '李旻恒')
    try:
        load_data(version)
        return jsonify({'status': 'ok', 'version': version})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/input_senlist', methods=['POST'])
def api_input_senlist():
    global input_senlist_received
    data = request.get_json()
    senlist_in = data.get('senlist', [])
    input_senlist_received = senlist_in
    return jsonify({'status': 'ok'})

@app.route('/api/input_nl', methods=['POST'])
def api_input_nl():
    global input_sentence_received
    data = request.get_json()
    sentence = data.get('sentence', '')
    input_sentence_received = sentence
    return jsonify({'status': 'ok'})

# ============================
# 9. 启动
# ============================
if __name__ == '__main__':
    print("正在初始化苍穹3号系统...")
    load_data("李旻恒")
    print("启动Flask服务，访问 http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000)