import os
import pandas as pd
import numpy as np

'''
Policy Mapping:
Index 0: Open-ended
Index 1: Anatomical Findings
Index 2: Explanation Generation
Index 3: Selection
Index 4: Findings Generation
Index 5: Quality Assessment
Index 6: Error Identification
Index 7: Impression Summary
Index 8: Close-ended
Index 9: Impression Generation
Index 10: View Classification
Index 11: Disease Classification
Index 12: Object Detection
Index 13: Inference-based
Index 14: Matching
Index 15: Inference Making
Index 16: Abnormality Detection
Index 17: Fact-based

Attribute Mapping:
Index 0: Dermoscopy and Skin
Index 1: MRI and Alzheimer
Index 2: MRI and Brain
Index 3: Fundus and Retina
Index 4: Mamography and Breast
Index 5: OCT and Retina
Index 6: CT and Chest
Index 7: CT and Heart
Index 8: CT and Brain
Index 9: Xray and Chest
Index 10: Xray and Skeleton
Index 11: Xray and Dental
Index 12: Endoscopy and Gastroent
Index 13: Ultrasound and Baby
Index 14: Ultrasound and Breast
Index 15: Ultrasound and Carotid
Index 16: Ultrasound and Ovary
Index 17: Ultrasound and Brain

Model Mapping:
Index 0: med-flamingo
Index 1: RadFM
Index 2: XrayGLM
Index 3: CheXagent

Method Mapping:
Index 0: gcg
Index 1: pgd
Index 2: mcm

Input Mapping:
Index 0: unmatch
Index 1: both
Index 2: malicious

'''
# 定义文件夹路径
base_dir = "/home/huangxijie/MedMLLM_attack/"
output_dir = "/home/huangxijie/MedMLLM_attack/clip_all"

# 创建输出目录
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 定义实验文件夹和相关参数
folders = ["transfer_experiment/ret_gcg", "transfer_experiment/ret_pgd", "transfer_experiment/ret_mcm"]
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
original_attributes[['primary_attribute', 'secondary_attribute']] = original_attributes['original_attribute'].str.split(' and ', expand=True)

# 合并原始属性和策略数据
scores_df = scores_df.merge(original_attributes, on="id")

# 创建六维矩阵
score_sums = np.zeros((18, 18, 4, 3, 3, 3))  # 用于累加分数
score_counts = np.zeros((18, 18, 4, 3, 3, 3))  # 用于计数

# 映射策略、属性、模型、攻击方法和输入类型到索引
policy_mapping = {policy: idx for idx, policy in enumerate(scores_df['policy'].unique())}
attribute_mapping = {attribute: idx for idx, attribute in enumerate(scores_df['original_attribute'].unique())}
model_mapping = {model: idx for idx, model in enumerate(scores_df['model'].unique())}
method_mapping = {method: idx for idx, method in enumerate(methods)}
input_mapping = {input_type: idx for idx, input_type in enumerate(input_types)}
score_mapping = {'text_score': 0, 'img_score': 1,'asr_score':2}

# 反向映射
policy_reverse_mapping = {idx: policy for policy, idx in policy_mapping.items()}
attribute_reverse_mapping = {idx: attribute for attribute, idx in attribute_mapping.items()}
model_reverse_mapping = {idx: model for model, idx in model_mapping.items()}
method_reverse_mapping = {idx: method for method, idx in method_mapping.items()}
input_reverse_mapping = {idx: input_type for input_type, idx in input_mapping.items()}
score_reverse_mapping = {0: 'text_score', 1: 'img_score',2:'asr_score'}

# 填充六维矩阵
for _, row in scores_df.iterrows():
    policy_idx = policy_mapping[row['policy']]
    attribute_idx = attribute_mapping[row['original_attribute']]
    model_idx = model_mapping[row['model']]
    method_idx = method_mapping[row['method']]
    
    for input_type in input_types:
        input_idx = input_mapping[input_type]
        
        text_score_column = f"text_score_{input_type}"
        img_score_column = f"img_score_{input_type}"
        asr_score_column = f"asr_score_{input_type}"
        
        if text_score_column in row and not pd.isna(row[text_score_column]):
            score_sums[policy_idx, attribute_idx, model_idx, method_idx, input_idx, score_mapping['text_score']] += row[text_score_column]
            score_counts[policy_idx, attribute_idx, model_idx, method_idx, input_idx, score_mapping['text_score']] += 1
        
        if img_score_column in row and not pd.isna(row[img_score_column]):
            score_sums[policy_idx, attribute_idx, model_idx, method_idx, input_idx, score_mapping['img_score']] += row[img_score_column]
            score_counts[policy_idx, attribute_idx, model_idx, method_idx, input_idx, score_mapping['img_score']] += 1
            
        if asr_score_column in row and not pd.isna(row[asr_score_column]):
            score_sums[policy_idx, attribute_idx, model_idx, method_idx, input_idx, score_mapping['asr_score']] += row[asr_score_column]
            score_counts[policy_idx, attribute_idx, model_idx, method_idx, input_idx, score_mapping['asr_score']] += 1

def print_mappings():
    print("Policy Mapping:")
    for idx in range(len(policy_reverse_mapping)):
        print(f"Index {idx}: {policy_reverse_mapping[idx]}")

    print("\nAttribute Mapping:")
    for idx in range(len(attribute_reverse_mapping)):
        print(f"Index {idx}: {attribute_reverse_mapping[idx]}")

    print("\nModel Mapping:")
    for idx in range(len(model_reverse_mapping)):
        print(f"Index {idx}: {model_reverse_mapping[idx]}")

    print("\nMethod Mapping:")
    for idx in range(len(method_reverse_mapping)):
        print(f"Index {idx}: {method_reverse_mapping[idx]}")

    print("\nInput Mapping:")
    for idx in range(len(input_reverse_mapping)):
        print(f"Index {idx}: {input_reverse_mapping[idx]}")
        
# 计算平均值
average_scores = np.divide(score_sums, score_counts, where=score_counts != 0)

# 保存六维矩阵
output_file = os.path.join(output_dir, "clip_all_six_dimensional_matrix_avg.npy")
np.save(output_file, average_scores)
print(f"Saved six-dimensional average matrix at {output_file}")

# 显示示例坐标和对应分值
def print_example_scores():
    for policy_idx in range(18):
        for attribute_idx in range(18):
            for model_idx in range(4):
                for method_idx in range(3):
                    for input_idx in range(3):
                        text_score = average_scores[policy_idx, attribute_idx, model_idx, method_idx, input_idx, score_mapping['text_score']]
                        img_score = average_scores[policy_idx, attribute_idx, model_idx, method_idx, input_idx, score_mapping['img_score']]
                        asr_score = average_scores[policy_idx, attribute_idx, model_idx, method_idx, input_idx, score_mapping['asr_score']]
                        print(f"Policy: {policy_reverse_mapping[policy_idx]}, Attribute: {attribute_reverse_mapping[attribute_idx]}, Model: {model_reverse_mapping[model_idx]}, Method: {method_reverse_mapping[method_idx]}, Input: {input_reverse_mapping[input_idx]}")
                        print(f"Text Score: {text_score}, Image Score: {img_score}, ASR Score: {asr_score}")

print_example_scores()
print_mappings()

