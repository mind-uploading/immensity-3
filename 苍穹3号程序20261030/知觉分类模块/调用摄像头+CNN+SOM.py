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
base_model = load_model('CNN/vgg16_base_model.h5')
with open('SOM/SOM1.p', 'rb') as infile:
    som = pickle.load(infile)

'''
# 如果是调用笔记本自带的摄像头，参数就为0；如果是外置USB摄像头，参数就为1。
cap = cv2.VideoCapture(0)
# 设置一下摄像头窗口的宽高，参数3代表宽度
cap.set(3, 128)
# 参数4代表的高度
cap.set(4, 128)
# 参数10代表亮度
cap.set(10, 100)

while True:
    success, img = cap.read()
    frame = cv2.flip(img, 1)
    # show a frame
    cv2.imshow('frame', frame)
    # 调整拍摄角度，确认后按‘q’键退出后，释放摄像头资源
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # 设置拍摄图像的保存路径，不设置默认为当前目录
        cv2.imwrite("test.png", frame)
        break

cap.release()
cv2.destroyAllWindows()

# 准备图像数据
img_resized = cv2.resize(cv2.imread("test.png"), (128, 128))  # 调整图像尺寸为 (128, 128)
img_array = np.array(img_resized)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)

# 提取特征
features = base_model.predict(img_array)
features = features.flatten()  # 展平特征向量
print("Features :", features)
data = np.array(features)  # 将特征转换为 numpy 数组


# 设置SOM参数
som_shape = (1, 10)  # SOM网格的大小
som = MiniSom(som_shape[0], som_shape[1], features.shape[-1], sigma=1.0, learning_rate=0.5)

# 初始化SOM
som.random_weights_init(features.reshape(1, -1))
'''

while True:
    # 如果是调用笔记本自带的摄像头，参数就为0；如果是外置USB摄像头，参数就为1。
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    # 设置一下摄像头窗口的宽高，参数3代表宽度
    cap.set(3, 128)
    # 参数4代表的高度
    cap.set(4, 128)
    # 参数10代表亮度
    cap.set(10, 100)

    while True:
        success=False
        while success == False:
            success, img = cap.read()
        frame = cv2.flip(img, 1)
        # show a frame
        cv2.imshow('frame', frame)
        # 调整拍摄角度，确认后按‘q’键退出后，释放摄像头资源
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # 设置拍摄图像的保存路径，不设置默认为当前目录
            cv2.imwrite("test.png", frame)
            break

    #cap.release()
    #cv2.destroyAllWindows()

    # 准备图像数据
    img_resized = cv2.resize(cv2.imread("test.png"), (128, 128))  # 调整图像尺寸为 (128, 128)
    img_array = np.array(img_resized)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # 提取特征
    features = base_model.predict(img_array)
    features = features.flatten()  # 展平特征向量
    print("Features :", features)
    data = np.array(features)  # 将特征转换为 numpy 数组

    

    # 更新 SOM
    som.train_random(features.reshape(1, -1), num_iteration=1000)

    # 获取获胜神经元
    winning_neurons = [som.winner(features)]  # 注意这里传入的是 features 而不是 data
    som_shape = (1, 10)  # SOM网格的大小
    winning_neurons_indices = [(w[0] * som_shape[1] + w[1]) for w in winning_neurons]

    # 输出获胜神经元序号
    dic = {}
    for i, neuron in enumerate(winning_neurons_indices):
        if neuron not in dic:
            dic[neuron] = 1
        else:
            dic[neuron] += 1
        print(f"Image activates neuron index: {neuron}")
    print(dic)

    # 可视化聚类结果
    plt.figure(figsize=(10, 10))
    plt.pcolor(som.distance_map().T, cmap='bone_r')  # 绘制距离图
    plt.colorbar()

    # 在图中标记数据点
    markers = ['o', 's', 'D']
    colors = ['C0', 'C1', 'C2']
    for cnt, xx in enumerate([features]):
        w = som.winner(xx.flatten())  # 获取获胜神经元
        plt.plot(w[0] + .5, w[1] + .5, markers[cnt % 3], markerfacecolor='None',
                markeredgecolor=colors[cnt % 3], markersize=12, markeredgewidth=2)

    plt.title('SOM Clustering')
    plt.show()

    with open('som.p', 'wb') as outfile:
        pickle.dump(som, outfile)

