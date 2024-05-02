import pandas as pd

# 加载CSV文件
df = pd.read_csv('3MAD-28K.csv')  # 将'data.csv'替换为你的CSV文件路径

# 统计ID总数
total_ids = df['id'].nunique()  # 确保"id"列存在且id唯一性

# 统计Policy的各个种类个数
policy_counts = df['policy'].value_counts()

# 统计Attributes的各个种类个数
attributes_counts = df['attributes'].value_counts()

# 打印结果
print("Total IDs:", total_ids)
print("Policy Counts:\n", policy_counts)
print("Attributes Counts:\n", attributes_counts)
