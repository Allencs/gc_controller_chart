from typing import List, Dict, Any
import matplotlib.pyplot as plt
import numpy as np

from residual_analyzer import ResidualAnalyzer


class GCPerformanceAnalyzer:
    def __init__(self, gc_times: List[float]):
        """
        GC性能分析器初始化

        参数:
        - gc_times: GC耗时列表
        """
        self.gc_times = np.array(gc_times)
        self.residual_analyzer = ResidualAnalyzer()

    def calculate_smaller_is_better_control_chart(self) -> Dict[str, Any]:
        """
        计算望小型控制图参数

        返回:
        控制图参数字典
        """
        # 去除高峰期数据
        processed_data = self.remove_peak_data()

        # 计算关键统计指标
        mean = np.mean(processed_data)
        std_dev = np.std(processed_data)

        # 计算控制限
        lcl = max(0, mean - 3 * std_dev)  # 下控制限不小于0
        ucl = mean + 3 * std_dev

        return {
            'mean': mean,
            'std_dev': std_dev,
            'lower_control_limit': lcl,
            'upper_control_limit': ucl,
            'processed_data': processed_data
        }

    def remove_peak_data(self) -> np.ndarray:
        """
        使用残差去除高峰期数据

        返回:
        处理后的数据
        """
        # 拟合趋势线
        # 生成0到观测值个数的整数序列
        x = np.arange(len(self.gc_times))
        # 将 x 和 gc耗时数据点拟合成一个一次多项式，返回的 trend_line 数组将包含拟合出的斜率和截距
        trend_line = np.poly1d(np.polyfit(x, self.gc_times, 1))

        # 计算残差
        residuals = self.residual_analyzer.calculate_residuals(
            self.gc_times,
            trend_line(x)
        )

        # 标准化残差
        normalized_residuals = self.residual_analyzer.normalize_residuals(residuals)

        # 过滤异常点（保留在2个标准差内的点）
        mask = np.abs(normalized_residuals) <= 2
        return self.gc_times[mask]

    def plot_control_chart(self, chart_params: Dict[str, Any]):

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置

        """
        绘制控制图

        参数:
        - chart_params: 控制图参数
        """
        plt.figure(figsize=(12, 6))

        x_value= range(len(self.gc_times))
        y_value= self.gc_times

        # 原始数据点
        plt.scatter(
            x_value,
            y_value,
            linestyle='-',
            label='原始GC耗时',
            alpha=0.5
        )

        # 控制限
        plt.axhline(
            y=chart_params['lower_control_limit'],
            color='r',
            linestyle='--',
            label='下控制限'
        )
        plt.axhline(
            y=chart_params['upper_control_limit'],
            color='r',
            linestyle='--',
            label='上控制限'
        )

        # 平均线
        plt.axhline(
            y=chart_params['mean'],
            color='g',
            linestyle='-',
            label='平均线'
        )

        plt.title('Java GC耗时望小型控制图')
        plt.xlabel('观测序列')
        plt.ylabel('GC耗时(ms)')
        plt.plot(x_value, y_value)
        plt.legend()
        plt.show()

    def performance_evaluation(self, chart_params: Dict[str, Any]) -> str:
        """
        GC性能评估

        参数:
        - chart_params: 控制图参数

        返回:
        性能评级
        """
        # 异常点计算
        out_of_control_points = np.sum(
            (self.gc_times < chart_params['lower_control_limit']) |
            (self.gc_times > chart_params['upper_control_limit'])
        )

        # 异常点比例
        out_of_control_ratio = out_of_control_points / len(self.gc_times)

        # 性能评级
        if out_of_control_ratio < 0.01:
            return "优秀"
        elif out_of_control_ratio < 0.05:
            return "良好"
        elif out_of_control_ratio < 0.1:
            return "可接受"
        else:
            return "需改进"