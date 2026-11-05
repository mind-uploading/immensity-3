import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class SelfOrganizingMap:
    def __init__(self, dimensions, map_size, learning_rate=0.5, radius=1.0):
        self.dimensions = dimensions  # 输入数据维度
        self.map_size = map_size  # 网络大小，例如(10, 10)
        self.learning_rate = learning_rate
        self.radius = radius
        self.weights = np.random.rand(map_size[0], map_size[1], dimensions)

    def _find_bmu(self, sample):
        """ 找到最佳匹配单元 """
        bmu_index = None
        min_distance = float('inf')
        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                distance = np.linalg.norm(sample - self.weights[i, j])
                if distance < min_distance:
                    min_distance = distance
                    bmu_index = (i, j)
        return bmu_index

    def train(self, data, epochs):
        """ 训练SOM """
        for epoch in range(epochs):
            for sample in data:
                bmu_index = self._find_bmu(sample)
                for i in range(self.map_size[0]):
                    for j in range(self.map_size[1]):
                        if np.linalg.norm(np.array(bmu_index) - np.array([i, j])) <= self.radius:
                            self.weights[i, j] += self.learning_rate * (sample - self.weights[i, j])

    def get_bmu_indices(self, data):
        """ 获取每个样本的最佳匹配单元索引 """
        bmu_indices = []
        for sample in data:
            bmu_index = self._find_bmu(sample)
            bmu_indices.append(bmu_index)
        return bmu_indices

def load_image_pixels(image_path, new_size):
    """ 加载图像并提取像素值，同时调整图像大小 """
    image = Image.open(image_path).convert('RGB')
    image = image.resize(new_size)  # 调整图像大小
    pixels = np.array(image)
    return pixels

def visualize_som(bmu_indices, pixels):
    """ 可视化 SOM 聚类结果 """
    height, width, _ = pixels.shape
    
    # 检查像素数量与 BMU 索引数量是否匹配
    if len(bmu_indices) != height * width:
        raise ValueError(f"像素数量 ({height * width}) 与 BMU 索引数量 ({len(bmu_indices)}) 不匹配")
    
    # 将每个像素映射到其对应的 BMU
    bmu_grid = np.zeros((height, width, 2), dtype=int)
    index = 0
    for i in range(height):
        for j in range(width):
            bmu_grid[i, j] = bmu_indices[index]
            index += 1
    
    # 绘制 SOM 权重分布
    plt.figure(figsize=(10, 8))
    plt.imshow(pixels)
    
    # 在图像上绘制 BMU 索引
    for i in range(height):
        for j in range(width):
            plt.text(j, i, f"{bmu_grid[i, j]}", color='white', fontsize=6, ha='center', va='center')
    
    plt.title("SOM Visualization")
    plt.axis('off')
    plt.show()

# 读取图像并提取像素值
image_path = '花朵.jpg'
new_size = (100, 100)  # 设置新的图像大小
pixels = load_image_pixels(image_path, new_size)

# 创建并训练 SOM
som = SelfOrganizingMap(dimensions=3, map_size=(5, 5))
som.train(pixels.reshape(-1, 3), epochs=3)  # 将像素数据重塑为二维数组

# 获取每个像素的最佳匹配单元索引
bmu_indices = som.get_bmu_indices(pixels.reshape(-1, 3))

# 可视化结果
visualize_som(bmu_indices, pixels)