import os
import tarfile
import csv
from PIL import Image

# .tar.gz 文件路径和解压缩目标路径
val_tar_path = "data/train_images_1.tar.gz"
val_extract_path = "data/val_images_extracted"
os.makedirs(val_extract_path, exist_ok=True)

# 类别映射文件
from classes import IMAGENET2012_CLASSES

# 新的图像文件夹
img_net_dir = "img_net"
os.makedirs(img_net_dir, exist_ok=True)

# 解压缩 tar.gz 文件
with tarfile.open(val_tar_path, "r:gz") as tar:
    tar.extractall(path=val_extract_path)

# CSV 文件名
csv_filename = "imagenet_val.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["image_path", "label"])

    # 遍历解压缩目录中的每个图像文件
    for root, _, files in os.walk(val_extract_path):
        for file in files:
            if file.endswith(".JPEG"):
                # 提取文件名和 synset_id（假设文件名格式为 `<image>_<synset_id>.JPEG`）
                image_filename = os.path.splitext(file)[0]
                _, synset_id = image_filename.rsplit("_", 1)

                # 获取对应的标签
                label = IMAGENET2012_CLASSES.get(synset_id, None)
                if label is None:
                    continue

                # 新文件名和路径
                new_image_filename = f"{image_filename}.jpg"
                new_image_path = os.path.join(img_net_dir, new_image_filename)

                # 打开 JPEG 图像并保存为 .jpg
                original_image_path = os.path.join(root, file)
                with Image.open(original_image_path) as img:
                    img.convert("RGB").save(new_image_path, "JPEG")

                # 将新路径和标签写入 CSV 文件
                writer.writerow([new_image_path, label])

print(f"CSV 文件 '{csv_filename}' 生成完毕，图像保存在 '{img_net_dir}'。")
