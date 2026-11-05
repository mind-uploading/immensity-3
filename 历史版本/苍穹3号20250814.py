#引入第三方库
import copy
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import load_model
import PIL.Image
import io
import numpy as np
import pandas as pd
from minisom import *
import matplotlib.pyplot as plt
import os
import cv2
import time
import random
from scipy.spatial import distance
import operator
import pyautogui
#初始化
#上一回合知觉概念列表
psenlist=["初始值"]
#上一回合行为概念列表
pactlist=["初始值"]
#知觉概念列表
senlist=[]
#行为概念列表
actlist=[]
#学习需求列表
want_learn_list=[]
#其他变量
hapsum=0
sadsum=0
vsum=0
predict_state_chance=[]
predict_max_state=''
predict_max_chance=0
act_detail_list=[]
updatesom=False
attentive_time_step_count=1
psav_memory=[]
psav_now=[]
introcontent=[]
#摄像头
# 如果是调用笔记本自带的摄像头，参数就为0；如果是外置USB摄像头，参数就为1。
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
# 设置一下摄像头窗口的宽高，参数3代表宽度
cap.set(3, 1280)
# 参数4代表的高度
cap.set(4, 1280)
# 参数10代表亮度
cap.set(10, 100)

# 引入行为类
class ACT:
    def __init__(self,senlist,hapsum,sadsum,vsum,actlist):
        self.senlist=senlist
        self.hapsum=hapsum
        self.sadsum=sadsum
        self.vsum=vsum
        self.actlist=actlist
 

    def report_qualia(self):#报告意识体验
        print("意识体验内容：")
        print("当前知觉概念：",self.senlist)
        print("当前喜：",self.hapsum)
        print("当前哀：",self.sadsum)
        print("当前总价值：",self.vsum)
        print("当前行为概念：",self.actlist)
    def increase_art_vigilance(self):#提高ART的警戒值
        art_model.vigilance=0.9
    def pressA(self):#按键盘中的A键
        pyautogui.press('a')
    def pressD(self):#按键盘中的D键
        pyautogui.press('d')
    def pressW(self):#按键盘中的W键
        pyautogui.press('w')
    def pressS(self):#按键盘中的S键
        pyautogui.press('s')

    def scrollup(self):#鼠标滚轮向上滚动
        pyautogui.scroll(100)
    def scrolldown(self):#鼠标滚轮向下滚动
        pyautogui.scroll(-100)

    def introspect(self):#内省
        #内省内容包括senlist、hapsum、sadsum和vsum（不包括actlist，因为 函数：扩展知觉概念列表senlist 会将其加入下一回合的知觉概念列表） 
        global introcontent
        introcontent=[]
        for sen in self.senlist:
            introcontent.append(sen+"（p）")#知觉概念末尾添加“（p）”，表示对于下一回合的senlist来说，这个知觉概念是上一回合发生的
        introcontent.append("喜："+str(self.hapsum))
        introcontent.append("哀："+str(self.sadsum))
        introcontent.append("总价值："+str(self.vsum))




#设置
print("请进行设置------------------")

#是否进入预设的模式
mode=input("是否进入预设的模式？（不可变模式：1，默认模式：2，自主模式：3，否：0）")
if mode=="1":
    senlist_add_actlist="0"
    randforget="0"
    adjust_hapsadhablist="0"
    adjust_acthablist="0"
elif mode=="2":
    senlist_add_actlist="0"
    randforget="0"
    adjust_hapsadhablist="1"
    hapsum_mem_threshold=2
    sadsum_mem_threshold=2
    adjust_acthablist="1"
    v_acthab_threshold=1
    v_adjustact_threshold=-1
elif mode=="3":
    senlist_add_actlist="0"
    randforget="0"
    adjust_hapsadhablist="1"
    hapsum_mem_threshold=2
    sadsum_mem_threshold=2
    adjust_acthablist="1"
    v_acthab_threshold=1
    v_adjustact_threshold=-1
    sleeptime=int(input("请输入两个回合之间的睡眠时间（单位：秒）："))
    imgsource=input("请输入图像来源（摄像头：1，截屏（左半边屏幕）：2）：")
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

        senlisthap1=hang.split("；")#引发喜的知觉概念列表（senlist）和该列表引发的喜的水平（hap）之间用“；”连接
        senlist=senlisthap1[0].split("。")#引发喜的知觉概念列表内部的概念用“。”连接
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

        senlistsad1=hang.split("；")#引发哀的知觉概念列表（senlist）和该列表引发的哀的水平（sad）之间用“；”连接
        senlist=senlistsad1[0].split("。")#引发哀的知觉概念列表内部的概念用“。”连接
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

#同步自传体记忆
print("同步自传体记忆----------------")
memorylist=[]
memorylistbbh=input("输入要同步的自传体记忆的版本号：")
memorylistwjlj="自传体记忆/自传体记忆"+memorylistbbh+".txt"#自传体记忆文件路径

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
     
        memorylist.append([senlist,actlist,vsum])
        hang=memorylistfile.readline().strip()

print("自传体记忆：",memorylist)

