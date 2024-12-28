import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns


class NormalGrouping:
    def __init__(self, data):
        self.data = np.array(data)
        self.mean = np.mean(self.data)
        self.std = np.std(self.data)

    def normality_test(self):
        """
        正态分布检验
        """
        # Shapiro-Wilk检验
        _, p_value = stats.shapiro(self.data)
        print(f"Shapiro-Wilk检验 p-value: {p_value}")

        # 偏度和峰度
        skewness = stats.skew(self.data)
        kurtosis = stats.kurtosis(self.data)
        print(f"偏度: {skewness}")
        print(f"峰度: {kurtosis}")

        # 可视化正态分布
        self.plot_distribution()

    def plot_distribution(self):
        """
        绘制数据分布图
        """
        plt.figure(figsize=(12, 4))

        # 直方图
        plt.subplot(131)
        sns.histplot(self.data, kde=True)
        plt.title('数据分布直方图')

        # Q-Q图
        plt.subplot(132)
        stats.probplot(self.data, plot=plt)
        plt.title('Q-Q图')

        # 箱线图
        plt.subplot(133)
        sns.boxplot(x=self.data)
        plt.title('箱线图')

        plt.tight_layout()
        plt.show()

    def group_by_standard_deviation(self):
        """
        按标准差进行分组
        """
        groups = {
            '中心区间 (μ ± 1σ)': [],
            '第一区间 (μ ± 2σ)': [],
            '第二区间 (μ ± 3σ)': [],
            '极端区间 (>3σ)': []
        }

        for value in self.data:
            if abs(value - self.mean) <= self.std:
                groups['中心区间 (μ ± 1σ)'].append(value)
            elif abs(value - self.mean) <= 2 * self.std:
                groups['第一区间 (μ ± 2σ)'].append(value)
            elif abs(value - self.mean) <= 3 * self.std:
                groups['第二区间 (μ ± 3σ)'].append(value)
            else:
                groups['极端区间 (>3σ)'].append(value)

        return groups

    def group_percentage(self):
        """
        按百分比分组
        """
        percentiles = {
            '0-50%': [],
            '50-84%': [],
            '84-97%': [],
            '97-100%': []
        }

        for value in self.data:
            z_score = (value - self.mean) / self.std

            if abs(z_score) <= 0.67:
                percentiles['0-50%'].append(value)
            elif abs(z_score) <= 1:
                percentiles['50-84%'].append(value)
            elif abs(z_score) <= 2:
                percentiles['84-97%'].append(value)
            else:
                percentiles['97-100%'].append(value)

        return percentiles

    def print_group_summary(self, groups):
        """
        打印分组汇总
        """
        print("\n分组统计:")
        for group, values in groups.items():
            print(f"{group}:")
            print(f"  数量: {len(values)}")
            print(f"  占比: {len(values) / len(self.data) * 100:.2f}%")
            if values:
                print(f"  最小值: {min(values)}")
                print(f"  最大值: {max(values)}")
            print()

    def visualization_grouping(self, groups):
        """
        分组可视化
        """
        plt.figure(figsize=(10, 6))
        group_names = list(groups.keys())
        group_sizes = [len(values) for values in groups.values()]

        plt.pie(group_sizes, labels=group_names, autopct='%1.1f%%')
        plt.title('数据分组分布')
        plt.show()


# 使用示例
def main():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
    # 模拟数据集
    # data = np.random.normal(100, 15, 1000)
    df = pd.read_excel('ygc_cost.xlsx', index_col=None, header=None, sheet_name='ygc_cost')
    data = df.iloc[:, 0]

    # 创建正态分组对象
    ng = NormalGrouping(data)

    # 正态分布检验
    ng.normality_test()

    # 标准差分组
    std_groups = ng.group_by_standard_deviation()
    ng.print_group_summary(std_groups)
    ng.visualization_grouping(std_groups)

    # 百分比分组
    percentage_groups = ng.group_percentage()
    ng.print_group_summary(percentage_groups)
    ng.visualization_grouping(percentage_groups)


if __name__ == "__main__":
    main()
