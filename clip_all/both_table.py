import numpy as np
import pandas as pd

# 加载六维矩阵
matrix_path = 'clip_all_six_dimensional_matrix_avg.npy'
six_dimensional_matrix = np.load(matrix_path)

# 打印矩阵形状以确认降维后的形状
print("Original matrix shape:", six_dimensional_matrix.shape)

# 对policy和attribute维度进行降维
reduced_matrix = np.mean(six_dimensional_matrix, axis=(0, 1))

# 打印降维后的矩阵形状
print("Reduced matrix shape:", reduced_matrix.shape)

# 选择input维度为'both'的数据，input维度index为1
input_index = 1
input_filtered_matrix = reduced_matrix[:, :, input_index, :]

# 定义method、model和score的映射
method_mapping = ['gcg', 'pgd', 'mcm']
model_mapping = ['med-flamingo', 'RadFM', 'XrayGLM', 'CheXagent']
score_mapping = ['text_score', 'img_score', 'asr_score']

# 创建多级列索引
columns = pd.MultiIndex.from_product([model_mapping, score_mapping], names=['Model', 'Score'])

# 创建空的数据框
df = pd.DataFrame(index=method_mapping, columns=columns)

# 填充数据框
for method_idx, method in enumerate(method_mapping):
    row_data = []
    for model_idx, model in enumerate(model_mapping):
        for score_idx, score in enumerate(score_mapping):
            row_data.append(input_filtered_matrix[ model_idx,method_idx, score_idx])
    df.loc[method] = row_data

# 设置行索引名称
df.index.name = 'input'

# 输出表格
print(df)

# 保存表格为CSV文件
output_path = 'reduced_matrix_scores.csv'
df.to_csv(output_path)
print(f"表格已保存为 {output_path}")
