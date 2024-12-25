import pandas as pd

df = pd.read_excel('ygc_cost.xlsx', index_col=None, header=None, sheet_name='ygc_cost')

# print(df)
#
column_names = df.columns.values
print(column_names)
# data = df['cost_time'].values

# 读取单列
print(df.iloc[:, 0])