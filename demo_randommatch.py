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
with open('3MAD-28K.csv', mode='r') as data_file:
    reader = csv.DictReader(data_file)
    for row in reader:
        data_rows.append(row)

# 收集所有可能的介质和部位组合
all_media_parts = set((row['attributes'].split(' and ')[0], row['attributes'].split(' and ')[1]) for row in data_rows)

# 准备更新后的数据
updated_rows = []
img_to_prompt_id = {}  # 存储图片路径到prompt id的映射

for row in data_rows:
    img_path = row['img']

    # 如果这张图片还没有分配prompt ID，随机选择一个
    if img_path not in img_to_prompt_id:
        prompt_id = random.choice(list(prompts_dict.keys()))
        img_to_prompt_id[img_path] = prompt_id

    # 获取选中的prompt信息
    selected_prompt = prompts_dict[img_to_prompt_id[img_path]]

    # 根据attack_category填充prompts
    if row['attack_category'] == 'unmatch':
        row['prompts'] = selected_prompt['question']
    else:
        row['prompts'] = selected_prompt['malicious_question']
        # 随机选择一个不同的介质和部位组合进行替换
        possible_replacements = list(all_media_parts - {(row['attributes'].split(' and ')[0], row['attributes'].split(' and ')[1])})
        if possible_replacements:
            new_media_part = random.choice(possible_replacements)
            row['attributes'] = ' and '.join(new_media_part)

    # 更新policy和key_phrases
    row['policy'] = selected_prompt['policy']
    row['key_phrases'] = selected_prompt['key_phrases']

    updated_rows.append(row)

# 将更新后的数据写回data.csv
with open('3MAD-28K.csv', mode='w', newline='') as file:
    fieldnames = ['id', 'attack_category', 'img', 'attributes', 'prompts', 'policy', 'key_phrases']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print("data.csv 文件已经更新完毕。")
