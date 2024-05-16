import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import pandas as pd
from collections import Counter

# 加载数据
data = np.load('clip_all_six_dimensional_matrix_avg.npy')

# 获取数据维度
policy_dim, attribute_dim, model_dim, method_dim, input_dim, score_dim = data.shape

# 将6维数据展平成2维数据
data_reshaped = data.reshape(-1, data.shape[-1])

# 数据标准化
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data_reshaped)

# PCA降维
pca = PCA(n_components=2)
pca_result = pca.fit_transform(data_scaled)

# t-SNE降维
tsne = TSNE(n_components=2, random_state=42)
tsne_result = tsne.fit_transform(data_scaled)

# 生成每个点的标签
labels = []
for p in range(policy_dim):
    for a in range(attribute_dim):
        for m in range(model_dim):
            for met in range(method_dim):
                for i in range(input_dim):
                    labels.append(f'P{p}_A{a}_M{m}_Met{met}_I{i}')

# 为每个点生成颜色和形状
colors = np.repeat(np.arange(policy_dim), attribute_dim * model_dim * method_dim * input_dim)
shapes = np.tile(np.arange(attribute_dim), policy_dim * model_dim * method_dim * input_dim)

# 可视化PCA结果
plt.figure(figsize=(12, 9))
scatter = plt.scatter(pca_result[:, 0], pca_result[:, 1], c=colors, alpha=0.5, marker='o', cmap='tab10')
plt.title('PCA Result')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar(scatter, ticks=range(policy_dim), label='Policy Index')
plt.grid(True)
plt.savefig('PCA.png')
plt.show()

# 可视化t-SNE结果
plt.figure(figsize=(12, 9))
scatter = plt.scatter(tsne_result[:, 0], tsne_result[:, 1], c=colors, alpha=0.5, marker='o', cmap='tab10')
plt.title('t-SNE Result')
plt.xlabel('Dimension 1')
plt.ylabel('Dimension 2')
plt.colorbar(scatter, ticks=range(policy_dim), label='Policy Index')
plt.grid(True)
plt.savefig('t-SNE.png')
plt.show()

# 层次聚类和热图
linkage_matrix = linkage(data_scaled, method='ward')
clusters = fcluster(linkage_matrix, t=20, criterion='maxclust')

# 创建一个自定义的clustermap
g = sns.clustermap(pd.DataFrame(data_scaled), method='ward', cmap='viridis', row_cluster=True, col_cluster=True)
plt.title('Heatmap with Hierarchical Clustering')

# 添加类标签
for label, (i, row) in zip(labels, enumerate(g.data2d.index)):
    g.ax_heatmap.text(-0.01, i, label, fontsize=6, ha='right', va='center', transform=g.ax_heatmap.get_yaxis_transform())

plt.savefig('Heatmap-with-Hierarchical-Clustering.png')
plt.show()

# 聚类结果解释
cluster_info = pd.DataFrame({'Label': labels, 'Cluster': clusters})
for cluster in cluster_info['Cluster'].unique():
    cluster_data = cluster_info[cluster_info['Cluster'] == cluster]
    print(f'Cluster {cluster}:')

    # 提取聚类标签中各维度的信息
    policies = [int(label.split('_')[0][1:]) for label in cluster_data['Label']]
    attributes = [int(label.split('_')[1][1:]) for label in cluster_data['Label']]
    models = [int(label.split('_')[2][1:]) for label in cluster_data['Label']]
    methods = [int(label.split('_')[3][3:]) for label in cluster_data['Label']]
    inputs = [int(label.split('_')[4][1:]) for label in cluster_data['Label']]
    
    # 统计每个维度的分布
    policy_counts = Counter(policies)
    attribute_counts = Counter(attributes)
    model_counts = Counter(models)
    method_counts = Counter(methods)
    input_counts = Counter(inputs)
    
    # 打印统计结果
    print("Policy 分布：", policy_counts)
    print("Attribute 分布：", attribute_counts)
    print("Model 分布：", model_counts)
    print("Method 分布：", method_counts)
    print("Input 分布：", input_counts)
    print()

# 打印PCA解释方差比例
print("Explained variance ratio by PCA components:")
print(pca.explained_variance_ratio_)

# 打印主成分负载
print("PCA components loadings:")
print(pca.components_)
