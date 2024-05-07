import pandas as pd

import json

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as file:
        return json.load(file)

config = load_config("config.json")
output_path= config.get("count_path","")
root_dir = config.get("root_dir","")


df = pd.read_csv(output_path)  # 将'data.csv'替换为你的CSV文件路径

# 统计ID总数
total_ids = df['id'].nunique()  # 确保"id"列存在且id唯一性

# 统计Policy的各个种类个数
policy_counts = df['policy'].value_counts()

# 统计Attributes的各个种类个数
attributes_counts = df['original_attribute'].value_counts()

# 打印结果
print("Total IDs:", total_ids)
print("Policy Counts:\n", policy_counts)
print("Attributes Counts:\n", attributes_counts)
