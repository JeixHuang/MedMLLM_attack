import pandas as pd

file_path = "general_prompts.csv"
# file_path = "CMIC/3MAD-66K.csv"
# file_path = "CMIC/3MAD-Tiny-1K.csv"


df = pd.read_csv(file_path)


null_count = df.isnull().sum()
null_list = df.isnull()

for column, count in null_count.items():
    print(f"列 '{column}' 中有 {count} 个空值")

print(null_list)


null_positions = null_list.stack()

empty_locations = null_positions[null_positions]
if empty_locations.empty:
    print("没有空值")
else:
    print("\n空值的位置（行索引, 列名）：")
    for index, column in empty_locations.index:
        print(f"行索引: {index}, 列: {column}")