import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import linkage, dendrogram

# 定义文件夹路径
base_dir = "/home/huangxijie/MedMLLM_attack/"
output_dir = "/home/huangxijie/MedMLLM_attack/clip_ret_all"

# 创建输出目录
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 定义实验文件夹
folders = [ "ret_gcg", "ret_pgd", "ret_mcm"]
methods = ["gcg", "pgd", "mcm"]
input_types = ["unmatch", "both", "malicious"]

# 读取每个模型的分数数据
def read_scores(folder, method):
    scores = []
    processed_dir = os.path.join(base_dir, folder, "processed_ret")
    for filename in os.listdir(processed_dir):
        if filename.endswith(".csv"):
            model_name = filename.replace(".csv", "")
            file_path = os.path.join(processed_dir, filename)
            df = pd.read_csv(file_path)
            df["model"] = model_name
            df["method"] = method
            
            # 根据文件夹名称处理列名
            if folder == "ret_normal":
                df["img_score_both"] = None
                df["text_both_score"] = None
            
            scores.append(df)
    return pd.concat(scores, ignore_index=True)

# 合并所有数据
all_scores = []
for folder, method in zip(folders, methods):
    all_scores.append(read_scores(folder, method))
scores_df = pd.concat(all_scores, ignore_index=True)

# 删除全为NA的列
scores_df = scores_df.dropna(axis=1, how='all')

# 读取原始属性和策略数据
original_attributes = pd.read_csv(os.path.join(base_dir, "CMIC/3MAD-Tiny-1K.csv"))

# 合并原始属性和策略数据
scores_df = scores_df.merge(original_attributes, on="id")

# 可视化函数
def plot_scores(df, input_type, score_type, score_column, title, output_dir):
    plt.figure(figsize=(12, 8))
    sns.boxplot(x="model", y=score_column, hue="method", data=df)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    output_file = os.path.join(output_dir, f"{input_type}_{score_type}.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Saved {title} at {output_file}")

def plot_distribution(df, input_type, score_type, score_column, title, output_dir):
    plt.figure(figsize=(12, 8))
    sns.histplot(data=df, x=score_column, hue="model", element="step", stat="density", common_norm=False)
    plt.title(title)
    plt.tight_layout()
    output_file = os.path.join(output_dir, f"{input_type}_{score_type}_distribution.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Saved Distribution of {title} at {output_file}")

def plot_pairwise(df, input_type, score_type, output_dir):
    plt.figure(figsize=(12, 8))
    sns.pairplot(df, hue="model", vars=[f"{score_type}_score_{input_type}"], diag_kind="kde")
    output_file = os.path.join(output_dir, f"{input_type}_{score_type}_pairwise.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Saved Pairwise Comparison of {score_type.capitalize()} Scores for {input_type.capitalize()} Inputs at {output_file}")

# 创建可视化
for input_type in input_types:
    for score_type in ["img", "text"]:
        score_column = f"{score_type}_score_{input_type}"
        title = f"{score_type.capitalize()} Scores for {input_type.capitalize()} Inputs"
        plot_scores(scores_df, input_type, score_type, score_column, title, output_dir)
        plot_distribution(scores_df, input_type, score_type, score_column, f"Distribution of {title}", output_dir)
        plot_pairwise(scores_df, input_type, score_type, output_dir)

# 多维度分析
def multi_dimension_analysis(df, output_dir):
    sns.pairplot(df, hue="method")
    output_file = os.path.join(output_dir, "multi_dimension_analysis.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Saved Multi Dimension Analysis at {output_file}")

# multi_dimension_analysis(scores_df, output_dir)

# 生成热力图
def plot_heatmap(df, model, method, score_type, input_type, output_dir):
    score_column = f"{score_type}_score_{input_type}"
    if score_column not in df.columns:
        print(f"Skipping heatmap for {model} with {method} on {score_column} (column not found)")
        return
    
    # 生成透视表
    pivot_table = pd.pivot_table(df, values=score_column, 
                                 index="original_attribute", columns="policy", aggfunc='mean')
    
    # 对行和列进行排序，使得最大值在右上角，最小值在左下角
    sorted_rows = pivot_table.mean(axis=1).sort_values(ascending=False).index
    sorted_cols = pivot_table.mean(axis=0).sort_values(ascending=False).index
    
    sorted_pivot_table = pivot_table.loc[sorted_rows, sorted_cols]
    
    plt.figure(figsize=(12, 12))
    sns.heatmap(sorted_pivot_table, annot=True, cmap="YlGnBu")
    plt.title(f"Heatmap of {score_type.capitalize()} Scores for {model} using {method} ({input_type} inputs)")
    plt.tight_layout()
    output_file = os.path.join(output_dir, f"heatmap_{model}_{method}_{score_type}_{input_type}.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Saved Heatmap of {score_type.capitalize()} Scores for {model} using {method} ({input_type} inputs) at {output_file}")

# 生成所有热力图
for model in scores_df["model"].unique():
    for method in methods:
        for score_type in ["img", "text"]:
            for input_type in input_types:
                plot_heatmap(scores_df[(scores_df["model"] == model) & (scores_df["method"] == method)], 
                             model, method, score_type, input_type, output_dir)