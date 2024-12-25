import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


# 方法1：pandas读取
df = pd.read_excel('ygc_cost.xlsx', sheet_name='ygc_cost', index_col=None, header=None)
column_names = df.columns.values
# 方法2：指定具体列
data = df.iloc[:, 0]

print(list(data))


def plot_normal_distribution(data):
    # 计算均值和标准差
    mu = np.mean(data)
    sigma = np.std(data)

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置

    # 创建图形
    plt.figure(figsize=(10,6))

    # 直方图
    # plt.hist(data, bins=30, density=True, alpha=0.7, color='skyblue')

    # 正态分布曲线
    xmin, xmax = plt.xlim()
    # print(xmin, xmax)
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, mu, sigma)
    print("x:" + str(data))
    print("p:" + str(p))
    plt.plot(x, p, 'k', linewidth=2)

    # 设置标题和标签
    plt.title('正态分布图')
    plt.xlabel('数值')
    plt.ylabel('频率')

    # 显示图形
    plt.show()


# 3. 正态性检验
def normality_test(data):
    """
    进行正态性检验

    参数:
    原始数据集

    返回:
    检验结果
    """
    # Shapiro-Wilk检验
    statistic, p_value = stats.shapiro(data)

    print("Shapiro-Wilk检验结果:")
    print(f"统计量: {statistic}")
    print(f"p值: {p_value}")

    # 判断是否服从正态分布
    alpha = 0.05
    if p_value > alpha:
        print("数据可能服从正态分布")
    else:
        print("数据不服从正态分布")

    return statistic, p_value


if __name__ == '__main__':
    # 调用函数
    plot_normal_distribution(list(data))
    # print(normality_test(list(data)))


