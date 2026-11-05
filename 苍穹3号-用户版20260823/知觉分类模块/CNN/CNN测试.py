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
foldername1 = "D:\\人生目标\\自然层面的解放\\意识上传\\人工心智载体\\人工脑\\意识\\初级意识\\意识引擎\\苍穹系列\\苍穹3号\\苍穹3号程序\\知觉分类模块\\图片\\tiny-imagenet-200\\train\\n01443537\\images"
foldername2 = "D:\\人生目标\\自然层面的解放\\意识上传\\人工心智载体\\人工脑\\意识\\初级意识\\意识引擎\\苍穹系列\\苍穹3号\\苍穹3号程序\\知觉分类模块\\图片\\tiny-imagenet-200\\train\\n02415577\\images"
foldername3 = "D:\\人生目标\\自然层面的解放\\意识上传\\人工心智载体\\人工脑\\意识\\初级意识\\意识引擎\\苍穹系列\\苍穹3号\\苍穹3号程序\\知觉分类模块\\图片\\金鱼"
foldername4 = "D:\\人生目标\\自然层面的解放\\意识上传\\人工心智载体\\人工脑\\意识\\初级意识\\意识引擎\\苍穹系列\\苍穹3号\\苍穹3号程序\\知觉分类模块\\图片\\金鱼2"


foldername5 = "D:\\人生目标\\自然层面的解放\\意识上传\\人工心智载体\\人工脑\\意识\\初级意识\\意识引擎\\苍穹系列\\苍穹3号\\苍穹3号程序\\知觉分类模块\\图片\\金鱼x45"
foldername6 = "D:\\人生目标\\自然层面的解放\\意识上传\\人工心智载体\\人工脑\\意识\\初级意识\\意识引擎\\苍穹系列\\苍穹3号\\苍穹3号程序\\知觉分类模块\\图片\\岩羊x45"
# 获取文件夹中的所有图片路径
def get_image_paths(folder):
    image_paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_paths.append(os.path.join(root, file))
    return image_paths

image_paths = get_image_paths(foldername5)+get_image_paths(foldername6)

# 选择所有图片来提取特征
selected_image_paths = image_paths  # 选择所有图片

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
        features = features.flatten()  # 展平特征向量
        features_list.append(features)
    except Exception as e:
        print(f"处理图片 {img_path} 时出错: {e}")

# 将特征列表转换为numpy数组
features_array = np.array(features_list)



# 计算特征向量两两之间的夹角
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def angle_between_vectors(vec1, vec2):
    cos_sim = cosine_similarity(vec1, vec2)
    angle_rad = np.arccos(np.clip(cos_sim, -1.0, 1.0))  # 防止数值超出范围
    angle_deg = np.degrees(angle_rad)
    return angle_deg

num_features = features_array.shape[0]
angles = []

for i in range(num_features):
    for j in range(i + 1, num_features):
        angle = angle_between_vectors(features_array[i], features_array[j])
        angles.append(angle)

# 计算夹角的均值和中位数
mean_angle = np.mean(angles)
median_angle = np.median(angles)

# 输出夹角的均值和中位数
print(f"夹角的均值: {mean_angle} 度")
print(f"夹角的中位数: {median_angle} 度")


# 计算特征向量两两之间的余弦相似度
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

num_features = features_array.shape[0]
cosine_similarities = []

for i in range(num_features):
    for j in range(i + 1, num_features):
        cos_sim = cosine_similarity(features_array[i], features_array[j])
        cosine_similarities.append(cos_sim)

# 计算余弦相似度的均值和中位数
mean_cos_sim = np.mean(cosine_similarities)
median_cos_sim = np.median(cosine_similarities)

# 输出余弦相似度的均值和中位数
print(f"余弦相似度的均值: {mean_cos_sim}")
print(f"余弦相似度的中位数: {median_cos_sim}")

# 计算欧式距离
def euclidean_distance(vec1, vec2):
    return np.linalg.norm(vec1 - vec2)

num_features = features_array.shape[0]
euclidean_distances = []

for i in range(num_features):
    for j in range(i + 1, num_features):
        distance = euclidean_distance(features_array[i], features_array[j])
        euclidean_distances.append(distance)

# 计算欧式距离的均值和中位数
mean_euclidean_distance = np.mean(euclidean_distances)
median_euclidean_distance = np.median(euclidean_distances)

# 输出欧式距离的均值和中位数
print(f"欧式距离的均值: {mean_euclidean_distance}")
print(f"欧式距离的中位数: {median_euclidean_distance}")