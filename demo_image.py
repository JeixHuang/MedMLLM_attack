import os

def count_images_in_directory(directory):
    """
    Recursively count image files in the directory and its subdirectories.
    """
    image_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg','JPG','PNG')):
                image_count += 1
    return image_count

def main():
    # 设置主文件夹路径
    main_directory = 'CMIC-111k'  # 请替换为你的文件夹路径

    # 统计主文件夹中的图片数量
    main_folder_count = count_images_in_directory(main_directory)

    # 准备写入统计数据的文本文件
    output_filename = 'image_counts.txt'
    with open(output_filename, 'w') as file:
        file.write(f"Total images in main folder: {main_folder_count}\n")

        # 遍历主文件夹中的每一个子文件夹
        for subdir in os.listdir(main_directory):
            subdir_path = os.path.join(main_directory, subdir)
            if os.path.isdir(subdir_path):
                # 统计子文件夹中的图片数量
                subdir_count = count_images_in_directory(subdir_path)
                file.write(f"Images in {subdir}: {subdir_count}\n")

                # 遍历子文件夹中的每一个子子文件夹
                for subsubdir in os.listdir(subdir_path):
                    subsubdir_path = os.path.join(subdir_path, subsubdir)
                    if os.path.isdir(subsubdir_path):
                        # 统计子子文件夹中的图片数量
                        subsubdir_count = count_images_in_directory(subsubdir_path)
                        file.write(f"Images in {subdir}/{subsubdir}: {subsubdir_count}\n")

    print(f"Statistics written to {output_filename}")

if __name__ == "__main__":
    main()
