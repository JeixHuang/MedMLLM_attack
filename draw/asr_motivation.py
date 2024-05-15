import matplotlib.pyplot as plt
import numpy as np

# 数据
categories = ['Med-flamingo', 'RADFM', 'Gemini']
asr = [30.534804, 29.0019775, 29.42414296]
rr = [17.048547, 23.11666, 23.42917159]
clipscore=[30.534804, 29.0019775, 29.42414296]

# 转换为两位小数
asr = [round(score, 2) for score in asr]
rr = [round(score, 2) for score in rr]
cs =[round(score, 2) for score in clipscore]
x = np.arange(len(categories))  # 分类的 x 轴位置
width = 0.25  # 柱状图的宽度

fig, ax = plt.subplots()

rects1 = ax.bar(x - width, asr, width, label='ASR', color='#D5E8D4')
rects2 = ax.bar(x , rr, width, label='RR', color='#F8CECC')
rects3 = ax.bar(x + width, cs, width, label='CS', color='#E1D5E7')
# 添加文本标签、标题和自定义 x 轴标签等
# ax.set_xlabel('Categories')
ax.set_ylabel('ASR')
# ax.set_title('Comparison between Original Score and Unmatch Score')
ax.set_xticks(x)
ax.set_xticklabels(categories)

# 自动标注 y 轴的百分比格式
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}'))

# 添加每个柱状图上方的值标签
def autolabel(rects):
    """在每个柱状图上显示值标签"""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

# 去除边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

ax.legend(loc='upper center', bbox_to_anchor=(0.4, 1.15),
          ncol=3, fancybox=True, shadow=True)

fig.tight_layout()

plt.show()

plt.savefig( 'ASR.png')