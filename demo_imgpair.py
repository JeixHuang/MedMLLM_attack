import os
import csv
import random
from glob import glob

# 设定数据的根目录
root_dir = "CMIC-111k"

# 定义一个函数来替换文件路径中的特定字符
def replace_special_chars(original_path):
    new_path = original_path.replace(" ", "_").replace("(", "_").replace(")", "_")
    if original_path != new_path:
        os.rename(original_path, new_path)
    return new_path

# 创建一个CSV文件并写入标题行
with open('3MAD-70K.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'file_name', 'original_attribute','unmatch_attribute', 'normal_prompt','harmful_prompt', 'policy', 'key_phrases'])

    id_counter = 0  # 初始化id计数器

    # 遍历每一个介质的文件夹
    for media in os.listdir(root_dir):
        media_path = os.path.join(root_dir, media)
        media_path = replace_special_chars(media_path)

        # 确保当前路径是文件夹
        if os.path.isdir(media_path):
            # 遍历每一个部位的文件夹
            for part in os.listdir(media_path):
                part_path = os.path.join(media_path, part)
                part_path = replace_special_chars(part_path)

                if os.path.isdir(part_path):
                    # 获取所有图片
                    images = glob(os.path.join(part_path, '*.jpg')) + glob(os.path.join(part_path, '*.png'))
                    images = [replace_special_chars(img) for img in images]
                    
                    # 随机选择图片，数量为部位内图片总数或最大1000张
                    selected_images = random.sample(images, min(len(images),12000))
                    
                    # 对于每张图片，写入两行
                    for img in selected_images:
                        attributes = f"{os.path.basename(media_path)} and {os.path.basename(part_path)}"
                        
                        # 第一行，attack_category为unmatch
                        writer.writerow([id_counter, img,attributes, attributes, '', '', '',''])
                        id_counter += 1
                        


print("CSV文件已生成。")
