import requests
from bs4 import BeautifulSoup
import os
import time

def download_images_from_baidu(keyword, save_dir='./images', num_images=10):
    # 创建保存图片的文件夹
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 百度图片搜索URL
    search_url = "https://image.baidu.com/search/index"
    params = {
        'tn': 'baiduimage',
        'word': keyword,
        'pn': 0,
        'rn': num_images
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(search_url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')[:num_images]

    downloaded_count = 0
    for i, img_tag in enumerate(img_tags):
        try:
            # 尝试从多个属性获取图片链接
            img_url = img_tag.get('data-src') or img_tag.get('src')
            if img_url:
                img_data = requests.get(img_url, headers=headers).content
                with open(os.path.join(save_dir, f'{keyword}_{i+1}.jpg'), 'wb') as handler:
                    handler.write(img_data)
                print(f"Downloaded image {i+1}: {img_url}")
                downloaded_count += 1
                # 防止触发反爬虫机制，增加延时
                time.sleep(1)
            else:
                print(f"No valid URL found for image {i+1}")
        except Exception as e:
            print(f"Failed to download image {i+1}: {e}")

    print(f"Total downloaded images: {downloaded_count} out of {num_images}")

# 指定保存路径
save_directory = r'D:\人生目标\自然层面的解放\意识上传\人工心智载体\人工脑\意识\初级意识\意识引擎\苍穹系列\苍穹3号\苍穹3号程序-备份\苍穹3号程序\训练数据\图片'

# 调用函数并传入关键词以及想要下载的图片数量
download_images_from_baidu('真实场景', save_directory, 5)