import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

# 指定要读取CSV文件的文件夹路径
folder_path = '../metric/ret_com'  # 修改为您的文件夹路径
output_path = 'plot_ret_distribution'
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

# 创建色彩渐变
color_count = len(data_paths)
colors = plt.cm.rainbow(np.linspace(0, 1, color_count))[::-1]

# 确保输出文件夹存在
os.makedirs(output_path, exist_ok=True)

# 为每个变量绘制图形
for variable in variable_names:
    plt.figure(figsize=(10, 8))
    all_density = []
    for df, color, path in zip(data_frames, colors, data_paths):
        if variable in df.columns:
            x = df[variable].dropna()
            # 归一化处理
            x_normalized = (x - x.min()) / (x.max() - x.min())
            kde = gaussian_kde(x_normalized)
            x_grid = np.linspace(0, 1, 1000)
            density = kde(x_grid)
            plt.fill_between(x_grid, density, alpha=0.7, color=color)  # 增大透明度
            all_density.append(density)
    
    plt.title(f'{variable}')
    # plt.xlabel('Normalized Score')
    plt.ylabel('Proportion(%)')
    plt.legend([os.path.basename(path).split('.')[0] for path in data_paths], loc='upper left')
    plt.grid(True)
    plt.xlim(0, 1)
    plt.ylim(0, max([max(density) for density in all_density]) * 1.2)  # 动态调整Y轴范围
    plt.savefig(os.path.join(output_path, f'{variable}.png'))  # 保存到指定文件夹
    plt.close()
