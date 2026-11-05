#知觉分类模块
import time
import PIL.Image
import numpy as np
import pandas as pd
import cv2
import pyautogui
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
from scipy.spatial import distance

import 公共状态


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
            for idx in range(len(self.cate_use_list)):
                self.cate_use_list[idx]=int(self.cate_use_list[idx]*0.9)#每个类别的活跃度衰减为原来的0.9倍（并取整）

            if matched_category is None:
                self.add_category(input_pattern)
            else:
                self.update_prototype(input_pattern, matched_category)



#加载CNN和ART
def 加载知觉模型():
    #加载CNN
    公共状态.base_model = load_model('知觉分类模块/CNN/vgg16_base_model.h5')
    #加载ART
    artbbh=input("输入要同步的ART的版本号：")
    artwjlj="意识数据/ART/ART"+artbbh+".csv"

    # 读取CSV文件
    prototypes_df = pd.read_csv(artwjlj, header=None)

    # 将DataFrame转换为numpy数组
    prototypes = prototypes_df.to_numpy()

    # 打印numpy数组
    print(prototypes)

    # 创建ART实例
    公共状态.art_model = ART(num_categories=100, vigilance=0.5, learning_rate=0,prototypes=prototypes)


#初始化摄像头
def 初始化摄像头():
    # 如果是调用笔记本自带的摄像头，参数就为0；如果是外置USB摄像头，参数就为1。
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    # 设置一下摄像头窗口的宽高，参数3代表宽度
    cap.set(3, 1280)
    # 参数4代表的高度
    cap.set(4, 1280)
    # 参数10代表亮度
    cap.set(10, 100)
    公共状态.cap = cap


#清空senlist
def clear_senlist():
    #清除senlist中的所有内容
    公共状态.senlist=[]


#视觉（进入自主模式时启用）
def vision(senlist):

    #传感器获取占满整个视野的图像


    if 公共状态.imgsource == "1":
        #拍摄图像并预处理
        success=False
        while success == False:
            success, img = 公共状态.cap.read()
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


        features = 公共状态.base_model.predict(img_array, verbose=0)
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
        winning_neurons_index = 公共状态.art_model.match(features)  # 获取获胜神经元在ART网络中的序号
        if winning_neurons_index!=None:
            winning_neurons_index_str=str(winning_neurons_index)
        else:
            winning_neurons_index_str="None"
        category="类别"+winning_neurons_index_str

        #更新ART
        公共状态.art_model.fit([features])




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
    公共状态.art_model.vigilance=0.5

    return senlist

#接收输入的知觉概念列表
def input_senlist(senlist):

    #若进入自主模式，等待用户输入5秒
    if 公共状态.mode=="3":
        for i in range(50):
            公共状态.root.update()
            time.sleep(0.1)
        senlist1=公共状态.entinputsen.get().split(" ")
        if senlist1!=[""]:
            senlist.extend(senlist1)

    #若没进入自主模式，等待用户输入直到用户确认输入完毕
    else:
        while True:
            公共状态.root.update()
            if 公共状态.varcbinputsen1.get()==1 and 公共状态.varcbinputsen2.get()==1:
                senlist1=公共状态.entinputsen.get().split(" ")
                if senlist1!=[""]:
                    senlist=senlist1
                break

            time.sleep(0.1)



    return senlist
