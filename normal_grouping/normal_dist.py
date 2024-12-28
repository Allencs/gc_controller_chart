import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt

# 假设data是你的数据集
# data = np.random.normal(loc=5.0, scale=2.0, size=1000)  # 生成一个正态分布的数据集
df = pd.read_excel('ygc_cost.xlsx', index_col=None, header=None, sheet_name='ygc_cost')
data = df.iloc[:, 0]

# 使用scipy.stats.norm.fit来拟合正态分布
(mu, sigma) = norm.fit(data)

# 创建正态分布的PDF
pdf = norm.pdf(np.arange(min(data), max(data)), mu, sigma)

# 绘制直方图
plt.hist(data, bins=30, density=True, alpha=0.5, label='Data')

# 绘制正态分布曲线
plt.plot(np.arange(min(data), max(data)), pdf, 'r--', label='Fitted normal distribution')

plt.title('Normal Distribution Fitted to Data')
plt.legend()
plt.show()
