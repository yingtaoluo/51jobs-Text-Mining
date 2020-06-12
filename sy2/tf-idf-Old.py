# -*- coding: utf-8 -*-
# 该python文件用于把excel里面的数据读取，并且转换成TF-IDF值
import math
import xlrd
import time

input_path = 'ansj_target.xls'                       # 输入文件
output_path = 'tfidf_target.txt'                     # 输出文件

time_start = time.time()   # 计时开始
data = xlrd.open_workbook(input_path)                   # 打开目标文件，即要进行向量化的文件
table = data.sheets()[0]
nrows = table.nrows                                     # 记录总的数据行数

output_file = open(output_path,'w',encoding='UTF-8')  # 新建一个输出文件用于保存结果

# 计算 基向量模版
base_Vector = set()                                     # 用python的set类型作为基向量，set内容是不可重复的
segments = []

for index in range(nrows):
    segs = table.row_values(index)[0].split(',')
    segments.append(segs)
    base_Vector.update(segs)                            # 为基向量添加元素
base_Vector_list = list(base_Vector)                    # 把set转换成list，使其有序
output_file.write(str(base_Vector_list)+"\n")           # 将结果保存在文件中

base_Vector_length = base_Vector_list.__len__()

# 计算IDF
IDF = [0.0 for i in range(base_Vector_length)]    # 记录IDF值的数组，生成一个长度为 向量模版的list，且所有的元素大小为0.0 浮点型
for i in range(base_Vector_length):
    for index in range(nrows):
        if base_Vector_list[i] in segments[index]:   # 如果存在则加1
            IDF[i] = IDF[i] + 1.0
for index in range(base_Vector_length):
    IDF[index] = math.log10(nrows / IDF[index])


# 计算所有词语的 IDF 值
TF_IDF = []                                                              # 存储所有的TF-IDF值
for index in range(nrows):                                              # 遍历所有的数据行

    vector = [0.0 for i in range(base_Vector_length)]                  # 生成一个空的llist，用于存储TF值
    items = table.row_values(index)[0].split(',')
    items_length = len(items)
    for ele in items:                                                  # 计算 TF
        location = base_Vector_list.index(ele)                          # 找到这个词在模版向量的位置
        vector[location] = vector[location] + 1                         # 然后把这个位置的值加一，代表出现的次数

    for ele in range(base_Vector_length):                               # 计算TF值
        vector[ele] = vector[ele]/items_length

    TF_IDF.append(vector)                                               # 把结果加入到 向量矩阵中

for index1 in range(nrows):                                             # 计算 TF*IDF值，保存在二维数组中
    for index2 in range(base_Vector_length):
        TF_IDF[index1][index2] = TF_IDF[index1][index2] * IDF[index2]
    output_file.write(str(TF_IDF[index1])+"\n")                         # 写入文件
    print('第'+str(index1)+'条数据已写入')

output_file.close()
print("计算完成！")
time_end = time.time()  # 计时结束
print('totally cost',time_end-time_start,'s')



