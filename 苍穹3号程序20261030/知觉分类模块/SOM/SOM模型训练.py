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
import pickle
import random



#加载CNN和SOM模型
base_model = load_model('D:/人生目标/自然层面的解放/意识上传/人工心智载体/人工脑/意识/初级意识/意识引擎/苍穹系列/苍穹3号/苍穹3号程序-备份/苍穹3号程序/知觉分类模块/CNN/vgg16_base_model.h5')
sombbh=input("输入要同步的SOM的版本号：")
somwjlj="SOM"+sombbh+".p"
with open(somwjlj, 'rb') as infile:
    som = pickle.load(infile)


#指定训练次数
train_num=int(input("输入训练次数："))

#指定训练图片文件夹
foldername1="D:/人生目标/自然层面的解放/意识上传/人工心智载体/人工脑/意识/初级意识/意识引擎/苍穹系列/苍穹3号/苍穹3号程序-备份/苍穹3号程序/训练数据/图片/tiny-imagenet-200/test/images"
foldername2="D:/人生目标/自然层面的解放/意识上传/人工心智载体/人工脑/意识/初级意识/意识引擎/苍穹系列/苍穹3号/苍穹3号程序-备份/苍穹3号程序/训练数据/图片/自己收集的图片"

foldername=foldername1

#训练SOM
for i in range(train_num):
    print("第",i+1,"次训练")
    #随机选取文件夹中的文件
    filename=random.choice(os.listdir(foldername))
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # 检查文件扩展名
        img_path = foldername+"/"+filename
        img_resized = Image.open(img_path).resize((128, 128))#读取图像并调整图像尺寸为 (128, 128)
        img_resized = img_resized.convert('RGB')#将图像通道数转化为3
        img_array = np.array(img_resized)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # 提取特征
        features = base_model.predict(img_array)
        features = features.flatten()  # 展平特征向量
        print("Features :", features)


        # 更新 SOM
        som.train_random(features.reshape(1, -1), num_iteration=1)
        print("SOM updated.")

            
        
            

#保存SOM模型
sombbh=input("输入要保存的SOM的版本号：")
somwjlj="SOM"+sombbh+".p"
with open(somwjlj, 'wb') as outfile:
        pickle.dump(som, outfile)
