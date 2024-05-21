import pandas as pd

# 读取 CSV 文件，不包括标题
file_path = r'C:\Users\17662\Desktop\校内\大二下\1-第十五届服创大赛参赛手册、赛题手册等系列材料\训练数据\【东软集团A08】医保特征数据16000（修订版）.csv'
data = pd.read_csv(file_path)

# 随机抽取2000行数据
sampled_data = data.sample(n=2000, random_state=42)

# 保存到原来的文件夹里面
output_file_path = r'C:\Users\17662\Desktop\校内\大二下\1-第十五届服创大赛参赛手册、赛题手册等系列材料\训练数据\test-2000.csv'
sampled_data.to_csv(output_file_path, index=False)

print(f'抽取的2000行数据已保存到 {output_file_path}')
