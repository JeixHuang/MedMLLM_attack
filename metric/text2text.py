from FlagEmbedding import BGEM3FlagModel
import argparse
import os

# 初始化模型
model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)

# 设置命令行参数
parser = argparse.ArgumentParser(description='Compare text files for similarity.')
parser.add_argument('--normal_text_folder', type=str, default='./output_normal', help='Folder containing normal text descriptions')
parser.add_argument('--harmful_text_folder', type=str, default='./output_harmful', help='Folder containing harmful text descriptions')
args = parser.parse_args()

# 获取文件夹路径
normal_text_directory = args.normal_text_folder
harmful_text_directory = args.harmful_text_folder

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
normal_texts = read_texts_from_folder(normal_text_directory)
harmful_texts = read_texts_from_folder(harmful_text_directory)

# 准备比较的句子对
sentence_pairs = []
for filename, normal_text in normal_texts.items():
    if filename in harmful_texts:
        harmful_text = harmful_texts[filename]
        sentence_pairs.append([normal_text, harmful_text])

# 计算并打印文本对的相似度
if sentence_pairs:
    similarity_scores = model.compute_score(sentence_pairs, max_passage_length=128, weights_for_different_modes=[0.4, 0.2, 0.4])
    print(similarity_scores)
else:
    print("No matching files found.")

# {
#   'colbert': [0.7796499729156494, 0.4621465802192688, 0.4523794651031494, 0.7898575067520142], 
#   'sparse': [0.195556640625, 0.00879669189453125, 0.0, 0.1802978515625], 
#   'dense': [0.6259765625, 0.347412109375, 0.349853515625, 0.67822265625], 
#   'sparse+dense': [0.482503205537796, 0.23454029858112335, 0.2332356721162796, 0.5122477412223816], 
#   'colbert+sparse+dense': [0.6013619303703308, 0.3255828022956848, 0.32089319825172424, 0.6232916116714478]
# }

# colbert：使用多向量交互匹配得到的分数。
# sparse：使用稀疏匹配得到的分数。
# dense：使用密集匹配得到的分数。
# sparse+dense：密集匹配和稀疏匹配分数的简单加和。
# colbert+sparse+dense：所有三种匹配模式的加权和，根据 weights_for_different_modes 指定的权重进行计算。
