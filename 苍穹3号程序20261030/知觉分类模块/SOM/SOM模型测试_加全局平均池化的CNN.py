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
base_model = load_model('D:/人生目标/自然层面的解放/意识上传/人工心智载体/人工脑/意识/初级意识/意识引擎/苍穹系列/苍穹3号/苍穹3号程序-备份/苍穹3号程序/知觉分类模块/CNN/vgg16_base_model.h5')

# 图片文件夹路径
foldername1 = "D:\\人生目标\\自然层面的解放\\意识上传\\人工心智载体\\人工脑\\意识\\初级意识\\意识引擎\\苍穹系列\\苍穹3号\\苍穹3号程序-备份\\苍穹3号程序\\训练数据\\图片\\tiny-imagenet-200\\train\\n01443537\\images"
foldername2 = "D:\\人生目标\\自然层面的解放\\意识上传\\人工心智载体\\人工脑\\意识\\初级意识\\意识引擎\\苍穹系列\\苍穹3号\\苍穹3号程序-备份\\苍穹3号程序\\训练数据\\图片\\tiny-imagenet-200\\train\\n02415577\\images"
foldername3 = "D:\\人生目标\\自然层面的解放\\意识上传\\人工心智载体\\人工脑\\意识\\初级意识\\意识引擎\\苍穹系列\\苍穹3号\\苍穹3号程序-备份\\苍穹3号程序\\训练数据\\图片\\金鱼"
foldername4 = "D:\\人生目标\\自然层面的解放\\意识上传\\人工心智载体\\人工脑\\意识\\初级意识\\意识引擎\\苍穹系列\\苍穹3号\\苍穹3号程序-备份\\苍穹3号程序\\训练数据\\图片\\金鱼2"


foldername5 = "D:\\人生目标\\自然层面的解放\\意识上传\\人工心智载体\\人工脑\\意识\\初级意识\\意识引擎\\苍穹系列\\苍穹3号\\苍穹3号程序-备份\\苍穹3号程序\\训练数据\\图片\\金鱼x45"
foldername6 = "D:\\人生目标\\自然层面的解放\\意识上传\\人工心智载体\\人工脑\\意识\\初级意识\\意识引擎\\苍穹系列\\苍穹3号\\苍穹3号程序-备份\\苍穹3号程序\\训练数据\\图片\\岩羊x45"

# 获取文件夹中的所有图片路径
def get_image_paths(folder):
    image_paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_paths.append(os.path.join(root, file))
    return image_paths

image_paths = get_image_paths(foldername2)

# 调试信息：检查 image_paths 是否为空
if not image_paths:
    print(f"没有找到任何图片在文件夹: {foldername1}")
else:
    print(f"找到 {len(image_paths)} 张图片在文件夹: {foldername1}")

# 随机选择100张图片来提取特征
random.shuffle(image_paths)
selected_image_paths = image_paths[:100]  # 选择前100张图片

# 调试信息：检查 selected_image_paths 是否为空
if not selected_image_paths:
    print("没有选择到任何图片")
else:
    print(f"选择了 {len(selected_image_paths)} 张图片")

features_list = []

for img_path in selected_image_paths:
    try:
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
        
    except Exception as e:
        print(f"处理图片 {img_path} 时出错: {e}")

# 将特征列表转换为numpy数组
features_array = np.array(features_list)

# 调试信息：检查 features_array 是否为空
if features_array.size == 0:
    print("没有提取到任何特征")
else:
    print(f"提取了 {features_array.shape[0]} 个特征向量")

# 加载用户指定的 SOM 模型
sombbh = input("输入要测试的SOM的版本号：")
somwjlj = "SOM" + sombbh + ".p"
with open(somwjlj, 'rb') as infile:
    som = pickle.load(infile)

# 测试 SOM 模型并输出激活的神经元坐标
for idx, features in enumerate(features_array):
    winning_neurons_position = som.winner(features)  # 获取获胜神经元在SOM网络中的位置（i，j）
    print(f"图片 {selected_image_paths[idx]} 激活的神经元坐标: ({winning_neurons_position[0]}, {winning_neurons_position[1]})")


# 初始化一个字典来存储神经元坐标及其激活次数
neuron_activation_count = {}

# 测试 SOM 模型并记录神经元激活次数
for idx, features in enumerate(features_array):
    winning_neurons_position = som.winner(features)  # 获取获胜神经元在SOM网络中的位置（i，j）
    neuron_position = (winning_neurons_position[0], winning_neurons_position[1])
    
    # 更新字典中的激活次数
    if neuron_position in neuron_activation_count:
        neuron_activation_count[neuron_position] += 1
    else:
        neuron_activation_count[neuron_position] = 1

# 输出神经元坐标及其激活次数
print("神经元坐标及其激活次数:")
for neuron_position, count in neuron_activation_count.items():
    print(f"神经元坐标: {neuron_position}, 激活次数: {count}")