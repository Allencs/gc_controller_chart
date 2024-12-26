import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import seaborn as sns


class NonNormalControlChart:
    def __init__(self, data, subgroup_size):
        self.data = np.array(data)
        self.subgroup_size = subgroup_size
        self.num_subgroups = len(data) // subgroup_size
        self.subgroups = self._create_subgroups()

    def _create_subgroups(self):
        """
        将数据划分为子组
        """
        return [
                   self.data[i:i + self.subgroup_size]
                   for i in range(0, len(self.data), self.subgroup_size)
               ][:self.num_subgroups]

    def calculate_subgroup_stats(self):
        """
        计算每个子组的均值和标准差
        """
        subgroup_means = [np.mean(subgroup) for subgroup in self.subgroups]
        subgroup_stds = [np.std(subgroup, ddof=1) for subgroup in self.subgroups]
        return np.array(subgroup_means), np.array(subgroup_stds)

    def fit_distribution(self):
        """
        拟合分布，返回拟合参数和分布类型
        """
        # 尝试对数正态分布
        params = stats.lognorm.fit(self.data)
        return params, stats.lognorm

    def calculate_control_limits(self, subgroup_stats, dist_params, dist):
        """
        计算控制限（基于非正态分布拟合）
        """
        subgroup_means, subgroup_stds = subgroup_stats

        # 中心线
        mean_CL = np.mean(subgroup_means)
        std_CL = np.mean(subgroup_stds)

        # 模拟控制限（95%上下分位数）
        mean_UCL = dist.ppf(0.975, *dist_params)
        mean_LCL = dist.ppf(0.025, *dist_params)
        std_UCL = dist.ppf(0.975, *dist_params)  # 标准差控制限
        std_LCL = dist.ppf(0.025, *dist_params)

        return {
            'mean_CL': mean_CL, 'mean_UCL': mean_UCL, 'mean_LCL': mean_LCL,
            'std_CL': std_CL, 'std_UCL': std_UCL, 'std_LCL': std_LCL
        }

    def plot_control_chart(self):
        """
        绘制控制图
        """
        subgroup_means, subgroup_stds = self.calculate_subgroup_stats()
        dist_params, dist = self.fit_distribution()
        limits = self.calculate_control_limits((subgroup_means, subgroup_stds), dist_params, dist)

        # 绘制均值控制图
        plt.figure(figsize=(12, 8))

        plt.subplot(2, 1, 1)
        plt.plot(subgroup_means, marker='o', linestyle='-', label='子组均值')
        plt.axhline(limits['mean_CL'], color='blue', linestyle='--', label='中心线 (CL)')
        plt.axhline(limits['mean_UCL'], color='red', linestyle='--', label='上控制限 (UCL)')
        plt.axhline(limits['mean_LCL'], color='red', linestyle='--', label='下控制限 (LCL)')
        plt.title('均值控制图 (非正态分布)')
        plt.xlabel('子组编号')
        plt.ylabel('均值')
        plt.legend()

        # 绘制标准差控制图
        plt.subplot(2, 1, 2)
        plt.plot(subgroup_stds, marker='o', linestyle='-', color='green', label='子组标准差')
        plt.axhline(limits['std_CL'], color='blue', linestyle='--', label='中心线 (CL)')
        plt.axhline(limits['std_UCL'], color='red', linestyle='--', label='上控制限 (UCL)')
        plt.axhline(limits['std_LCL'], color='red', linestyle='--', label='下控制限 (LCL)')
        plt.title('标准差控制图 (非正态分布)')
        plt.xlabel('子组编号')
        plt.ylabel('标准差')
        plt.legend()

        plt.tight_layout()
        plt.show()


# 示例使用
if __name__ == "__main__":
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置

    # 生成非正态分布数据（例如对数正态分布）
    # data = np.random.lognormal(mean=1, sigma=0.5, size=100)
    df = pd.read_excel('ygc_cost.xlsx', index_col=None, header=None, sheet_name='ygc_cost')
    data = list(df.iloc[:, 0])

    subgroup_size = 5  # 子组大小

    # 创建控制图对象
    control_chart = NonNormalControlChart(data, subgroup_size)

    # 绘制控制图
    control_chart.plot_control_chart()
