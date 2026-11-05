
import tensorflow as tf
from PIL import Image
import numpy as np
model = tf.keras.applications.MobileNetV2(weights='imagenet')

def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((224, 224))  # MobileNetV2 expects input size of 224x224
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch
    return tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
def predict_and_decode(image_path):
    preprocessed_img = preprocess_image(image_path)
    predictions = model.predict(preprocessed_img)
    # Decode the top 5 predictions
    return tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=5)[0]
image_path = 'path/to/your/image.jpg'
predictions = predict_and_decode(image_path)

for i, (class_id, label, score) in enumerate(predictions):
    print(f"Prediction {i+1}: {label} ({score:.2f})")