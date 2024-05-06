import pandas as pd

# 1. 加载CSV文件
df = pd.read_csv("metric/med2na_nature_img2text/train_results.csv")

# 2. 根据"policy"列进行分组，并计算其他列的平均值
# averaged_df = df[.groupby("origin_score")].mean().reset_index()
# averaged_df_un = df.groupby("unmatch_score").mean().reset_index()
# # 3. 将结果写入新的CSV文件或更新原始CSV文件
# averaged_df.to_csv("nature_averaged_file.csv", index=False)

# Calculate the mean of the specified columns and create a DataFrame
averaged_df = pd.DataFrame({
    'origin_score_mean': [df['origin_score'].mean()],
    'unmatch_score_mean': [df['unmatch_score'].mean()]
})

# Save the DataFrame to a CSV file
averaged_df.to_csv("metric/med2na_nature_img2text/train_results_avg.csv", index=False)
