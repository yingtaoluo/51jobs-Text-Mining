# -*- coding: utf-8 -*-
import random
import xlwt
import xlrd
import jieba
import math
import numpy as np
# 简化版 canopy 只用一个阈值T
input_path = 'qianchengwuyou.xlsx'

# 计算两个向量之间的余弦相似度的函数
def getCosDistance(vector1, vector2):
    num = np.sum(vector1 * vector2.T)
    denom = (np.linalg.norm(vector1) * np.linalg.norm(vector2))  # 计算范式,也即两个向量之间的余弦相似度
    return num/denom

# 加载用户词典
jieba.load_userdict('userwords.txt')  # userwords.txt 为文件类对象或自定义词典
print('完成用户词典加载')
# 读取停用词文件
with open('stopwords.txt', encoding='UTF-8') as f:
    stoplist = f.readlines()                        # 读取所有的数据到 list 中
    for i in range(stoplist.__len__()):
        stoplist[i] = stoplist[i].strip('\n')    #去掉换行符
f.close()
print('完成停用词表加载')

# 分词处理
data = xlrd.open_workbook(input_path)   # 打开源文件
ansjResult = []           # 存储分词结果
table = data.sheets()[0]  # 读取excel文件的第一张表
nrows = table.nrows       # 行数
for index in range(nrows):
    segs = jieba.lcut(table.row_values(index)[1])  # 对第二列进行jieba分词处理
    segs = [word for word in list(segs) if word not in stoplist]  # 去除在停用词中的词语
    ansjResult.append(segs)
print('完成分词过程')

# 计算tf-idf值
# 计算 基向量模版
base_Vector = set()                                     # 用python的sets类型作为基向量，set内容是不可重复的
for index in range(nrows):
    base_Vector.update(ansjResult[index])                            # 为基向量批量添加元素
base_Vector_list = list(base_Vector)                    # 把set转换成list，使其有序

#计算所有词语的 IDF 值
base_Vector_length = base_Vector_list.__len__()
base_Vector_IDf = [0.0 for i in range(base_Vector_length)]              # 生成一个长度为 向量模版的list，且所有的元素大小为0.0 浮点型
TF_IDF =  []                                                              # 存储所有的TF-IDF值

for index in range(nrows):                                              # 遍历所有的数据行

    vector = [0.0 for i in range(base_Vector_length)]                  # 生成一个空的list，用于存储TF值
    items = ansjResult[index]
    items_length = items.__len__()
    for ele in items:                                                  # 计算 TF
        location = base_Vector_list.index(ele)                          # 找到这个词在模版向量的位置
        vector[location] = vector[location] + 1                         # 然后把这个位置的值加1，代表出现的次数

    items = set(items)                                                  # 把列表转换成set从而去掉重复元素
    for ele in items:
        location = base_Vector_list.index(ele)
        base_Vector_IDf[location] = base_Vector_IDf[location] + 1       # 在此把出现过的词的IDF值加1

    for i in range(base_Vector_length):                                # 计算TF值
        vector[i] = vector[i]/items_length

    TF_IDF.append(vector)

for index in range(base_Vector_length):                                 # 最后的每个词语的 IDF值
    base_Vector_IDf[index] = math.log10( nrows / base_Vector_IDf[index])

for index1 in range(nrows):                                             # 计算 TF*IDF值，保存在二维数组中
    for index2 in range(base_Vector_length):
        TF_IDF[index1][index2] = TF_IDF[index1][index2] * base_Vector_IDf[index2]

print('完成TF_IDF计算过程')

# 此处为非必须代码
# 在此保存一下计算得到的TF-IDF值，为下一个K-means实验节省时间
output_file = open('canopy_tfidf_target.txt','w',encoding='UTF-8')  # 新建一个输出文件用于保存结果
for index in range(nrows):
    output_file.write(str(TF_IDF[index]) + "\n")
output_file.close()

# 计算余弦复杂度
TF_IDF_Vector = np.array(TF_IDF)                # 转换成numpy数组,也即转换成向量
AllDisance = []                                 # 存储余弦相似度的矩阵
for i in range(nrows):                         # 初始化一个二维数组用于存储不同向量之间的相似度
    item = [0.0 for i in range(nrows)]
    AllDisance.append(item)

for i in range(nrows):
    for index in range(i, nrows):  # 计算余弦相似度
        if index == i:
            AllDisance[i][i] = 1.0     # 自己跟自己的相似距离为1
            continue
        AllDisance[i][index] = getCosDistance(TF_IDF_Vector[i], TF_IDF_Vector[index])
        AllDisance[index][i] = AllDisance[i][index]
print(AllDisance)
print('完成余弦复杂度计算过程')


average_distance = 0.0   # 从平均余弦相似度中选取平均值作为阈值

for item in AllDisance:
    average_distance = average_distance + sum(item)
count = nrows * nrows
T = (average_distance/count) * 0.35  # 阈值是 余弦相似度的平均值，自己可以设置，如果阈值小导致聚类数目过小，阈值大导致聚类数目过大






# 聚类初始化 变量
dataIndex = [i for i in range(nrows)]    # 元素集合
clusterDict = dict()                     # 用dict来保存簇类结果
clusterCount = 0                         # 保存类的数目

# 聚类初始化 一个点
index = random.randint(0, dataIndex.__len__() - 1)
clusterDict[clusterCount] = [index]  # 随机选取一个元素作为第一个类,然后作为列表加入到聚类集合中
dataIndex.remove(dataIndex[index])    # 在元素集合中删除该元素
clusterCount = clusterCount + 1
print('完成canopy聚类初始化过程')

while dataIndex.__len__() > 0:
    a = random.randint(0, dataIndex.__len__() - 1)  # 从剩下的元素中随机取一个
    item = dataIndex[a]
    setFlag = 0       # 设置标志位，用于确定该元素是否被归类过
    for i in range(clusterDict.__len__()):
        cluList = clusterDict[i]
        Class_Average_distance = 0.0
        ClassSum = 0
        for j in cluList:
            Class_Average_distance = Class_Average_distance + AllDisance[a][j]
            ClassSum = ClassSum + 1
        Average_distance2Class = Class_Average_distance / ClassSum    # 求得item元素到这个类所有元素的平均相似距离
        if Average_distance2Class > T:                               # 若平均距离大于阈值，则将该元素加入该类
            clusterDict[i].append(item)
            setFlag = setFlag + 1


    if setFlag == 0:#如果没有被归类过，就将该点归为一类
        clusterDict[clusterCount] = [item]
        clusterCount = clusterCount + 1

    if dataIndex.count(item) > 0:
        dataIndex.remove(item)                               # 最后 在集合中删除该元素

print("一共有 %d 类" % (clusterCount))
print('完成canopy聚类过程')
# 以下为 读取结果 然后把对应的数据放入不同的文件中
for key in clusterDict.keys():
    # #新建一个excel文件
    target_file = xlwt.Workbook()
    target_table = target_file.add_sheet('target', cell_overwrite_ok=True)
    clusterItemList = clusterDict[key]
    Listlength = clusterItemList.__len__()
    for index in range(Listlength):
        for i in range(11):  # 读取到另一个文件里面
                target_table.write(index, i, table.row_values(clusterItemList[index])[i])
    target_file.save('CanopyResult\\第%d类.xls' % (key + 1))
print('完成canopy文件写入化过程')
print('算法结束')