#同步状态转移概率矩阵
print("同步状态转移概率矩阵----------------")
transmatrix=[]
transmatrixbbh=input("输入要同步的状态转移概率矩阵的版本号：")
transmatrixwjlj="状态转移概率矩阵/状态转移概率矩阵"+transmatrixbbh+".txt"
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
        
        transmatrix.append(translist)

        hang=transmatrixfile.readline().strip()

print("状态转移概率矩阵：",transmatrix)

#加载CNN
base_model = load_model('知觉分类模块/CNN/vgg16_base_model.h5')
#加载ART
artbbh=input("输入要同步的ART的版本号：")
artwjlj="知觉分类模块/ART/ART"+artbbh+".csv"

# 读取CSV文件
prototypes_df = pd.read_csv(artwjlj, header=None)

# 将DataFrame转换为numpy数组
prototypes = prototypes_df.to_numpy()

# 打印numpy数组
print(prototypes)

class ART:
    def __init__(self, num_categories, vigilance, learning_rate,prototypes):
        self.num_categories = num_categories  # 类别数
        self.vigilance = vigilance  # 警戒值
        self.learning_rate = learning_rate  # 学习率
        self.prototypes = prototypes  # 原型初始化
        self.cate_use_list=[0]*self.num_categories#类别使用情况列表，其中每个数字代表该类别的活跃度
    

    def calculate_similarity(self, input_pattern, prototype):
        return np.dot(input_pattern, prototype) / (np.linalg.norm(input_pattern) * np.linalg.norm(prototype))
    
    
    def match(self, input_pattern):
        matched_category = None
        matched_similarity = 0
        for i in range(self.num_categories):
            similarity = self.calculate_similarity(input_pattern, self.prototypes[i])#计算输入向量(CNN输出的特征)与每个识别层神经元所对应的模式类的代表向量的相似度
            if similarity >= self.vigilance:#判断相似度是否大于等于警戒值
                if similarity > matched_similarity:#若大于警戒值，找到相似度最高的那个神经元
                    matched_category = i#激活该神经元，将输入向量归为该神经元代表的类别
                    matched_similarity = similarity

        return matched_category
    
    def update_prototype(self, input_pattern, category):
        self.prototypes[category] += self.learning_rate * (input_pattern - self.prototypes[category])
    
    def add_category(self, input_pattern):
        
        for i in range(self.num_categories):
            if np.all(self.prototypes[i]==1) == True:
                self.prototypes[i] = input_pattern
                break
        else:
            #ART 网络的类别已达上限，新类别将覆盖原有类别中最不活跃的那个类别
            print("ART 网络的所有类别已满，新类别将覆盖原有类别中最不活跃的那个类别")
            least_active_index=self.cate_use_list.index(min(self.cate_use_list))#找到最不活跃的那个类别的索引
            self.prototypes[least_active_index] = input_pattern
            

    def fit(self, data):
        for input_pattern in data:
            matched_category = self.match(input_pattern)
            if matched_category is not None:
                self.cate_use_list[matched_category]+=100#该类别活跃度加100
            for j in self.cate_use_list:
                j=int(j*0.9)#每个类别的活跃度衰减为原来的0.9倍（并取整）
        
            if matched_category is None:
                self.add_category(input_pattern)
            else:
                self.update_prototype(input_pattern, matched_category)
        
    

        
# 创建ART实例
art_model = ART(num_categories=100, vigilance=0.5, learning_rate=0,prototypes=prototypes)



print("同步完成--------------")













#各个模块








#知觉分类模块


#清空senlist
def clear_senlist():
    #清除senlist中的所有内容
    global senlist
    senlist=[]


