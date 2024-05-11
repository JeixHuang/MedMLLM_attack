import os
import shutil

def collect_and_rename_images(source_dir, target_dir):
    # 确保目标目录存在
    os.makedirs(target_dir, exist_ok=True)

    # 支持的图片格式
    extensions = ('.png', '.jpg', '.jpeg')
    # 初始化文件编号
    file_number = 1

    # 遍历源目录及其所有子目录
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(extensions):
                # 构造原始文件完整路径
                full_file_path = os.path.join(root, file)
                
                # 如果是JPEG文件，将后缀改为.jpg
                if file.lower().endswith('.JPEG'):
                    new_file_name = f'{file_number:04d}.jpg'
                else:
                    new_file_name = f'{file_number:04d}' + os.path.splitext(file)[1]

                new_file_path = os.path.join(target_dir, new_file_name)
                # 复制文件
                shutil.copy(full_file_path, new_file_path)
                # 更新文件编号
                file_number += 1

    print(f'共复制并重新编号了 {file_number - 1} 张图片。')

# 使用示例
source_directory = '/home/huangxijie/MedMLLM_attack/imagenet-1k/data/text'  # 设置源目录路径
target_directory = '/home/huangxijie/MedMLLM_attack/imagenet-1k/data/image'  # 设置目标目录路径
collect_and_rename_images(source_directory, target_directory)
