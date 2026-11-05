import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import load_model  # 导入 load_model 函数
from PIL import Image
import io
import numpy as np
import pandas as pd
from minisom import MiniSom
import matplotlib.pyplot as plt
import os

# 加载模型
base_model = load_model('CNN/vgg16_base_model.h5')

# 获取文件夹中所有图片路径
def get_image_paths(folder_path):
    image_paths = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg')):
            image_paths.append(os.path.join(folder_path, filename))
    return image_paths

# 准备图像数据
def load_and_preprocess_image(img_path):
    img = Image.open(img_path).resize((128, 128))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

# 提取特征
def extract_features(img_path):
    img_array = load_and_preprocess_image(img_path)
    features = base_model.predict(img_array)
    features = features.flatten()  # 展平特征向量
    return features


# 定义文件夹路径
folder_path = 'd:\\人生目标\\自然层面的解放\\意识上传\\人工心智载体\\人工脑\\意识\\初级意识\\意识引擎\\苍穹系列\\苍穹3号\\苍穹3号程序-备份\\苍穹3号程序\\训练数据\\图片'
# 获取图片路径
image_paths = get_image_paths(folder_path)


# 提取并输出特征
features_list = []
for img_path in image_paths:
    features = extract_features(img_path)
    features_list.append(features)
    print(f"Features for {img_path}: {features}")
data = np.array(features_list)  # 将特征转换为 numpy 数组

# 设置SOM参数
som_shape = (1,10)  # SOM网格的大小
som = MiniSom(som_shape[0], som_shape[1], data.shape[1], sigma=1.0, learning_rate=0.5)

# 初始化SOM
som.random_weights_init(data)

# 更新 SOM
som.train_random(data, num_iteration=1000)

# 获取获胜神经元
winning_neurons = [som.winner(feature) for feature in data]
winning_neurons_indices = [(w[0] * som_shape[1] + w[1]) for w in winning_neurons]

# 输出获胜神经元序号
dic={}
for i, neuron in enumerate(winning_neurons_indices):
    if neuron not in dic: 
        dic[neuron]=1
    else:
        dic[neuron]+=1
    print(f"Image {image_paths[i]} activates neuron index: {neuron}")
print(dic)

# 可视化聚类结果
plt.figure(figsize=(10, 10))
plt.pcolor(som.distance_map().T, cmap='bone_r')  # 绘制距离图
plt.colorbar()

# 在图中标记数据点
markers = ['o', 's', 'D']
colors = ['C0', 'C1', 'C2']
for cnt, xx in enumerate(data):
    w = som.winner(xx)  # 获取获胜神经元
    plt.plot(w[0] + .5, w[1] + .5, markers[cnt % 3], markerfacecolor='None',
             markeredgecolor=colors[cnt % 3], markersize=12, markeredgewidth=2)

plt.title('SOM Clustering')
plt.show()