#视觉（进入自主模式时启用）
def vision(senlist):
    
    #传感器获取占满整个视野的图像


    if imgsource == "1":
        #拍摄图像并预处理
        success=False
        while success == False:
            success, img = cap.read()
        frame = cv2.flip(img, 1)
        # show a frame
        cv2.imshow('frame', frame)
        # 设置拍摄图像的保存路径，不设置默认为当前目录
        cv2.imwrite("pic.png", frame)
    else:
        #屏幕截图，并保存为图片
        img=pyautogui.screenshot(region=(0,0,960,1080))
        img.save("pic.png")



    
    # 通过图像金字塔和滑动窗口对图像进行采样，获得采样窗口及其坐标（窗口中心相对于金字塔中心坐标的偏移比例）

    def create_image_pyramid(image, num_levels):
        pyramid = [image]
        for i in range(1, num_levels):
            new_size = (int(np.array(image).shape[1] / (2 ** i)), int(np.array(image).shape[0] / (2 ** i)))
            resized_image = image.resize(new_size)
            pyramid.append(resized_image)
        return pyramid#创建图像金字塔
    def sliding_window(image, window_size, step_size):
        for y in range(0, np.array(image).shape[0] - window_size[1], step_size):
            for x in range(0, np.array(image).shape[1] - window_size[0], step_size):
                yield (x, y, PIL.Image.fromarray(np.array(image)[y:y + window_size[1], x:x + window_size[0]]))
    def sample_image_pyramid(image_path, num_levels, window_size, step_size):
        image = PIL.Image.open(image_path)
        
        
        results = []

        pyramid = create_image_pyramid(image, num_levels)#创建图像金字塔
        for level, img in enumerate(pyramid):#对每一个金字塔层用滑动窗口进行采样
            pyramid_center = (np.array(img).shape[1] // 2, np.array(img).shape[0] // 2)#计算金字塔中心坐标
            for (x, y, window) in sliding_window(img, window_size, step_size):
                window_center = (x + window_size[0] // 2, y + window_size[1] // 2)#计算窗口中心坐标
                center_offset = (window_center[0] - pyramid_center[0], window_center[1] - pyramid_center[1])#计算窗口中心相对于金字塔中心坐标的偏移
                width_ratio = round(center_offset[0] / np.array(img).shape[1],1)#计算窗口中心相对于金字塔中心坐标的偏移比例，此即为窗口的坐标
                height_ratio = round(center_offset[1] / np.array(img).shape[0],1)#计算窗口中心相对于金字塔中心坐标的偏移比例，此即为窗口的坐标
                results.append([window,width_ratio,height_ratio])
    
        return results#采样窗口及其坐标
    
    #对图片进行采样
    image_path = 'pic.png'
    num_levels = 3  # 金字塔层数
    window_size = (128, 128)  # 窗口大小
    step_size = 128  # 步长

    samples = sample_image_pyramid(image_path, num_levels, window_size, step_size)

    
    
    #对每个采样窗口：
    for sample in samples:
        #确保图像格式正确
        img_resized = sample[0].resize((128, 128)).convert('RGB') # 调整图像尺寸为 (128, 128)，将图像通道数转化为3



        #what通路：识别窗口中的物体的类别




        # 准备图像数据
        img_array = np.array(img_resized)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)



        # 通过去除最后一层全连接层的CNN模型（VGG16）将窗口图片映射为反映图片中物体类别信息的特征（512维向量）


        features = base_model.predict(img_array)
        features = features[0]  # 去掉批次维度，形状为 (7, 7, 512)
        
        # 每张特征图进行全局平均池化（对所有特征值求平均）
        avg_features = []
        for channel in range(features.shape[2]):
            feature_map = features[:, :, channel].flatten()
            avg_value = np.mean(feature_map)
            avg_features.append(avg_value)
        features=avg_features
        

        #通过ART将CNN模型输出的特征聚类为类别
        #CNN输出的特征会激活ART网络中序号为i的神经元，该神经元会发放类别i
        winning_neurons_index = art_model.match(features)  # 获取获胜神经元在ART网络中的序号
        if winning_neurons_index!=None:
            winning_neurons_index_str=str(winning_neurons_index)
        else:
            winning_neurons_index_str="None"
        category="类别"+winning_neurons_index_str

        #更新ART
        art_model.fit([features])
    

    

        #color通路：感知图像的主要颜色



        # 定义8种颜色的调色板
        pal = np.array([
            [0, 0, 0],    # 黑色
            [255, 0, 0],  # 红色
            [0, 255, 0],  # 绿色
            [0, 0, 255],  # 蓝色
            [255, 255, 0],  # 黄色
            [255, 0, 255],  # 紫色
            [0, 255, 255],  # 青色
            [255, 255, 255],  # 白色
        ])
        #定义颜色字典
        colorlist={(0, 0, 0):'黑',
                (255, 0, 0):'红',
                (0, 255, 0):'绿',
                (0, 0, 255):'蓝',
                (255, 255, 0):'黄',
                (255, 0, 255):'紫',
                (0, 255, 255):'青',
                (255, 255, 255):'白'}

        # 计算每个像素与调色板中每个颜色的距离
        distances = distance.cdist(np.array(img_resized).reshape(-1, 3), pal, 'euclidean')

        # 找到每个像素最接近的颜色的索引
        closest_indices = np.argmin(distances, axis=1)

        # 将每个像素替换为调色板中最接近的颜色
        img_resized_flat = pal[closest_indices]
        img_resized = img_resized_flat.reshape(np.array(img_resized).shape)

        # 统计每个颜色的出现次数
        unique_colors, counts = np.unique(img_resized_flat, axis=0, return_counts=True)

        # 计算总像素数
        total_pixels = np.array(img_resized).size // 3

        # 找出主要颜色（出现次数超过 25% 的颜色）
        frequent_colors = unique_colors[counts > total_pixels * 0.25]
        frequent_colors_str=""
        if len(frequent_colors)!=0:
            for i in frequent_colors:
                frequent_colors_str+=colorlist[tuple(i)]+"色"
        else:
            frequent_colors_str="拼色"
        



        #where通路：感知窗口相对于系统的位置


        coordinate=str(sample[1])+"|"+str(sample[2])




        #整合所有通路的信息，然后将其添加入senlist
        #what通路和color通路的信息分别单独添加入senlist，然后将三个通路整合后的信息添加入senlist
        senlist.append(category)
        senlist.append(frequent_colors_str)
        senlist.append(category+"@"+frequent_colors_str+"@"+coordinate)


    
    
    #重置ART网络的警戒值为0.5
    art_model.vigilance=0.5

    return senlist

#接收输入的知觉概念列表
def input_senlist(senlist):
    
    #若进入自主模式，等待用户输入5秒
    if mode=="3":
        for i in range(50):
            root.update()
            time.sleep(0.1)
        senlist1=entinputsen.get().split(" ")
        if senlist1!=[""]:
            senlist.extend(senlist1)

    #若没进入自主模式，等待用户输入直到用户确认输入完毕
    else:
        while True:
            root.update()
            if varcbinputsen1.get()==1 and varcbinputsen2.get()==1:
                senlist1=entinputsen.get().split(" ")
                if senlist1!=[""]:
                    senlist=senlist1
                break

            time.sleep(0.1)


    if senlist_add_actlist=="1":#若启用“将上一回合输出的行为概念加入下一回合的知觉概念列表中”的机制
        senlist.extend(pactlist)
    

    return senlist





#价值分类记忆与价值系统

#发放情绪
def emo(senlist):
    #清零总的喜/哀的水平hapsum/sadsum
    hapsum=0
    sadsum=0


    #根据状态转移概率矩阵发放情绪

    #1、创建一个状态-概率堆（包括状态及其发生概率（相对于当前状态而言））
    state_chance_heap=[]

    #2、根据行为习惯列表确定当前知觉概念列表引发的行为概念列表，将两者合并为当前状态（发生概率为1），将其加入状态-概率堆中
    actlist_predict,psav_now_predict=choose_act(actlist,[])
    state_chance_heap.append([senlist+actlist_predict,1])

    #5、重复3、4两步直到预测到5个回合后
    for j in range(5):

        #3、对状态-概率堆中所有状态，若状态包含某个senlist-hap/sad组的senlist，则发放这个senlist对应的hap/sad与概率的乘积
        for state_chance in state_chance_heap:
            for i in haphablist:
                if set(i[0]).issubset(set(state_chance[0])):
                    hapsum+=int(i[1])*state_chance[1]
            for i in sadhablist:
                if set(i[0]).issubset(set(state_chance[0])):
                    sadsum+=int(i[1])*state_chance[1]

        #4、根据状态转移概率矩阵预测下一回合的状态及其概率，并用他们替换状态-概率堆中原先的内容
        state_chance_heap1=[]
        for state_chance in state_chance_heap:
            for translist in transmatrix:
                if translist[0]==state_chance[0]:
                    for i in translist[1:]:
                        state_chance_heap1.append([i[0],i[1]*state_chance[1]])
        state_chance_heap=state_chance_heap1



    #将hapsum和sadsum的值限制在0-5这一范围内，并保留小数点后1位


    if hapsum>5:
        hapsum=5
    if sadsum>5:
        sadsum=5
    hapsum=round(hapsum,1)
    sadsum=round(sadsum,1)
    #print("喜x",hapsum)
    #print("哀x",sadsum)
        
    #总价值vsum=hapsum-sadsum

    vsum=hapsum-sadsum
    #print("总价值：",vsum)

    return hapsum,sadsum,vsum




#行为与计划模块


#根据实践结果更新psav组的v值
def update_v(acthablist):
    #对在前attentive_time_step_count(=5)个时间步内被激活过的psav组（记录在psav_memory中），关注其激活后的attentive_time_step_count(=5)个时间步内的vsum（分别记为vsum1，vsum2，...）。
    #将这attentive_time_step_count个时间步的vsum的求和，然后与此psav中原来的v（v0）进行加权平均，即得新的v
    #newv=lr*（vsum1+vsum2+ ...）+(1-lr)*v0，其中lr为学习率（=0.3），newv四舍五入为整数
    lr=0.3


    for i in range(len(psav_memory)):#获取psav_memory中倒数attentive_time_step_count个时间步内的psav(们)
        psavs=psav_memory[-i-1]

        for j in psavs:#对psavs中的每一个psav，在acthablist中查找该psav
            for psav in acthablist:
                
                if sorted(j[0])==sorted(psav[0]) and sorted(j[1])==sorted(psav[1]):#若psavs中的psav与acthablist中的psav在ps和a上相同
                    
                    v0=psav[2]
                    if i ==0:
                        newv=round(vsum*lr+v0*(1-lr))
                    else:
                        newv=round(vsum*lr+v0)
                    psav[2]=newv
    
    return acthablist



#根据行为的价值（借助情绪习惯列表和状态转移概率矩阵求得）调整行为习惯
def change_acthablist(acthablist):

    #对行为习惯列表中的每个psav(psen-act-value)组，若value<=行为调整激活阈值v_adjustact_threshold，
    #根据状态转移概率矩阵和情绪习惯列表对该psav组进行优化：
    for psav in acthablist:
        if psav[2]<=v_adjustact_threshold:




            bxact=[]#备选act
            bxvalue=v_adjustact_threshold#备选value


        
            #在状态转移概率矩阵中查找包含psen且不包含行为空间外的行为的状态。将此状态中除psen外的部分（肯定在行为空间内）作为备选act
            for translist in transmatrix:

                #判断translist[0]-psenlist的差集是否被allact包含，即判断translist[0]中除了psenlist外，是否有做不到的行为
                zuobudao=0
                diffset=[]
                for i in translist[0]:
                    if i not in psav[0]:
                        diffset.append(i)
                for i in diffset:
                    if i not in allact:
                        zuobudao=1
                        break
                if zuobudao==0:
                    #判断psenlist是否⊂translist[0]
                    for psen in psav[0]:
                        if psen not in translist[0]:
                            break
                    else:#没有执行break说明psenlist⊂translist[0]且translist[0]中除了psenlist外，没有做不到的行为
                        
                        #对每个备选act：将其与psen结合作为初始状态，然后将这个初始状态导入状态转移概率矩阵中，预测出接下来attentive_time_step_count个时间步的状态及其发生概率。
                        allresult=[]#所有时间步的状态及其发生概率
                        result=[]#某一时间步的状态及其发生概率
                    
                        result=sorted(translist[1:], key=operator.itemgetter(1), reverse=True)[0:3]#获取translist中发生概率前三大的状态及其发生概率
                        allresult.extend(result)
                        for i in range(attentive_time_step_count-1):#对attentive_time_step_count-1个时间步进行预测
                            for state_chance_times in result:
                                for translist in transmatrix:
                                    if translist[0]==state_chance_times[0]:
                                        result=sorted(translist[1:], key=operator.itemgetter(1), reverse=True)[0:3]#获取translist中发生概率前三大的状态及其发生概率
                                        allresult.extend(result)
                            

                        #对这attentive_time_step_count个时间步的状态，先根据 函数：发放情绪 求出每个状态的价值，再将状态的价值与状态发生的概率相乘，最后对这些乘积求和，以此作为这个备选act的备选value
                        vsum1=0
                        for state_chance_times in allresult:  
                            hapsum2,sadsum2,vsum2=emo(state_chance_times[0]) 
                            vsum1+=vsum2*state_chance_times[1]

                        #选出备选value最高的备选act
                        if vsum1>bxvalue:
                            bxvalue=vsum1
                            bxact=diffset
                        
            #1、若其备选value高于v_adjustact_threshold，将其记作newact，将其备选value记作newvalue
            if bxvalue>v_adjustact_threshold:
                newact=bxact
                newvalue=bxvalue
                #往行为习惯列表中添加一个新的psav组：psen-newact-newvalue
                acthablist.append([psav[0],newact,newvalue])
            #2、若其备选value不高于v_adjustact_threshold，往原psav组的act（实际上是actlist）中随机地添加或删除行为，将结果作为newact，newvalue则为v_adjustact_threshold+1（对优化后的行为的价值持乐观预期）
            else:
                if random.random()<0.5:
                    newact=copy.deepcopy(psav[1])
                    newact.append(random.choice(list(allact)))
                    newvalue=v_adjustact_threshold+1
                    print('random:',random.choice(list(allact)))
                    print('psav[0]:',psav[0])
                    print('newact:',newact)
                    #往行为习惯列表中添加一个新的psav组：psen-newact-newvalue        
                    acthablist.append([psav[0],newact,newvalue])
                    print(acthablist)
                
                else:
                    if psav[1]!=[]:
                        removeact=psav[1][random.randint(0, len(psav[1]) - 1)]
                        newact=copy.deepcopy(psav[1])
                        newact.remove(removeact)
                        newvalue=v_adjustact_threshold+1
                        #往行为习惯列表中添加一个新的psav组：psen-newact-newvalue        
                        acthablist.append([psav[0],newact,newvalue])


    #若该psav组已是attentive_time_step_count个时间步之前发生的了，且其value<=v_adjustact_threshold，将其移除        
    senlist_actlist_vsum=memorylist[-attentive_time_step_count]
    for psav in copy.deepcopy(acthablist):
        if psav[0]==senlist_actlist_vsum[0] and psav[1]==senlist_actlist_vsum[1] and psav[2]<=v_adjustact_threshold:
            acthablist.remove(psav)        



            
    
    #删除自发行为
    acthablist1=[]
    for psav in acthablist:
        if psav[0]!=[]:
            acthablist1.append(psav)
    acthablist=acthablist1
    

    return acthablist

            
#根据知觉概念列表和行为习惯选择将执行的行为概念
def choose_act(actlist,psav_now):
    #注：当行为从一个psav组中被选择出来，这个psav组会被记录到此回合用到的psav（psav_now）中

    psav_now=[]
    actlist=[]
    find=False
    
    #step0、如果senlist=想+某行为，输出该行为

    for sen in senlist:
        if sen!="":
            if sen[0]=="想":
                actlist.extend([sen[1:]])

    #step1、遍历acthablist，若其中某些psav组的psen=senlist，输出v最大（需大于v_adjustact_threshold）的那个psav组中的act


    vmax=v_adjustact_threshold
    for psav in acthablist:
        if sorted(psav[0])==sorted(senlist):
            if psav[2]>vmax:
                vmax=psav[2]
                actlist=psav[1]
                find=True#表示step1中找到了符合要求的psav组
                psav_now.append(psav.copy())

    #step2（模糊匹配）、若step1中未找到符合要求的psav组，扩大搜索范围：遍历acthablist，若某些psav组的psen⊂senlist，输出v最大（需大于v_adjustact_threshold）的那个psav组中的act


    if find==False:
        for psav in acthablist:
            for i in psav[0]:
                if i not in senlist:
                    break
            else:
                if psav[2]>vmax:
                    vmax=psav[2]
                    actlist=psav[1]
                    find=True#表示step2中找到了符合要求的psav组
                    psav_now.append(psav.copy())

    #step3、若step1和step2中都未找到符合要求的psav组，则不输出行为

    if find==False:
        psav_now.append(["未激活","未激活",0])



    #若整理好的行为概念（actlist）与senlist构成的ps-a在acthablist中没有与之对应的psav组，这个psav组也会被记录到psav_now中

    for psav in acthablist:
        if sorted(psav[0])==sorted(senlist) and sorted(psav[1])==sorted(actlist):
            break
    else:
        psav_now.append([senlist,actlist,0])

    return actlist,psav_now
    
#添加psav组
def add_psav(acthablist):

    #若整理好的行为概念（actlist）与senlist构成的ps-a在acthablist中没有与之对应的psav组，则将其作为新的psav组添加入acthablist（v值初始化为0）
    
    for psav in acthablist:
        if sorted(psav[0])==sorted(senlist) and sorted(psav[1])==sorted(actlist):
            break
    else:
        acthablist.append([senlist,actlist,0])

    return acthablist


#更新psav_memory
def update_psav_memory(psav_now,psav_memory):
    #psav_memory是一个列表，其中按从旧到新的先后顺序存储了最近attentive_time_step_count个时间步用过的psav（们）
    #在psav_memory中添加psav_now，并移除psav_memory中最旧的psav（们）
    if len(psav_memory) >= attentive_time_step_count:
        psav_memory.pop(0)
    psav_memory.append(psav_now)

    return psav_memory




#对行为进行分解细化
def act_detail(want_learn_list):
    counts=0
    if mode!="3":#若未进入自主模式
        while True:
            root.update()
            if varcbcounts1.get()==1 and varcbcounts2.get()==1:
                counts=int(entcounts.get())
                varcbcounts1.set(0)
                varcbcounts2.set(0)
                break
            import time
            time.sleep(0.1)
    '''
    counts=0
    if actlist!=[]:
        counts=int(input("分解次数:"))
    '''

    act_detail_list=copy.deepcopy(actlist)
    act_detail_list1=[]

    if counts>=1:
        for i in range(counts):
        
            for act in act_detail_list:
            #在状态转移概率矩阵中寻找要做的行为的前置状态，若未搜索到，将该行为添加入学习需求列表want_learn_list中
                find=False
                for translist in transmatrix:
                    for state_chance_times in translist[1:]:
                        if act in state_chance_times[0] and state_chance_times[1]>=0.5:
                            act_detail_list1.extend(translist[0])
                            find=True
                            print("要做",act,"先做",translist[0])

                if find==False:        
                    print("未搜索到",act,"的前置状态")
                    want_learn_list.append(act)
            
            act_detail_list=copy.deepcopy(act_detail_list1)
            act_detail_list1=[]



    #对学习需求列表进行去重
    list1=[]
    for i in want_learn_list:
        if i not in list1:
            list1.append(i)
    want_learn_list=list1

    #输出学习需求列表
    if want_learn_list!=[]:
        print("需要学习以下行为：",want_learn_list)
    
    return act_detail_list,want_learn_list
    

#输出行为概念并执行
def output_act(actlist):
    if "报告意识体验" in actlist:
        ACT(senlist,hapsum,sadsum,vsum,actlist).report_qualia()
    if "更新SOM" in actlist:
        ACT(senlist,hapsum,sadsum,vsum,actlist).update_som()
    if "pressA" in actlist:
        ACT(senlist,hapsum,sadsum,vsum,actlist).pressA()
    if "pressD" in actlist:
        ACT(senlist,hapsum,sadsum,vsum,actlist).pressD()
    if "pressW" in actlist:
        ACT(senlist,hapsum,sadsum,vsum,actlist).pressW()
    if "pressS" in actlist:
        ACT(senlist,hapsum,sadsum,vsum,actlist).pressS()
    if "scrollup" in actlist:
        ACT(senlist,hapsum,sadsum,vsum,actlist).scrollup()
    if "scrolldown" in actlist:
        ACT(senlist,hapsum,sadsum,vsum,actlist).scrolldown()
    if "内省" in actlist:
        ACT(senlist,hapsum,sadsum,vsum,actlist).introspect()
   


        




#记忆模块



#将当前的[senlist,actlist,vsum]加入自传体记忆memorylist中
def add_memorylist(senlist,actlist,vsum,memorylist):
    memorylist.append([senlist,actlist,vsum])
    return memorylist





#世界模型


#根据当前状态state更新状态转移概率矩阵
def update_transmatrix(transmatrix):

    #更新状态转移概率矩阵中的状态和次数
    for translist in transmatrix:
        if translist[0]==psenlist+pactlist:
            
            cunzai=False
            
            for i in translist[1:]:
                if i[0]==senlist+actlist:
                    i[2]+=1
                    i[1]=i[1]*0.8+1*0.2
                    cunzai=True
                else:
                    i[1]=i[1]*0.8+0*0.2 
                    
            if cunzai==False:
                translist.append([senlist+actlist,1,1])
            
            break
    else:
        transmatrix.append([psenlist+pactlist,[senlist+actlist,1,1]])


    #print("截至目前的状态转移概率矩阵为：",transmatrix)
    
    return transmatrix



#根据状态转移矩阵预测接下来各状态的发生概率，以及最可能发生的状态
def predict_next_state_chance():
    predict_state_chance=[]
    predict_max_chance=-1
    predict_max_state="未发现"
    
    for translist in transmatrix:
        if translist[0]==senlist+actlist:
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
    












#全局神经工作空间GW






#扩展知觉概念列表senlist
def extend_senlist():

    #1、extended_senlist=pactlist（上一回合的行为概念列表）+senlist（本回合知觉概念列表）+其他
    #其他包含内省出来的内容
    qita=introcontent
    extended_senlist=pactlist+senlist+qita
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




#可视化界面初始化
from tkinter import *
root=Tk()
root.title("苍穹3号")
root.geometry('1000x800')


lbGW=Label(root,text="全局神经工作空间GW")
lbGW.grid(row=0,column=1)



lbsenpart=Label(root,text="知觉分类模块")
lbsenpart.grid(row=1,column=0)
lbinputsen=Label(root,text="输入当前知觉概念列表,各知觉概念之间用空格隔开。（若输入：想+某行为，系统将会输出该行为）")
lbinputsen.grid(row=2,column=0)
entinputsen=Entry(root,width=40)
entinputsen.grid(row=3,column=0)

varcbinputsen1=IntVar()
varcbinputsen2=IntVar()
cbinputsen1=Checkbutton(root,text="知觉概念列表准备完毕",variable=varcbinputsen1,onvalue=1,offvalue=0)
cbinputsen1.grid(row=4,column=0)
cbinputsen2=Checkbutton(root,text="提交知觉概念列表",variable=varcbinputsen2,onvalue=1,offvalue=0)
cbinputsen2.grid(row=5,column=0)

lbsenlist=Label(root,text="知觉概念列表：扩展前（当前从环境中获得的知觉内容）")
lbsenlist.grid(row=6,column=0)
txsenlist=Text(root,width=40,height=5)
txsenlist.grid(row=7,column=0)

lbextended_senlist=Label(root,text="知觉概念列表：扩展后（既是注意力选择后的结果，也模拟工作记忆的内容）")
lbextended_senlist.grid(row=8,column=0)
txextended_senlist=Text(root,width=40,height=5)
txextended_senlist.grid(row=9,column=0)

varcbbaocun1=IntVar()
varcbbaocun2=IntVar()
cbbaocun1=Checkbutton(root,text="保存当前记忆",variable=varcbbaocun1,onvalue=1,offvalue=0)
cbbaocun1.grid(row=10,column=0)
cbbaocun2=Checkbutton(root,text="确认保存当前记忆",variable=varcbbaocun2,onvalue=1,offvalue=0)
cbbaocun2.grid(row=11,column=0)


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





#控制流
while True:
    
    #更新可视化界面
    root.update()

    #清空senlist
    clear_senlist()

    #若进入自主模式，启用视觉
    if mode=='3':
        senlist=vision(senlist)
    
    #接收输入的知觉概念列表
    senlist=input_senlist(senlist)

    #更新可视化界面
    varcbinputsen1.set(0)
    varcbinputsen2.set(0)
    senliststr=','.join(senlist)
    txsenlist.configure(state='normal')
    txsenlist.delete(0.0,'end')
    txsenlist.insert(0.0,senliststr)
    txsenlist.configure(state='disabled')

    #扩展知觉概念列表senlist
    senlist=extend_senlist()
    
    #更新可视化界面

    extended_senliststr=','.join(senlist)
    txextended_senlist.configure(state='normal')
    txextended_senlist.delete(0.0,'end')
    txextended_senlist.insert(0.0,extended_senliststr)
    txextended_senlist.configure(state='disabled')

    #发放情绪
    hapsum,sadsum,vsum=emo(senlist)

    #更新可视化界面
    lbhapsum.configure(text="喜的值:"+str(hapsum))
    lbsadsum.configure(text="哀的值:"+str(sadsum))
    lbvsum.configure(text="总价值:"+str(vsum))
    
    content=''
    for senlist_hap in haphablist:
        cont_senlist=''
        for i in senlist_hap[0]:
            cont_senlist+=str(i)+"。"
        
        hap=senlist_hap[1]

        line=cont_senlist+"；"+str(hap)
        content+=str(line)+"\n"*2
    txhaphablist.configure(state='normal')
    txhaphablist.delete(0.0,'end')
    txhaphablist.insert(0.0,content)
    txhaphablist.configure(state='disabled')
    
    content=''
    for senlist_sad in sadhablist:
        cont_senlist=''
        for i in senlist_sad[0]:
            cont_senlist+=str(i)+"。"
        
        sad=senlist_sad[1]

        line=cont_senlist+"；"+str(sad)
        content+=str(line)+"\n"*2
    txsadhablist.configure(state='normal')
    txsadhablist.delete(0.0,'end')
    txsadhablist.insert(0.0,content)
    txsadhablist.configure(state='disabled')

    if adjust_acthablist=="1":#若允许调整行为习惯列表
        #根据实践结果更新psav组的v值
        acthablist=update_v(acthablist)

        #根据行为的价值（借助情绪习惯列表和状态转移概率矩阵求得）调整行为习惯
        acthablist=change_acthablist(acthablist)

    #根据知觉概念列表和行为习惯选择将执行的行为概念
    actlist,psav_now=choose_act(actlist,psav_now)

    if adjust_acthablist=="1":#若允许调整行为习惯列表
        #添加psav组
        acthablist=add_psav(acthablist)

    #更新psav_memory
    psav_memory=update_psav_memory(psav_now,psav_memory)

    #更新可视化界面
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
        content+=str(line)+"\n"*2
    
    txacthablist.configure(state='normal')
    txacthablist.delete(0.0,'end')
    txacthablist.insert(0.0,content)
    txacthablist.configure(state='disabled')
    
    txactlist.configure(state='normal')
    txactlist.delete(0.0,'end')
    txactlist.insert(0.0,','.join(actlist))
    txactlist.configure(state='disabled')

    #对行为进行分解细化
    act_detail_list,want_learn_list=act_detail(want_learn_list)

    #更新可视化界面
    txact_detail_list.configure(state='normal')
    txact_detail_list.delete(0.0,'end')
    txact_detail_list.insert(0.0,','.join(act_detail_list))
    txact_detail_list.configure(state='disabled')

    #输出行为概念并执行
    output_act(actlist)

    #将当前的[senlist,actlist,vsum]加入自传体记忆memorylist中
    memorylist=add_memorylist(senlist,actlist,vsum,memorylist)

    #更新可视化界面
    memoryliststr=""
    for i in memorylist:
        memoryliststr+=','.join(i[0])+"；"+','.join(i[1])+"；"+str(i[2])+"\n"*2
    txmemorylist.configure(state='normal')
    txmemorylist.delete(0.0,'end')
    txmemorylist.insert(0.0,memoryliststr)
    txmemorylist.configure(state='disabled')

    #根据当前状态state更新状态转移概率矩阵
    transmatrix=update_transmatrix(transmatrix)

    #根据状态转移矩阵预测接下来各状态的发生概率，以及最可能发生的状态
    predict_state_chance,predict_max_state,predict_max_chance=predict_next_state_chance()

    #更新可视化界面
    content=''
    for translist in transmatrix:
        cont_translist=''
        cont_translist+='。'.join(translist[0])
        for i in translist[1:]:
            cont_translist+='；'+'。'.join(i[0])+"、"+str(i[1])+"、"+str(i[2])

        line=cont_translist
        content+=str(line)+"\n"*2
    txtransmatrix.configure(state='normal')
    txtransmatrix.delete(0.0,'end')
    txtransmatrix.insert(0.0,content)
    txtransmatrix.configure(state='disabled')

    txpredict_state_chance.configure(state='normal')
    txpredict_state_chance.delete(0.0,'end')
    if predict_state_chance=="未发现":
        txpredict_state_chance.insert(0.0,"未发现")
    else:
        content=''
        for i in predict_state_chance:
            content+='。'.join(i[0])+"、"+str(i[1])+"、"+str(i[2])+"\n"*2
        txpredict_state_chance.insert(0.0,content)
    txpredict_state_chance.configure(state='disabled')
    
    if predict_state_chance=="未发现":
        lbpredict_max_state.configure(text="接下来最可能发生的状态为:未发现")
    else:
        lbpredict_max_state.configure(text="接下来最可能发生的状态为:"+",".join(predict_max_state))
    lbpredict_max_chance.configure(text="发生概率为:"+str(predict_max_chance))
    

    #将psenlist更新为senlist，pactlist更新为actlist
    psenlist=copy.deepcopy(senlist)
    pactlist=copy.deepcopy(actlist)

    #若未进入不可变模式，询问是否保存当前心智内容
    if mode!="0":
        from pathlib import Path
        #baocun=input("是否要保存当前记忆？（是：1，否：0）")
        if varcbbaocun1.get()==1 and varcbbaocun2.get()==1:
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

            #保存自传体记忆
            memorybbh=input("输入要保存的自传体记忆的版本号：")
            memorywjlj="自传体记忆/自传体记忆"+memorybbh+".txt"
            content=''
            for senlist_actlist_vsum in memorylist:
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
            transwjlj="状态转移概率矩阵/状态转移概率矩阵"+transbbh+".txt"
            content=''
            for translist in transmatrix:
                cont_translist=''
                cont_translist+='。'.join(translist[0])
                for i in translist[1:]:
                    cont_translist+='；'+'。'.join(i[0])+"、"+str(i[1])+"、"+str(i[2])

                line=cont_translist
                content+=str(line)+"\n"
            
            with open(transwjlj,"w",encoding='utf-8') as transfile:
                transfile.write(content)


            #保存ART
            artbbh=input("输入要保存的ART模型的版本号：")
            artwjlj="知觉分类模块/ART/ART"+artbbh+".csv"
            df = pd.DataFrame(art_model.prototypes)# 将prototypes转换为DataFrame
            # 保存为CSV文件，不包含标题行，每行之间没有空行
            df.to_csv(artwjlj, index=False, header=False)


            print("保存成功——————————————")
            varcbbaocun1.set(0)
            varcbbaocun2.set(0)
    
    #若进入自主模式，睡眠一段时间
    if mode=="3":
        time.sleep(sleeptime)