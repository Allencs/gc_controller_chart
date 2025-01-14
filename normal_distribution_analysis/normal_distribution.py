import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

from normal_distribution_analysis.box_cox import box_cox_transform
from residual_analyzer import ResidualAnalyzer

# 方法1：pandas读取
df = pd.read_excel('ygc_cost.xlsx', sheet_name='ygc_cost', index_col=None, header=None)
column_names = df.columns.values
# 方法2：指定具体列
data = df.iloc[:, 0]

residual_analyzer = ResidualAnalyzer()
# print(list(data))


def plot_normal_distribution(data):
    # 计算均值和标准差
    mu = np.mean(data)
    sigma = np.std(data)

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置

    # 创建图形
    plt.figure(figsize=(10, 6))

    # 直方图
    # plt.hist(data, bins=30, density=True, alpha=0.7, color='skyblue')

    # 正态分布曲线(生成x轴，范围-> 最大值～最小值)
    xmin, xmax = plt.xlim(min(data), max(data))
    print(xmin, xmax)
    x = np.linspace(xmin, xmax, 100)
    # x = np.arange(min(data), max(data))
    p = stats.norm.pdf(x, mu, sigma)
    # print("x:" + str(data))
    # print("p:" + str(p))
    plt.plot(x, p, 'k', linewidth=2)

    # 设置标题和标签
    plt.title('正态分布图')
    plt.xlabel('数值')
    plt.ylabel('频率')

    # 显示图形
    plt.show()


def remove_peak_data(data) -> np.ndarray:
    """
    使用残差去除高峰期数据

    返回:
    处理后的数据
    """
    # 拟合趋势线
    # 生成0到观测值个数的整数序列
    x = np.arange(len(data))
    # 将 x 和 gc耗时数据点拟合成一个一次多项式，返回的 trend_line 数组将包含拟合出的斜率和截距
    trend_line = np.poly1d(np.polyfit(x, data, 1))

    # 计算残差
    residuals = residual_analyzer.calculate_residuals(
        data,
        trend_line(x)
    )

    # 标准化残差
    normalized_residuals = residual_analyzer.normalize_residuals(residuals)

    # 过滤异常点（保留在2个标准差内的点）
    mask = np.abs(normalized_residuals) <= 2
    return data[mask]


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
    target_data = remove_peak_data(data)
    transformed_data, lambda_param = box_cox_transform(target_data)
    print("最佳的Box-Cox变换参数: " + str(lambda_param))
    # 调用函数
    plot_normal_distribution(transformed_data)
    # print(normality_test(transformed_data))
