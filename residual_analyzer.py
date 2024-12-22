import numpy as np

class ResidualAnalyzer:
    def calculate_residuals(self, observed: np.ndarray, predicted: np.ndarray) -> np.ndarray:
        """
        计算残差

        参数:
        - observed: 观测值
        - predicted: 预测值

        返回:
        残差数组
        """
        return observed - predicted

    def normalize_residuals(self, residuals: np.ndarray) -> np.ndarray:
        """
        标准化残差

        参数:
        - residuals: 残差数组

        返回:
        标准化后的残差
        """
        return (residuals - np.mean(residuals)) / np.std(residuals)