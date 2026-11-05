import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import load_model
from PIL import Image
import io
import numpy as np
import pandas as pd
from minisom import MiniSom
import matplotlib.pyplot as plt
import os
import cv2
import pickle
import random

# 加载模型
base_model = load_model('D:/人生目标/自然层面的解放/意识上传/人工心智载体/人工脑/意识/初级意识/意识引擎/苍穹系列/苍穹3号/苍穹3号程序/知觉分类模块/CNN/vgg16_base_model.h5')

# 图片文件夹路径
foldername1 = "D:/人生目标/自然层面的解放/意识上传/人工心智载体/人工脑/意识/初级意识/意识引擎/苍穹系列/苍穹3号/苍穹3号程序/知觉分类模块/图片/tiny-imagenet-200/test/images"

# 获取文件夹中的所有图片路径
def get_image_paths(folder):
    image_paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_paths.append(os.path.join(root, file))
    return image_paths

image_paths = get_image_paths(foldername1)

# 随机选择100张图片来提取特征
random.shuffle(image_paths)
selected_image_paths = image_paths[:100]  # 选择前100张图片

features_list = []

for img_path in selected_image_paths:
    img_resized = Image.open(img_path).resize((128, 128))  # 调整图像尺寸为 (128, 128)
    img_resized = img_resized.convert('RGB')#将图像通道数转化为3
    img_array = np.array(img_resized)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # 提取特征
    features = base_model.predict(img_array)
    features = features[0]  # 去掉批次维度，形状为 (7, 7, 512)

    '''
    # 对每张特征图找到最大的特征值
    max_features = []
    for channel in range(features.shape[2]):
        feature_map = features[:, :, channel].flatten()
        max_value = np.max(feature_map)
        max_features.append(max_value)

    features_list.append(max_features)
    '''
    '''
    # 对每张特征图找到所有正的特征值求和
    positive_sum_features = []
    for channel in range(features.shape[2]):
        feature_map = features[:, :, channel].flatten()
        positive_sum = np.sum(feature_map[feature_map > 0])
        positive_sum_features.append(positive_sum)

    features_list.append(positive_sum_features)
    '''
    # 对每张特征图找到所有特征值求平均
    avg_features = []
    for channel in range(features.shape[2]):
        feature_map = features[:, :, channel].flatten()
        avg_value = np.mean(feature_map)
        avg_features.append(avg_value)

    features_list.append(avg_features)
    
    

# 将特征列表转换为numpy数组
features_array = np.array(features_list)


prototypes=np.around(features_array, decimals=3)#用这100张图片的特征向量分别初始化ART的100个神经元，并将数值保留到小数点后3位
print(prototypes)



# 保存prototypes

# 将prototypes转换为DataFrame
df = pd.DataFrame(prototypes)
# 保存为CSV文件，不包含标题行，每行之间没有空行
df.to_csv('prototypes.csv', index=False, header=False)
