from ultralytics import YOLO

# 加载预训练的YOLOv5模型
model = YOLO('yolov5s.pt')

# 定义一个函数来检测图像中的物体
def detect_objects(image_path):
    # 使用模型进行预测
    results = model(image_path)
    
    # 解析结果
    for result in results:
        boxes = result.boxes  # 所有边界框
        for box in boxes:
            r = box.xyxy[0].tolist()  # 边界框坐标
            cls = int(box.cls[0])  # 类别索引
            conf = box.conf[0]  # 置信度
            print(f"检测到物体: {model.names[cls]}, 置信度: {conf:.2f}, 坐标: {r}")

# 使用示例
image_path = '昆虫7.jpg'
detect_objects(image_path)