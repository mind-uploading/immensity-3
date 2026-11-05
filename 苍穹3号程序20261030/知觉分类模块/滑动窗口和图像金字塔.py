import cv2
import numpy as np
import time

def create_image_pyramid(image, num_levels):
    pyramid = [image]
    for i in range(1, num_levels):
        new_size = (int(image.shape[1] / (2 ** i)), int(image.shape[0] / (2 ** i)))
        resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
        pyramid.append(resized_image)
    return pyramid

def sliding_window(image, window_size, step_size):
    for y in range(0, image.shape[0] - window_size[1], step_size):
        for x in range(0, image.shape[1] - window_size[0], step_size):
            yield (x, y, image[y:y + window_size[1], x:x + window_size[0]])

def sample_image_pyramid(image_path, num_levels, window_size, step_size):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("图像未找到或无法加载。")
    
    original_center = (image.shape[1] // 2, image.shape[0] // 2)
    results = []

    pyramid = create_image_pyramid(image, num_levels)
    for level, img in enumerate(pyramid):
        scale_factor = 2 ** level
        pyramid_center = (img.shape[1] // 2, img.shape[0] // 2)
        for (x, y, window) in sliding_window(img, window_size, step_size):
            window_center = (x + window_size[0] // 2, y + window_size[1] // 2)
            center_offset = (window_center[0] - pyramid_center[0], window_center[1] - pyramid_center[1])
            width_ratio = round(center_offset[0] / img.shape[1],1)
            height_ratio = round(center_offset[1] / img.shape[0],1)
            results.append({
                'level': level,
                'window_center': window_center,
                'center_offset': center_offset,
                'width_ratio': width_ratio,
                'height_ratio': height_ratio
            })

            # 绘制窗口
            cv2.rectangle(img, (x, y), (x + window_size[0], y + window_size[1]), (0, 255, 0), 2)
            # 绘制窗口中心
            cv2.circle(img, window_center, 5, (0, 0, 255), -1)
            # 标注窗口中心位置
            text = f"({window_center[0]}, {window_center[1]})"
            cv2.putText(img, text, (window_center[0] + 10, window_center[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            # 标注相对位置比例
            ratio_text = f"({width_ratio:.2f}, {height_ratio:.2f})"
            cv2.putText(img, ratio_text, (window_center[0] + 10, window_center[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            
    return results, pyramid


# 使用示例
image_path = 'pic.png'
num_levels = 3  # 金字塔层数
window_size = (128, 128)  # 窗口大小
step_size = 128  # 步长

samples, pyramid = sample_image_pyramid(image_path, num_levels, window_size, step_size)

# 显示每一层金字塔的结果
for level, img in enumerate(pyramid):
    cv2.imshow(f'Level {level}', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


for sample in samples:
    print(f"层级: {sample['level']}, "
          f"窗口中心: {sample['window_center']}, "
          f"中心偏移: {sample['center_offset']}, "
          f"宽度比例: {sample['width_ratio']:.4f}, "
          f"高度比例: {sample['height_ratio']:.4f}")