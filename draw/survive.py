import os
import pandas as pd
import matplotlib.pyplot as plt

# 指定CSV文件夹路径
folder_path = '../llavamed_ret_patch/processed_ret'

compare_path='../ret_llavamed/ret_llavamed_score.csv'
# 获取文件夹中的所有CSV文件
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

df_compare = pd.read_csv(compare_path)
# iter_compare = df_compare[]
# 遍历每个CSV文件
for csv_file in csv_files:
    # 读取CSV文件
    df = pd.read_csv(os.path.join(folder_path, csv_file))

    # 获取所有iter
    iters = df['iter'].unique()
    
    # 创建一个字典来存储不同score类型的均值和标准差
    scores = {
        'img_score_malicious': [],
        'img_score_unmatch': [],
        'img_score_both': [],
        'text_malicious_score': [],
        'text_unmatch_score': [],
        'text_both_score': []
    }
    
    for score_type in scores.keys():
        for i in iters:
            iter_df = df[df['iter'] == i]
            scores[score_type].append((iter_df[score_type].mean(), iter_df[score_type].std()))

    # 绘制分数变化趋势图
    plt.figure(figsize=(14, 8))

    for score_type, values in scores.items():
        means = [val[0] for val in values]
        stds = [val[1] for val in values]
        plt.plot(iters, means, label=f'{score_type} mean', marker='o')
        plt.fill_between(iters, [m-s for m, s in zip(means, stds)], [m+s for m, s in zip(means, stds)], alpha=0.2)

    # 图表信息
    plt.title(f'Survival Curves in file {csv_file}')
    plt.xlabel('Iteration')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)

    # 保存图表
    plt.savefig(os.path.join(folder_path, f'ret_{csv_file.split(".")[0]}_survival_curve.png'))
    plt.close()

print("Survival curves have been saved successfully.")
