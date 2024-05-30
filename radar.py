import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_radar_chart(ax, title, categories, values, models, r_range=None):
    num_vars = len(categories)
    
    # Compute angle of each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    
    # Set radar chart parameters
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, color='grey', size=15, fontweight='bold')
    
    # Draw y-labels
    ax.set_rlabel_position(0)
    ax.yaxis.set_tick_params(labelsize=12)
    
    if r_range:
        ax.set_ylim(*r_range)
    
    # Plot each model
    for model, model_values in values.items():
        values_cycle = model_values + model_values[:1]
        ax.plot(angles, values_cycle, label=model, linewidth=2, linestyle='solid')
        ax.fill(angles, values_cycle, alpha=0.25)
    
    ax.set_title(title, size=20, color='black', y=1.1)
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1), fontsize=12)

# 获取所有CSV文件的路径
csv_files = glob.glob('ret_blank_asr/processed_ret/*.csv')

# 读取所有CSV文件并存储在字典中
data = {}
for file in csv_files:
    model_name = file.split('/')[-1].split('.')[0]
    data[model_name] = pd.read_csv(file)

# 初始化存储平均分值的字典
average_scores = {model: [] for model in data.keys()}

# 计算平均分值
for model_name, df in data.items():
    for input_type in ['normal', 'unmatch', 'both', 'malicious']:
        column_name = f'img_score_{input_type}'
        average_score = df[column_name].mean()
        average_scores[model_name].append(average_score)

# 输入类型作为维度
categories = ['normal', 'unmatch', 'both', 'malicious']
models = list(data.keys())

# 创建一个子图
fig, ax = plt.subplots(figsize=(14, 10), subplot_kw=dict(polar=True))

# 高级配色方案
sns.set_palette("husl")

# 绘制img_score的雷达图
r_range = (0, 25)

plot_radar_chart(
    ax,
    title='Img Score Radar Chart',
    categories=categories,
    values=average_scores,
    models=models,
    r_range=r_range
)

# 调整布局和配色
plt.tight_layout()
plt.savefig('radar_chart.png')
plt.show()
