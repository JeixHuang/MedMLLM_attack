import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def perpendicular_distance(x, y):
    return abs(y - x) / np.sqrt(2)

def plot_labeled_scatter(ax, folder_path):
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    all_data = {}
    print("Found CSV files:", len(csv_files))

    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        if 'origin_score' in df.columns and 'unmatch_score' in df.columns and 'label_original' in df.columns:
            file_name = os.path.basename(csv_file).replace('.csv', '')
            all_data[file_name] = df[['origin_score', 'unmatch_score', 'label_original']]
    
    combined_data = pd.concat(all_data.values())
    print("Total data points to plot:", combined_data.shape[0])

    unique_labels = combined_data['label_original'].unique()
    color_count = len(unique_labels)
    colors = plt.cm.rainbow(np.linspace(0, 1, color_count))[::-1]
    label_to_color = {label: colors[i] for i, label in enumerate(unique_labels)}

    global_origin_scores = np.array(combined_data['origin_score'])
    global_unmatch_scores = np.array(combined_data['unmatch_score'])

    distances = perpendicular_distance(global_origin_scores, global_unmatch_scores)
    average_distance = np.mean(distances)

    for label, color in label_to_color.items():
        label_data = combined_data[combined_data['label_original'] == label]
        ax.scatter(label_data['origin_score'], label_data['unmatch_score'], color=color, alpha=0.6, label=label)

    x_values = np.linspace(0, 50, 100)
    ax.plot(x_values, x_values, 'r--', label='y=x Line')
    offset = average_distance * np.sqrt(2)
    ax.plot(x_values, x_values + offset, 'g--', label=f'Bias Line (Offset by {offset:.2f})')
    # ax.text(x_values[-1], x_values[-1] + offset, f'Offset: {offset:.2f}', fontsize=12, color='black', ha='left', va='bottom')
    ax.fill_between(x_values, x_values, x_values + offset, color='grey', alpha=0.2, label='Impact Region')
    mid_x = 10  # 在x=25的位置标记，位于两条线中间的位置
    mid_y = 35 + offset / 2  # 中间点的y值
    ax.text(mid_x, mid_y, f'Offset: {offset:.2f}', fontsize=12, color='black', ha='center', va='center')
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 50)
    # ax.set_xlabel('Origin Score')
    # ax.set_ylabel('Unmatch Score')
    # ax.set_title('Scatter Plot by Label Original')
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
        variance = np.var(perpendicular_distance(data['origin_scores'], data['unmatch_scores']))

        # Draw circle with center at the means and radius as sqrt(variance)
        circle = plt.Circle(center, np.sqrt(variance), color=data['color'],alpha=0.2, fill=True, linewidth=2)
        ax.add_patch(circle)
        ax.text(*center, f'{file_name}', fontsize=12, color='black', ha='center')

    ax.set_xlim(0, 50)
    ax.set_ylim(0, 50)
    # ax.set_xlabel('Origin Score')
    # ax.set_ylabel('Unmatch Score')
    # ax.set_title('Scatter Plot with Highlighted Circles')
    
    
# 使用示例
fig, ax = plt.subplots(figsize=(10, 10))
plot_labeled_scatter(ax, '../metric/metric/na2na_nature_img2text')
plt.show()
