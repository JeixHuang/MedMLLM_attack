import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches 

def perpendicular_distance(x, y):
    return abs(y - x) / np.sqrt(2)

def plot_scatter_with_bias(ax, folder_path):
    # Get all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    all_data = {}
    color_count = len(csv_files)
    colors = plt.cm.rainbow(np.linspace(0, 1, color_count))[::-1]  # Reverse to start from red

    for i, csv_file in enumerate(csv_files):
        df = pd.read_csv(csv_file)
        if 'origin_score' in df.columns and 'unmatch_score' in df.columns:
            file_name = os.path.basename(csv_file).replace('.csv', '')
            all_data[file_name] = {
                'origin_scores': df['origin_score'].values,
                'unmatch_scores': df['unmatch_score'].values,
                'color': colors[i]
            }

    if not all_data:
        raise ValueError("No valid data found in any CSV files.")

    global_origin_scores = []
    global_unmatch_scores = []
    for file_name, data in all_data.items():
        global_origin_scores.extend(data['origin_scores'])
        global_unmatch_scores.extend(data['unmatch_scores'])
        ax.scatter(data['origin_scores'], data['unmatch_scores'], color=data['color'], alpha=0.6, label=file_name)

    global_origin_scores = np.array(global_origin_scores)
    global_unmatch_scores = np.array(global_unmatch_scores)
    distances = perpendicular_distance(global_origin_scores, global_unmatch_scores)
    average_distance = np.mean(distances)
    x_values = np.linspace(min(global_origin_scores.min(), global_unmatch_scores.min()), max(global_origin_scores.max(), global_unmatch_scores.max()), 100)
    
    x_all = np.linspace(0, 50, 100)  # Modified to be from 0 to 50
    y_line = x_all  # y = x line
    offset = average_distance * np.sqrt(2)
    y_line_offset = y_line + offset  # Offset line
    ax.plot(x_all, y_line, 'r--', label='y=x Line')
    ax.plot(x_all, y_line_offset, 'g--', label=f'Bias Line (Offset by {offset:.2f})')
    
    # ax.plot(x_values, x_values, 'r--', label='y=x Line')
    
    # ax.plot(x_values, x_values + offset, 'g--', label=f'Bias Line (Offset by {offset:.2f})')
    ax.text(x_values[-1], x_values[-1] + offset, '', fontsize=12, color='green', ha='left', va='bottom')
    ax.fill_between(x_all, x_all, x_all + offset, color='grey', alpha=0.2, label='Impact Region')
    # 标记偏移值
    mid_x = 10  # 在x=25的位置标记，位于两条线中间的位置
    mid_y = 35 + offset / 2  # 中间点的y值
    ax.text(mid_x, mid_y, f'Offset: {offset:.2f}', fontsize=12, color='black', ha='center', va='center')
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 50)
    # ax.set_xlabel('Origin Score')
    # ax.set_ylabel('Unmatch Score')
    # ax.set_title('Scatter Plot with Highlighted Bias Line')
    ax.grid(True)


def add_circles(ax, folder_path):
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    all_data = {}
    color_count = len(csv_files)
    colors = plt.cm.rainbow(np.linspace(0, 1, color_count))[::-1]

    for i, csv_file in enumerate(csv_files):
        df = pd.read_csv(csv_file)
        if 'origin_score' in df.columns and 'unmatch_score' in df.columns:
            file_name = os.path.basename(csv_file).replace('.csv', '')
            all_data[file_name] = {
                'origin_scores': df['origin_score'].values,
                'unmatch_scores': df['unmatch_score'].values,
                'color': colors[i]
            }

    if not all_data:
        raise ValueError("No valid data found in any CSV files.")
    for file_name, data in all_data.items():
        origin_mean = np.mean(data['origin_scores'])
        unmatch_mean = np.mean(data['unmatch_scores'])
        center = (origin_mean, unmatch_mean)
        # 计算 x 坐标到 x 坐标均值的平均距离
        x_distances = np.abs(data['origin_scores'] - origin_mean)
        x_radius = np.mean(x_distances)

        # 计算 y 坐标到 y 坐标均值的平均距离
        y_distances = np.abs(data['unmatch_scores'] - unmatch_mean)
        y_radius = np.mean(y_distances)

        # 绘制椭圆
        ellipse = patches.Ellipse(center, 2 * x_radius, 2 * y_radius, color=data['color'], alpha=0.2, fill=True)
        ax.add_patch(ellipse)
        # ax.text(*center, f'{file_name}', fontsize=12, color='black', ha='center')

    ax.set_xlim(0, 50)
    ax.set_ylim(0, 50)
    # ax.set_xlabel('Origin Score')
    # ax.set_ylabel('Unmatch Score')
    # ax.set_title('Scatter Plot with Highlighted Circles')
    
# 使用示例
fig, ax = plt.subplots(figsize=(10, 10))
plot_scatter_with_bias(ax, '../metric/na2med_img2text_results')
plt.show()
