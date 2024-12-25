import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns


class DataDistributionAnalysis:
    def __init__(self, data):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
        self.data = np.array(data)

    # 1. 分布特征分析
    def distribution_characteristics(self):
        """
        分析数据分布基本特征
        """
        characteristics = {
            '样本量': len(self.data),
            '最小值': np.min(self.data),
            '最大值': np.max(self.data),
            '平均值': np.mean(self.data),
            '中位数': np.median(self.data),
            '标准差': np.std(self.data),
            '偏度': stats.skew(self.data),
            '峰度': stats.kurtosis(self.data)
        }

        print("数据分布特征:")
        for key, value in characteristics.items():
            print(f"{key}: {value:.4f}")

        return characteristics

    # 2. 分布类型识别
    def identify_distribution(self):
        """
        识别可能的分布类型
        """
        # 偏度和峰度判断
        skewness = stats.skew(self.data)
        kurtosis = stats.kurtosis(self.data)

        distribution_types = {
            '正态分布': abs(skewness) < 1 and abs(kurtosis) < 1,
            '右偏分布': skewness > 1,
            '左偏分布': skewness < -1,
            '重尾分布': abs(kurtosis) > 1,
            '轻尾分布': abs(kurtosis) < 1
        }

        print("\n分布类型识别:")
        for dist_type, is_match in distribution_types.items():
            if is_match:
                print(f"可能的分布类型: {dist_type}")

        return distribution_types

    # 3. 概率分布拟合
    def distribution_fitting(self):
        """
        常见概率分布拟合
        """
        # 常见分布列表
        distributions = [
            stats.norm,  # 正态分布
            stats.lognorm,  # 对数正态分布
            stats.expon,  # 指数分布
            stats.gamma,  # Gamma分布
            stats.weibull_min  # 威布尔分布
        ]

        # 分布拟合结果
        fitting_results = []

        for dist in distributions:
            # 参数估计
            params = dist.fit(self.data)

            # 拟合优度检验
            _, p_value = stats.kstest(self.data, dist.name, args=params)

            fitting_results.append({
                '分布类型': dist.name,
                'p值': p_value,
                '参数': params
            })

        # 排序并输出
        fitting_results.sort(key=lambda x: x['p值'], reverse=True)

        print("\n概率分布拟合结果:")
        for result in fitting_results:
            print(f"分布类型: {result['分布类型']}, "
                  f"p值: {result['p值']:.4f}")

        return fitting_results

    # 4. 可视化分析
    def visualization_analysis(self):
        """
        数据分布可视化
        """
        plt.figure(figsize=(15, 10))

        # 子图1：直方图
        plt.subplot(2, 2, 1)
        plt.hist(self.data, bins=30, density=True, alpha=0.7)
        plt.title('直方图')
        plt.xlabel('数值')
        plt.ylabel('频率')

        # 子图2：核密度估计
        plt.subplot(2, 2, 2)
        sns.kdeplot(self.data, fill=True)
        plt.title('核密度估计')

        # 子图3：箱线图
        plt.subplot(2, 2, 3)
        plt.boxplot(self.data)
        plt.title('箱线图')

        # 子图4：Q-Q图
        plt.subplot(2, 2, 4)
        stats.probplot(self.data, plot=plt)
        plt.title('Q-Q图')

        plt.tight_layout()
        plt.show()

    # 5. 异常值处理
    def outlier_analysis(self):
        """
        异常值分析与处理
        """
        # IQR方法
        Q1 = np.percentile(self.data, 25)
        Q3 = np.percentile(self.data, 75)
        IQR = Q3 - Q1

        # 异常值判断
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = self.data[(self.data < lower_bound) | (self.data > upper_bound)]

        print("\n异常值分析:")
        print(f"下边界: {lower_bound:.4f}")
        print(f"上边界: {upper_bound:.4f}")
        print(f"异常值数量: {len(outliers)}")
        print("异常值:", outliers)

        return {
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'outliers': outliers
        }


# 使用示例
def main():
    # 生成非正态分布数据
    # data = np.random.exponential(scale=2, size=1000)

    # 方法1：pandas读取
    df = pd.read_excel('ygc_cost.xlsx', sheet_name='ygc_cost', index_col=None, header=None)
    # 方法2：指定具体列
    data = df.iloc[:, 0]

    # 创建分析对象
    analyzer = DataDistributionAnalysis(list(data))

    # 执行分析
    analyzer.distribution_characteristics()
    analyzer.identify_distribution()
    analyzer.distribution_fitting()
    analyzer.visualization_analysis()
    analyzer.outlier_analysis()


if __name__ == "__main__":
    main()
