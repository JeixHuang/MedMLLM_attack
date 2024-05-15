import matplotlib.pyplot as plt
from med2med_linear import plot_scatter_with_bias as plot_med2med
from med2na_linear import plot_data_by_label as plot_med2na
from na2med_linear import plot_scatter_with_bias as plot_na2med
from na2na_linear import plot_labeled_scatter as plot_na2na
from med2med_linear import add_circles as circle1
from med2na_linear import add_circles as circle2
from na2med_linear import add_circles as circle3
from na2na_linear import add_circles as circle4
from med2med_linear import print_scores as score1
from med2na_linear import print_scores as score2
from na2med_linear import print_scores as score3
from na2na_linear import print_scores as score4

def main():
    # 设置图形大小和子图布局，分为上下两排，每排四个图
    fig, axs = plt.subplots(2, 4, figsize=(20, 10), gridspec_kw={'wspace': 0.1, 'hspace': 0.1})
    axs = axs.flatten()  # 将 axs 数组扁平化

    # 定义每个绘图函数对应的文件夹路径
    folder_paths = [
        '../metric/img2text_results',  # 适当调整路径
        '../metric/metric/med2na_nature_img2text',
        '../metric/na2med_img2text_results',
        '../metric/metric/na2na_nature_img2text'
    ]

    # 将绘图函数和圆圈函数存储在列表中
    plot_functions = [plot_med2med, plot_med2na, plot_na2med, plot_na2na]
    circle_functions = [circle1, circle2, circle3, circle4]
    score_functions = [score1, score2, score3, score4]

    # # 循环遍历 axs、绘图函数列表和路径，上排绘制点状图，下排绘制圆圈
    for i, (plot_func, circle_func, folder_path) in enumerate(zip(plot_functions, circle_functions, folder_paths)):
        plot_func(axs[i], folder_path)  # 调用绘点状图函数
        circle_func(axs[i + 4], folder_path)  # 调用绘制圆圈的函数，修改以适应实心圆和透明度

    plt.tight_layout()  # 调整布局以防止重叠
    plt.savefig('combined_scatter_plots.png')  # 保存图像
    plt.show()  # 显示图形
    
    # for score_func, folder_path in zip(score_functions, folder_paths):
    #     print(folder_path)
    #     score_func(folder_path)
        

if __name__ == "__main__":
    main()
