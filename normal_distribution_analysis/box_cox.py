import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy import stats


plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置

# 1. 数据预处理
def data_preprocessing(data):
    """
    数据预处理

    参数:
    原始数据集

    返回:
    处理后的数据
    """
    # 删除缺失值
    data = data[~np.isnan(data)]

    # 确保数据为正值（Box-Cox变换要求）
    if np.any(data <= 0):
        data = data - np.min(data) + 1

    return data


# 2. Box-Cox变换
def box_cox_transform(data):
    """
    Box-Cox变换

    参数:
    data: 原始数据集

    返回:
    变换后的数据和最优lambda值
    """
    # 数据预处理
    data = data_preprocessing(data)

    # Box-Cox变换
    transformed_data, lambda_param = stats.boxcox(data)

    return transformed_data, lambda_param


# 3. 正态性检验
def normality_test(data, title):
    """
    正态性检验

    参数:
    data: 待检验数据
    title: 检验标题
    """
    # Shapiro-Wilk检验
    statistic, p_value = stats.shapiro(data)

    print(f"{title} Shapiro-Wilk检验结果:")
    print(f"统计量: {statistic}")
    print(f"p值: {p_value}")

    # 判断是否服从正态分布
    alpha = 0.05
    if p_value > alpha:
        print("数据可能服从正态分布")
    else:
        print("数据不服从正态分布")

    return statistic, p_value


# 4. 绘制对比图
def plot_distribution_comparison(original_data, transformed_data, lambda_param):
    """
    绘制原始数据和变换后数据的分布对比图

    参数:
    original_原始数据
    transformed_data: 变换后数据
    lambda_param: Box-Cox变换参数
    """
    # 创建图形
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # 原始数据分布
    ax1.hist(original_data, bins=30, density=True, alpha=0.7, color='skyblue')
    ax1.set_title('原始数据分布')
    ax1.set_xlabel('数值')
    ax1.set_ylabel('频率')

    # 变换后数据分布
    ax2.hist(transformed_data, bins=30, density=True, alpha=0.7, color='lightgreen')
    ax2.set_title(f'Box-Cox变换后分布 (λ={lambda_param:.4f})')
    ax2.set_xlabel('数值')
    ax2.set_ylabel('频率')

    plt.tight_layout()
    plt.show()


# 5. Q-Q图
def plot_qq_comparison(original_data, transformed_data):
    """
    绘制原始数据和变换后数据的Q-Q图

    参数:
    original_原始数据
    transformed_变换后数据
    """
    # 创建图形
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # 原始数据Q-Q图
    stats.probplot(original_data, plot=ax1)
    ax1.set_title('原始数据Q-Q图')

    # 变换后数据Q-Q图
    stats.probplot(transformed_data, plot=ax2)
    ax2.set_title('Box-Cox变换后Q-Q图')

    plt.tight_layout()
    plt.show()


# 6. 主函数
def main(data):
    """
    主函数

    参数:
    data: 原始数据集
    """
    # 原始数据正态性检验
    print("原始数据正态性检验:")
    normality_test(data, "原始数据")

    # Box-Cox变换
    transformed_data, lambda_param = box_cox_transform(data)

    # 变换后数据正态性检验
    print("\n变换后数据正态性检验:")
    normality_test(transformed_data, "变换后数据")

    # 绘制分布对比图
    plot_distribution_comparison(data, transformed_data, lambda_param)

    # 绘制Q-Q图
    plot_qq_comparison(data, transformed_data)

    return transformed_data, lambda_param


# 示例调用
if __name__ == "__main__":
    # 方法1：生成非正态分布数据
    # data = np.random.exponential(scale=2, size=1000)

    # 方法2：从文件读取
    # import pandas as pd
    # data = pd.read_excel('your_data.xlsx')['column_name'].values

    # 方法1：pandas读取
    df = pd.read_excel('ygc_cost.xlsx', sheet_name='ygc_cost', index_col=None, header=None)
    # 方法2：指定具体列
    data = df.iloc[:, 0]

    # 执行主函数
    transformed_data, lambda_param = main(data)
