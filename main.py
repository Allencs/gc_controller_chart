import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from typing import List
from gc_perf_analyzer import GCPerformanceAnalyzer


def simulate_gc_times(n_samples: int = 200) -> List[float]:
    """
    模拟GC耗时数据

    参数:
    - n_samples: 样本数量

    返回:
    模拟的GC耗时列表
    """
    # 基础随机波动
    base_gc_times = np.random.normal(10, 2, n_samples)

    # 模拟周期性波动
    periodic_component = 5 * np.sin(np.arange(n_samples) * 0.1)

    # 模拟高峰期
    peak_periods = np.random.choice(n_samples, 20, replace=False)
    base_gc_times[peak_periods] += np.random.uniform(5, 10, 20)

    return base_gc_times + periodic_component


def main():
    # 模拟GC耗时数据
    gc_times = simulate_gc_times()

    # 创建性能分析器
    analyzer = GCPerformanceAnalyzer(gc_times)

    # 计算控制图参数
    chart_params = analyzer.calculate_smaller_is_better_control_chart()

    # 绘制控制图
    analyzer.plot_control_chart(chart_params)

    # 性能评估
    performance_grade = analyzer.performance_evaluation(chart_params)

    # 输出结果
    print("GC性能统计:")
    print(f"平均GC耗时: {chart_params['mean']:.2f} ms")
    print(f"GC耗时标准差: {chart_params['std_dev']:.2f} ms")
    print(f"下控制限: {chart_params['lower_control_limit']:.2f} ms")
    print(f"上控制限: {chart_params['upper_control_limit']:.2f} ms")
    print(f"性能评级: {performance_grade}")


if __name__ == "__main__":
    # 设置随机数种子
    np.random.seed(1)
    main()
