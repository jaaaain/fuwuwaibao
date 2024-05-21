import pandas as pd

# 读取 CSV 文件
pred_df = pd.read_csv('uploads/test-2000.csv')
actual_df = pd.read_csv(r'C:\Users\17662\Desktop\校内\大二下\1-第十五届服创大赛参赛手册、赛题手册等系列材料\训练数据\test-2000.csv')

# 提取结果列
y_pred = pred_df['RES']
y_true = actual_df['RES']

# 确保两个文件的长度相同
assert len(y_pred) == len(y_true), "两个文件的行数不一致，无法比较。"

#
accuracy = (y_pred == y_true).mean()

print(f'一致率: {accuracy * 100:.2f}%')
