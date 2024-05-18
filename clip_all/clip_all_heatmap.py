import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import linkage, dendrogram
import numpy as np

# 定义文件夹路径
base_dir = "/home/huangxijie/MedMLLM_attack/"
output_dir = "/home/huangxijie/MedMLLM_attack/clip_ret_all"

# 创建输出目录
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 定义实验文件夹
folders = ["ret_gcg", "ret_pgd", "ret_mcm"]
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

# 将 attribute 列拆分成一级类和二级类
original_attributes[['primary_attribute', 'secondary_attribute']] = original_attributes['attribute'].str.split(' and ', expand=True)

# 合并原始属性和策略数据
scores_df = scores_df.merge(original_attributes, on="id")

# 定义分类树结构
policy_tree = {
    "Image Understanding": {
        "Coarse-grained": ["Disease Classification", "View Classification"],
        "Fine-grained": ["Abnormality Detection", "Object Detection"]
    },
    "Text Generation": {
        "Report Generation": ["Impression Generation", "Findings Generation"],
        "Findings and Impressions": ["Anatomical Findings", "Impression Summary"]
    },
    "Question Answering": {
        "Visual QA": ["Open-ended", "Close-ended"],
        "Text QA": ["Fact-based", "Inference-based"]
    },
    "Miscellaneous": {
        "Image-Text Matching": ["Matching", "Selection"],
        "Report Evaluation": ["Error Identification", "Quality Assessment"],
        "Explanation and Inference": ["Explanation Generation", "Inference Making"]
    }
}

attribute_tree = {
    "MRI": ["Alzheimer", "brain"],
    "Fundus": ["retinaFundus"],
    "Mamography": ["breast"],
    "OCT": ["retinaOCT"],
    "CT": ["heart", "brain", "chest"],
    "Endoscopy": ["gastroent"],
    "dermoscopy": ["skin"],
    "Ultrasound": ["carotid", "breast", "ovary", "brain", "baby"],
    "X-ray": ["Skeleton", "Dental", "chest"]
}

# 定义绘制分类树的函数
def plot_dendrogram(tree, title, orientation='top'):
    labels = []
    for key, value in tree.items():
        if isinstance(value, list):
            labels.extend(value)
        else:
            for sub_key, sub_value in value.items():
                labels.extend(sub_value)
    data = np.random.rand(len(labels), 2)
    linked = linkage(data, 'single')
    plt.figure(figsize=(8, 8))
    dendrogram(linked, labels=labels, orientation=orientation)
    plt.title(title)
    plt.show()

# 绘制分类树
plot_dendrogram(policy_tree, "Policy Classification Tree", orientation='top')
plot_dendrogram(attribute_tree, "Attribute Classification Tree", orientation='left')

# 生成热力图
def plot_heatmap(df, model, method, score_type, input_type, output_dir):
    score_column = f"{score_type}_score_{input_type}"
    if score_column not in df.columns:
        print(f"Skipping heatmap for {model} with {method} on {score_column} (column not found)")
        return
    
    # 生成透视表
    pivot_table = pd.pivot_table(df, values=score_column, 
                                 index="secondary_attribute", columns="policy", aggfunc='mean')
    
    plt.figure(figsize=(12, 12))  # 保证图形为正方形
    sns.heatmap(pivot_table, cmap="YlGnBu", cbar_kws={'label': 'Score'})
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
