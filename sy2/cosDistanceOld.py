# -*- coding: utf-8 -*-
import numpy as np

input_path = 'tfidf_target.txt'
output_path = 'distance_target.txt'

#计算两个向量之间的距离的函数
def getCosDistance(vector1,vector2):
    num = np.sum(vector1 * vector2.T)
    denom = (np.linalg.norm(vector1) * np.linalg.norm(vector2))  # 计算范式,也即两个向量之间的余弦相似度
    return num / denom

vector = []                       # vector 保存向量
with open(input_path, encoding='UTF-8') as f:
    lines = f.readlines()
    data_length = lines.__len__()

    print(lines[0])    # 先把 文件的第一行读取，第一行是向量模版
    for i in range(1,data_length):
        items = [float(i) for i in lines[i].replace('[','').replace(']','').split(",")]
        vector.append(items)

data_length = data_length - 1   # 去掉第一行
output_file = open(output_path,'w',encoding='UTF-8')  # 新建一个输出文件用于保存结果

for i in range(data_length):
    dis = [0.0 for m in range(0,data_length)]
    for index in range(i,data_length):                       # 以右下三角形式计算
        if index == i:
            dis[index] = 0
            continue
        dis[index] = getCosDistance(vector[i],vector[index])
    print(i)
    output_file.write(str(dis[i:data_length])+"\n")            # 在此直接保存到txt文件中，节省内存

output_file.close()
print("计算完成！")



