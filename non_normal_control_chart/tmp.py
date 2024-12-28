import pandas as pd
import seaborn as sns


df = pd.read_excel('ygc_cost.xlsx', index_col=None, header=None, sheet_name='ygc_cost')
data = df.iloc[:, 0]

print(min(data), max(data))

#绘制特征的分布图
sns.distplot(data)