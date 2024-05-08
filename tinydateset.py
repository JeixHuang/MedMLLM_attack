import pandas as pd

# 读取原始 CSV 文件
file_path = 'CMIC/3MAD-68K.csv'
data = pd.read_csv(file_path)

# 初始化一个空的 DataFrame 以存储筛选后的数据
filtered_data = pd.DataFrame(columns=data.columns)

# 每个 original_attribute 按 policy 分配尽量均匀的 60 行
num_samples = 60
original_attributes = data['original_attribute'].unique()
policies = data['policy'].unique()
num_policies = len(policies)

for attribute in original_attributes:
    attribute_group = data[data['original_attribute'] == attribute]
    
    # 初始化 policy 计数器
    policy_counts = {policy: 0 for policy in policies}
    samples = pd.DataFrame(columns=data.columns)
    
    # 确保每个 policy 尽量均匀分配
    while len(samples) < num_samples:
        for policy in policies:
            if policy_counts[policy] < num_samples // num_policies:
                policy_group = attribute_group[attribute_group['policy'] == policy]
                sample_count = min(1, len(policy_group) - policy_counts[policy])
                if sample_count > 0:
                    samples = pd.concat([samples, policy_group.iloc[policy_counts[policy]:policy_counts[policy] + sample_count]])
                    policy_counts[policy] += sample_count
        # 假如某个 `policy` 样本不足时，用其他数据填充
        if len(samples) < num_samples:
            remaining_samples = attribute_group[~attribute_group.index.isin(samples.index)].sample(num_samples - len(samples), replace=True)
            samples = pd.concat([samples, remaining_samples])
    
    filtered_data = pd.concat([filtered_data, samples])

# 确保总行数为 1080，并给 id 重新编号
filtered_data.reset_index(drop=True, inplace=True)
filtered_data['id'] = filtered_data.index + 1

# 将数据保存到新的 CSV 文件
output_path = '3MAD-Tiny-1K.csv'
filtered_data.to_csv(output_path, index=False)

print(f'数据已保存至：{output_path}')
