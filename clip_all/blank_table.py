import numpy as np
import pandas as pd

# 加载六维矩阵数据
data = np.load('blank_clip_all_six_dimensional_matrix_avg.npy')

# 定义映射
policy_mapping = ["Open-ended", "Anatomical Findings", "Explanation Generation", "Selection", "Findings Generation",
                  "Quality Assessment", "Error Identification", "Impression Summary", "Close-ended", "Impression Generation",
                  "View Classification", "Disease Classification", "Object Detection", "Inference-based", "Matching",
                  "Inference Making", "Abnormality Detection", "Fact-based"]

attribute_mapping = ["Dermoscopy and Skin", "MRI and Alzheimer", "MRI and Brain", "Fundus and Retina", "Mamography and Breast",
                     "OCT and Retina", "CT and Chest", "CT and Heart", "CT and Brain", "Xray and Chest", "Xray and Skeleton",
                     "Xray and Dental", "Endoscopy and Gastroent", "Ultrasound and Baby", "Ultrasound and Breast",
                     "Ultrasound and Carotid", "Ultrasound and Ovary", "Ultrasound and Brain"]

model_mapping = ["med-flamingo", "RadFM", "XrayGLM", "CheXagent"]

input_mapping = ["unmatch", "both", "malicious", "normal"]

score_mapping = ["text_score", "img_score", "asr_score"]

# 对 policy 和 attribute 维度进行平均
reduced_data = np.mean(data, axis=(0, 1, 3))

# 创建 DataFrame
df = pd.DataFrame(reduced_data.reshape(-1, 1), columns=['value'])

# 为每个维度创建标签
df['model'] = np.tile(np.repeat(np.arange(4), 3), 4)
df['input'] = np.repeat(np.arange(4), 12)
df['score_type'] = np.tile(np.arange(3), 16)

# 将数字映射到相应的字符串标签
df['model'] = df['model'].map(dict(enumerate(model_mapping)))
df['input'] = df['input'].map(dict(enumerate(input_mapping)))
df['score_type'] = df['score_type'].map(dict(enumerate(score_mapping)))

# 生成表格，并按索引排序
table = pd.pivot_table(df, values='value', index='input', columns=['model', 'score_type'])

# 按索引排序
table = table.reindex(columns=pd.MultiIndex.from_product([model_mapping, score_mapping]))
table = table.sort_index(axis=0, level='input')

# 输出表格
print(table)