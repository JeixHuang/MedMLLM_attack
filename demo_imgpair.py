import os
import csv
import random
from glob import glob

# 设定数据的根目录
root_dir = "MedMQ-2k"

# 创建一个CSV文件并写入标题行
with open('data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'attack_category', 'img', 'attributes', 'prompts', 'policy', 'key_phrases'])

    id_counter = 0  # 初始化id计数器

    # 遍历每一个介质的文件夹
    for media in os.listdir(root_dir):
        media_path = os.path.join(root_dir, media)

        # 确保当前路径是文件夹
        if os.path.isdir(media_path):
            # 遍历每一个部位的文件夹
            for part in os.listdir(media_path):
                part_path = os.path.join(media_path, part)
                
                if os.path.isdir(part_path):
                    # 获取所有图片
                    images = glob(os.path.join(part_path, '*.jpg')) + glob(os.path.join(part_path, '*.png'))
                    
                    # 随机选择图片，数量为部位内图片总数或最大1000张
                    selected_images = random.sample(images, min(len(images), 1000))
                    
                    # 对于每张图片，写入两行
                    for img in selected_images:
                        attributes = f"{media} and {part}"
                        
                        # 第一行，attack_category为unmatch
                        writer.writerow([id_counter, 'unmatch', img, attributes, '', '', ''])
                        id_counter += 1
                        
                        # 第二行，attack_category为malicious
                        writer.writerow([id_counter, 'malicious', img, attributes, '', '', ''])
                        id_counter += 1

print("CSV文件已生成。")