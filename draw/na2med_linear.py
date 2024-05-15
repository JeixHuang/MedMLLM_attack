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
    ax.text(mid_x, mid_y, f'Offset: {offset:.2f}', fontsize=16, color='black', ha='center', va='center')
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 50)
    # ax.set_xlabel('Origin Score')
    # ax.set_ylabel('Unmatch Score')
    # ax.set_title('Scatter Plot with Highlighted Bias Line')
    ax.grid(True)


def add_circles(ax, folder_path):
    print("Processing folder:", folder_path)
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    all_data = {}
    color_count = len(csv_files)
    colors = plt.cm.rainbow(np.linspace(0, 1, color_count))[::-1]

    # 初始化列表来存储所有数据点
    all_origins = []
    all_unmatches = []

    for i, csv_file in enumerate(csv_files):
        df = pd.read_csv(csv_file)
        if 'origin_score' in df.columns and 'unmatch_score' in df.columns:
            file_name = os.path.basename(csv_file).replace('.csv', '')
            origins = df['origin_score'].values
            unmatches = df['unmatch_score'].values
            all_data[file_name] = {
                'origin_scores': origins,
                'unmatch_scores': unmatches,
                'color': colors[i]
            }
            
            # 加入全局数据列表
            all_origins.extend(origins)
            all_unmatches.extend(unmatches)

    if not all_data:
        raise ValueError("No valid data found in any CSV files.")

    # 计算全局中心
    overall_origin_mean = np.mean(all_origins)
    overall_unmatch_mean = np.mean(all_unmatches)
    overall_center = (overall_origin_mean, overall_unmatch_mean)
    print("Overall Center:", overall_center)

    for file_name, data in all_data.items():
        origin_mean = np.mean(data['origin_scores'])
        unmatch_mean = np.mean(data['unmatch_scores'])
        center = (origin_mean, unmatch_mean)

        x_distances = np.abs(data['origin_scores'] - origin_mean)
        x_radius = np.mean(x_distances)
        y_distances = np.abs(data['unmatch_scores'] - unmatch_mean)
        y_radius = np.mean(y_distances)

        ellipse = patches.Ellipse(center, 2 * x_radius, 2 * y_radius, color=data['color'], alpha=0.2, fill=True)
        ax.add_patch(ellipse)

    # 在图上标记整体平均中心
    ax.scatter(*overall_center, color='red', label='Overall Center')
    ax.text(*overall_center, 'Overall Center', fontsize=12, color='red', ha='center')

    ax.set_xlim(0, 50)
    ax.set_ylim(0, 50)
    ax.legend()
    
def print_scores(folder_path):
    # Reuse the CSV reading part from plot_scatter_with_bias
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    all_origin_scores = []
    all_unmatch_scores = []

    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        if 'origin_score' in df.columns and 'unmatch_score' in df.columns:
            all_origin_scores.extend(df['origin_score'].tolist())
            all_unmatch_scores.extend(df['unmatch_score'].tolist())

    if not all_origin_scores or not all_unmatch_scores:
        print("No valid scores found in CSV files.")
        return

    # Calculate the averages
    avg_origin_score = np.mean(all_origin_scores)
    avg_unmatch_score = np.mean(all_unmatch_scores)

    # Print the averages
    print(f"Average Original Score: {avg_origin_score:.2f}")
    print(f"Average Unmatch Score: {avg_unmatch_score:.2f}")
    
# 使用示例
fig, ax = plt.subplots(figsize=(10, 10))
plot_scatter_with_bias(ax, '../metric/na2med_img2text_results')
plt.show()
