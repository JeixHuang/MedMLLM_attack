# import pandas as pd

# # 读取CSV文件
# df = pd.read_csv('general_prompts.csv')

# # 确保你的CSV文件中有足够的列，下面的代码假设第三列索引为2（因为索引从0开始）
# # 计算第三列中各个名字出现的次数
# name_counts = df.iloc[:, 3].value_counts()

# # 打印结果
# print(name_counts)

from datasets import load_dataset

dataset = load_dataset("MedMLLM-attack/3MAD-70K")