import pandas as pd

# 1. 加载CSV文件
df = pd.read_csv("similarity_results.csv")

# 2. 根据"policy"列进行分组，并计算其他列的平均值
averaged_df = df.groupby("Policy").mean().reset_index()

# 3. 将结果写入新的CSV文件或更新原始CSV文件
averaged_df.to_csv("averaged_file.csv", index=False)
