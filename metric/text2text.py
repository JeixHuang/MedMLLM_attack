from FlagEmbedding import BGEM3FlagModel
import argparse
import os
import pandas as pd

# 初始化模型
model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)

# 设置命令行参数
parser = argparse.ArgumentParser(description='Compare text files for similarity.')
parser.add_argument('--normal_text_folder', type=str, default='./output_normal', help='Folder containing normal text descriptions')
parser.add_argument('--harmful_text_folder', type=str, default='./output_harmful', help='Folder containing harmful text descriptions')
args = parser.parse_args()

# 读取文件名和内容
def read_texts_from_folder(folder):
    texts = {}
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                texts[filename] = file.read()
    return texts

# 加载文本
normal_texts = read_texts_from_folder(args.normal_text_folder)
harmful_texts = read_texts_from_folder(args.harmful_text_folder)

# 准备比较的句子对
sentence_pairs = []
file_pairs = []
for filename, normal_text in normal_texts.items():
    if filename in harmful_texts:
        harmful_text = harmful_texts[filename]
        sentence_pairs.append([normal_text, harmful_text])
        file_pairs.append(filename)

# 计算文本对的相似度并保存到表格
if sentence_pairs:
    similarity_scores = model.compute_score(sentence_pairs, max_passage_length=128, weights_for_different_modes=[0.4, 0.2, 0.4])
    df_scores = pd.DataFrame(similarity_scores)
    df_scores['File Pair'] = file_pairs
    df_scores = df_scores[['File Pair', 'colbert', 'sparse', 'dense', 'sparse+dense', 'colbert+sparse+dense']]
    print(df_scores)
else:
    print("No matching files found.")
