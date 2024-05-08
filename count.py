import pandas as pd
import json

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# config = load_config("config.json")
# output_path= config.get("output_path","")
# root_dir = config.get("img_dir","")


# 设置 CSV 文件路径
output_path = "CMIC/3MAD-Tiny-1K.csv"  # 请替换为实际文件路径

# 使用 `usecols` 参数排除 `file_name` 列
columns_to_use = ['id', 'original_attribute', 'unmatch_attribute', 'normal_prompt', 'harmful_prompt', 'policy', 'key_phrases']

# 尝试读取文件并处理列
try:
    df = pd.read_csv(output_path, usecols=columns_to_use)

    # 统计唯一的 ID 数量
    total_ids = df['id'].nunique()

    # 统计 Policy 的各个种类数量
    policy_counts = df['policy'].value_counts()

    # 统计 Attributes 的各个种类数量
    attributes_counts = df['original_attribute'].value_counts()

    # 打印结果
    print("Total IDs:", total_ids)
    print("Policy Counts:\n", policy_counts)
    print("Attributes Counts:\n", attributes_counts)

except pd.errors.ParserError as e:
    print(f"Error parsing the CSV file: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
