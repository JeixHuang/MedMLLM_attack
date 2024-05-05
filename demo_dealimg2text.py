import pandas as pd
import os

# 指定 CSV 文件存放的文件夹
directory = 'metric/img2text_results'

# 用于存储最终结果的字典
results = {}

# 遍历指定文件夹下的所有 CSV 文件
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # 构造完整的文件路径
        filepath = os.path.join(directory, filename)
        
        # 读取 CSV 文件
        df = pd.read_csv(filepath)
        
        # 计算两种分数的平均值
        origin_score_avg = df['origin_score'].mean()
        unmatch_score_avg = df['unmatch_score'].mean()
        
        # 获取类别名称（假设文件名就是类别名称，去除 '.csv' 后缀）
        category = filename[:-4]
        
        # 将计算结果存入字典
        results[category] = {
            'origin_score_avg': origin_score_avg,
            'unmatch_score_avg': unmatch_score_avg
        }

# 将结果字典转换为 DataFrame
results_df = pd.DataFrame.from_dict(results, orient='index')

# 保存结果到新的 CSV 文件
results_df.to_csv('aggregated_scores.csv')

print("完成！已将平均分数保存到 'aggregated_scores.csv'")
