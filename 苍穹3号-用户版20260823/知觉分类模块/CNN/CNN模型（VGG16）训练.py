import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import os

# 加载预训练的VGG16模型，不包括顶层
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
base_model.save('vgg16_base_model.h5')