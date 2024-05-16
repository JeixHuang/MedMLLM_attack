import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.stats import pearsonr
import statsmodels.api as sm

# 加载数据
data = np.load('clip_all_six_dimensional_matrix_avg.npy')

# 获取数据维度
policy_dim, attribute_dim, model_dim, method_dim, input_dim, score_dim = data.shape

# 将6维数据展平成2维数据，并提取分数
data_reshaped = data.reshape(-1, score_dim)
scores = data_reshaped[:, -1]

# 生成每个点的标签
labels = []
for p in range(policy_dim):
    for a in range(attribute_dim):
        for m in range(model_dim):
            for met in range(method_dim):
                for i in range(input_dim):
                    labels.append(f'P{p}_A{a}_M{m}_Met{met}_I{i}')

# 创建DataFrame
df = pd.DataFrame(data_reshaped, columns=[f'Dim_{i}' for i in range(score_dim)])
df['Label'] = labels
df['Policy'] = [int(label.split('_')[0][1:]) for label in labels]
df['Attribute'] = [int(label.split('_')[1][1:]) for label in labels]
df['Model'] = [int(label.split('_')[2][1:]) for label in labels]
df['Method'] = [int(label.split('_')[3][3:]) for label in labels]
df['Input'] = [int(label.split('_')[4][1:]) for label in labels]

# 统计分析 - 计算每个维度的平均分数并绘制条形图
avg_scores_policy = df.groupby('Policy')[f'Dim_{score_dim-1}'].mean()
avg_scores_attribute = df.groupby('Attribute')[f'Dim_{score_dim-1}'].mean()
avg_scores_model = df.groupby('Model')[f'Dim_{score_dim-1}'].mean()
avg_scores_method = df.groupby('Method')[f'Dim_{score_dim-1}'].mean()
avg_scores_input = df.groupby('Input')[f'Dim_{score_dim-1}'].mean()

fig, axes = plt.subplots(3, 2, figsize=(15, 15))

avg_scores_policy.plot(kind='bar', ax=axes[0, 0], title='Average Scores by Policy')
avg_scores_attribute.plot(kind='bar', ax=axes[0, 1], title='Average Scores by Attribute')
avg_scores_model.plot(kind='bar', ax=axes[1, 0], title='Average Scores by Model')
avg_scores_method.plot(kind='bar', ax=axes[1, 1], title='Average Scores by Method')
avg_scores_input.plot(kind='bar', ax=axes[2, 0], title='Average Scores by Input')

# 隐藏最后一个子图
axes[2, 1].axis('off')

plt.tight_layout()
plt.savefig('average_scores_by_dimension.png')
plt.show()

# 相关性分析 - 计算每个维度的相关性并绘制热图
correlation_results = {}
p_values = {}
for col in ['Policy', 'Attribute', 'Model', 'Method', 'Input']:
    correlation, p_value = pearsonr(df[col], df[f'Dim_{score_dim-1}'])
    correlation_results[col] = correlation
    p_values[col] = p_value

correlation_df = pd.DataFrame(list(correlation_results.items()), columns=['Dimension', 'Correlation'])
p_values_df = pd.DataFrame(list(p_values.items()), columns=['Dimension', 'P-Value'])

plt.figure(figsize=(10, 6))
sns.heatmap(correlation_df.set_index('Dimension').T, annot=True, cmap='coolwarm')
plt.title('Correlation between Dimensions and Scores')
plt.savefig('correlation_heatmap.png')
plt.show()

# 回归分析 - 进行多元回归并绘制回归系数条形图
X = df[['Policy', 'Attribute', 'Model', 'Method', 'Input']]
y = df[f'Dim_{score_dim-1}']
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print(model.summary())

coefficients = model.params[1:]  # 排除常数项
coefficients.plot(kind='bar', title='Regression Coefficients')
plt.ylabel('Coefficient Value')
plt.savefig('regression_coefficients.png')
plt.show()
