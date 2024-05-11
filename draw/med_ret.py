import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# 指定要读取CSV文件的文件夹路径
folder_path = '../metric/ret_com'  # 请替换为你的文件夹路径
output_path='plot_ret'
data_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

# 定义变量名
variable_names = [
    'text_sim_score_malicious', 
    'text_sim_score_unmatch', 
    'image_text_sim_score_malicious_nature', 
    'image_text_sim_score_unmatch_nature', 
    'image_text_sim_score_malicious_bio', 
    'image_text_sim_score_unmatch_nature_bio'
]

# 读取CSV文件
data_frames = [pd.read_csv(path) for path in data_paths]

# Create a color gradient from red to violet
color_count = len(data_paths)
colors = plt.cm.rainbow(np.linspace(0, 1, color_count))[::-1]  # Reverse to start from red
# 创建并保存图表
os.makedirs(output_path, exist_ok=True)  # 确保文件夹存在

for variable in variable_names:
    plt.figure(figsize=(10,8))
    for df, color, path in zip(data_frames, colors, data_paths):
        plt.scatter(df['id'], df[variable], color=color, alpha=0.5, label=f'Data from {os.path.basename(path)}')
    plt.title(f'Distribution of {variable} across different CSV files')
    plt.xlabel('ID')
    plt.ylabel('Score')
    plt.legend()
    plt.savefig(os.path.join(output_path, f'{variable}.png'))  # 保存文件到文件夹
    plt.close()
