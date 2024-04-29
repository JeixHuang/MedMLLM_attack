import csv
import random

# 加载general_prompts.csv
prompts_dict = {}
with open('general_prompts.csv', mode='r') as prompts_file:
    reader = csv.DictReader(prompts_file)
    for row in reader:
        prompts_dict[row['id']] = row

# 读取data.csv
data_rows = []
with open('MedMQ-21k.csv', mode='r') as data_file:
    reader = csv.DictReader(data_file)
    for row in reader:
        data_rows.append(row)

# 对于data.csv中的每一行，随机选择一个prompt
updated_rows = []
img_to_prompt_id = {}  # 存储图片路径到prompt id的映射

for row in data_rows:
    img_path = row['img']
    if img_path not in img_to_prompt_id:
        # 随机选择一个prompt id
        prompt_id = random.choice(list(prompts_dict.keys()))
        img_to_prompt_id[img_path] = prompt_id
    
    selected_prompt = prompts_dict[img_to_prompt_id[img_path]]
    
    if row['attack_category'] == 'unmatch':
        row['prompts'] = selected_prompt['question']
    else:
        row['prompts'] = selected_prompt['malicious_question']
    
    row['policy'] = selected_prompt['policy']
    row['key_phrases'] = selected_prompt['key_phrases']

    updated_rows.append(row)

# 将更新后的数据写回data.csv
with open('MedMQ-21k.csv', mode='w', newline='') as file:
    fieldnames = ['id', 'attack_category', 'img', 'attributes', 'prompts', 'policy', 'key_phrases']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print("data.csv 文件已经更新完毕。")
