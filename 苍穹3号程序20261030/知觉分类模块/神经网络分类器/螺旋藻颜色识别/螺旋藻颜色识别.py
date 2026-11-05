'''
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import os

def resize_images(directory, size):
    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                img_path = os.path.join(folder_path, filename)
                with Image.open(img_path) as img:
                    img_resized = img.resize(size)
                    img_resized.save(img_path)

# 调整训练集图像大小
resize_images('lxz_dataset/train', (150, 150))

# 调整验证集图像大小
resize_images('lxz_dataset/validation', (150, 150))

# 调整测试集图像大小
resize_images('lxz_dataset/test', (150, 150))
# 数据增强
train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=40,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   fill_mode='nearest')

test_datagen = ImageDataGenerator(rescale=1./255)

# 训练数据和验证数据加载
train_generator = train_datagen.flow_from_directory(
        'lxz_dataset/train',  # 这里替换为你的训练数据路径
        target_size=(150, 150),
        batch_size=32,
        class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
        'lxz_dataset/validation',  # 这里替换为你的验证数据路径
        target_size=(150, 150),
        batch_size=32,
        class_mode='categorical')
#定义模型
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(train_generator.num_classes, activation='softmax')  # 输出层大小取决于类别数量
])
#编译模型
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
#训练模型
history = model.fit(
      train_generator,
      steps_per_epoch=train_generator.samples // train_generator.batch_size,
      epochs=30,
      validation_data=validation_generator,
      validation_steps=validation_generator.samples // validation_generator.batch_size)
# 保存整个模型
model.save('lxz_color_classifier.h5')
'''




#应用模型
from tensorflow.keras.models import load_model

# 加载整个模型
loaded_model = load_model('lxz_color_classifier.h5')
# 预处理输入数据
from PIL import Image
import numpy as np

def preprocess_image(image_path, target_size=(150, 150)):
    # 读取图像
    img = Image.open(image_path)
    
    # 调整图像大小
    img = img.resize(target_size)
    
    # 转换为 NumPy 数组
    img_array = np.array(img)
    
    # 归一化
    img_array = img_array / 255.0
    
    # 扩展维度以匹配模型输入
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array



class_names=['绿色','黄色']
# 示例1
image_path = 'lxz_dataset/test/黄色/黄色.jpg'
preprocessed_image = preprocess_image(image_path)
# 进行预测
predictions = loaded_model.predict(preprocessed_image)

# 获取预测结果
predicted_class_index = np.argmax(predictions)
predicted_probability = predictions[0][predicted_class_index]


# 获取类别名称
predicted_class_name = class_names[predicted_class_index]

print(f"预测类别: {predicted_class_name}")
print(f"预测概率: {predicted_probability}")
print(f"预测类别索引: {predicted_class_index}")
print(f"预测概率: {predicted_probability}")

# 示例2
image_path = 'lxz_dataset/test/绿色/绿色.jpg'
preprocessed_image = preprocess_image(image_path)
# 进行预测
predictions = loaded_model.predict(preprocessed_image)

# 获取预测结果
predicted_class_index = np.argmax(predictions)
predicted_probability = predictions[0][predicted_class_index]

# 获取类别名称
predicted_class_name = class_names[predicted_class_index]

print(f"预测类别: {predicted_class_name}")
print(f"预测概率: {predicted_probability}")
print(f"预测类别索引: {predicted_class_index}")
print(f"预测概率: {predicted_probability}")

# 示例3
image_path = 'lxz_dataset/test/绿色/绿色2.jpg'
preprocessed_image = preprocess_image(image_path)
# 进行预测
predictions = loaded_model.predict(preprocessed_image)

# 获取预测结果
predicted_class_index = np.argmax(predictions)
predicted_probability = predictions[0][predicted_class_index]

# 获取类别名称
predicted_class_name = class_names[predicted_class_index]

print(f"预测类别: {predicted_class_name}")
print(f"预测概率: {predicted_probability}")
print(f"预测类别索引: {predicted_class_index}")
print(f"预测概率: {predicted_probability}")

# 示例4
image_path = 'lxz_dataset/test/黄色/黄色2.jpg'
preprocessed_image = preprocess_image(image_path)
# 进行预测
predictions = loaded_model.predict(preprocessed_image)

# 获取预测结果
predicted_class_index = np.argmax(predictions)
predicted_probability = predictions[0][predicted_class_index]

# 获取类别名称
predicted_class_name = class_names[predicted_class_index]

print(f"预测类别: {predicted_class_name}")
print(f"预测概率: {predicted_probability}")
print(f"预测类别索引: {predicted_class_index}")
print(f"预测概率: {predicted_probability}")