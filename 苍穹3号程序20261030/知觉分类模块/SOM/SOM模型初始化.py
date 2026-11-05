import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import load_model
from PIL import Image
import io
import numpy as np
import pandas as pd
from minisom import *
import matplotlib.pyplot as plt
import os
import cv2

# 加载模型
base_model = load_model('D:/人生目标/自然层面的解放/意识上传/人工心智载体/人工脑/意识/初级意识/意识引擎/苍穹系列/苍穹3号/苍穹3号程序-备份/苍穹3号程序/知觉分类模块/CNN/vgg16_base_model.h5')


# 准备图像数据
img_resized = cv2.resize(cv2.imread("init_pic.png"), (128, 128))  # 调整图像尺寸为 (128, 128)
img_array = np.array(img_resized)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)

# 提取特征
features = base_model.predict(img_array)
features = features.flatten()  # 展平特征向量
print("Features :", features)


# 设置SOM参数
som_shape = (10, 10)  # SOM网格的大小
som = MiniSom(som_shape[0], som_shape[1], features.shape[-1], sigma=0.1, learning_rate=0.3)

# 初始化SOM
som.random_weights_init(features.reshape(1, -1))

#保存SOM模型
sombbh=input("输入要保存的SOM的版本号：")
somwjlj="SOM"+sombbh+".p"
with open(somwjlj, 'wb') as outfile:
        pickle.dump(som, outfile)
