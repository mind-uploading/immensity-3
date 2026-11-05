# -*- coding: utf-8 -*-
from PCV.tools import imtools, pca
from PIL import Image, ImageDraw
from pylab import *
from scipy.cluster.vq import *

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

image_paths = get_image_paths(foldername5)+get_image_paths(foldername6)

imlist = image_paths
#imtools.get_imlist('F:\\Anaconda\\chapter6\\picture\\data\\fontimages\\a_thumbs')
imnbr = len(imlist)
 
# Load images, run PCA.
immatrix = array([array(Image.open(im)).flatten() for im in imlist], 'f')
V, S, immean = pca.pca(immatrix)
 
# Project on 2 PCs.
projected = array([dot(V[[0, 1]], immatrix[i] - immean) for i in range(imnbr)])
 
n = len(projected)
# 计算距离矩阵
S = array([[sqrt(sum((projected[i] - projected[j]) ** 2))
            for i in range(n)] for j in range(n)], 'f')
# 创建拉普拉斯矩阵
rowsum = sum(S, axis=0)
D = diag(1 / sqrt(rowsum))
I = identity(n)
L = I - dot(D, dot(S, D))
# 计算矩阵 L 的特征向量
U, sigma, V = linalg.svd(L)
k = 5
# 从矩阵 L 的前k个特征向量（eigenvector）中创建特征向量（feature vector） # 叠加特征向量作为数组的列
features = array(V[:k]).T
# k-means 聚类 
features = whiten(features)
centroids, distortion = kmeans(features, k)
code, distance = vq(features, centroids)
# 绘制聚类簇
for c in range(k):
    ind = where(code == c)[0]
    figure()
    gray()
    for i in range(minimum(len(ind), 39)):
        im = Image.open(imlist[ind[i]])
        subplot(4, 10, i + 1)
        imshow(array(im))
        axis('equal')
        axis('off')
show()