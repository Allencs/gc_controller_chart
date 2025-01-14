import pandas as pd
import matplotlib.pyplot as plt
# 设置中文
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('CO₂ emissions per dollar of GDP.csv')
df.head()

# 筛选Year列为2000到2023的数据
df = df[df['Year'].between(2000, 2023)]
# 删除Code列为空的值
df = df[df['Code'].notna()]
df['人均二氧化碳排放量'] = df['Annual CO₂ emissions'] / df['Population (historical)']


# 通过df生成每个国家每年的Annual CO₂ emissions
grouped_df2 = df.pivot(index='Year', columns='Code', values='Annual CO₂ emissions')
print(grouped_df2)


plt.figure(figsize=(10,6))
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
plt.plot(grouped_df2.index,grouped_df2['OWID_WRL'])
plt.title('世界二氧化碳排放趋势')
plt.xlabel('年份')
plt.ylabel('二氧化碳排放量')
plt.xticks(grouped_df2.index,rotation=45)
plt.show()