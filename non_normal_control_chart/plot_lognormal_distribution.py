import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import lognorm
import seaborn as sns


def plot_lognormal_distribution(data):
    """
    绘制数据的对数正态分布图，包括直方图和拟合的概率密度函数
    """
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置

    # 检查数据是否为正数（对数正态分布要求数据必须为正）
    if np.any(data <= 0):
        raise ValueError("数据中存在非正数，无法拟合对数正态分布！")

    # 对数正态分布拟合
    shape, loc, scale = lognorm.fit(data, floc=0)  # 通过拟合确定参数

    # 理论对数正态分布
    x = np.linspace(min(data), max(data), 1000)
    print(min(data), max(data))
    pdf = lognorm.pdf(x, shape, loc, scale)  # 概率密度函数

    # 可视化
    plt.figure(figsize=(10, 6))

    # 绘制实际数据直方图
    sns.histplot(data, bins=30, kde=False, color='skyblue', stat='density', label='数据直方图')

    # 绘制拟合的对数正态分布
    plt.plot(x, pdf, 'r-', lw=2, label=f'对数正态拟合\n(shape={shape:.2f}, scale={scale:.2f})')

    # 图形修饰
    plt.title('对数正态分布拟合', fontsize=14)
    plt.xlabel('数据值', fontsize=12)
    plt.ylabel('概率密度', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(alpha=0.3)
    plt.show()


# 示例使用
if __name__ == "__main__":
    # 生成对数正态分布数据（示例）
    np.random.seed(42)
    # data = np.random.lognormal(mean=1, sigma=0.5, size=1000)

    df = pd.read_excel('ygc_cost.xlsx', index_col=None, header=None, sheet_name='ygc_cost')
    data = df.iloc[:, 0]

    # 绘制对数正态分布图
    plot_lognormal_distribution(data)
