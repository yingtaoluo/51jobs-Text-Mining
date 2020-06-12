# -*- coding: UTF-8 -*-
import numpy as np
import random
import xlwt
import xlrd

def calcuDistance(vec1, vec2):
    # 计算向量vec1和向量vec2之间的欧氏距离
    return np.sqrt(np.sum(np.square(vec1 - vec2)))

def loadDataSet(inFile):
    # 载入数据测试数据集
    # 数据由文本保存，为二维坐标
    dataSet = []                     # vector 保存向量
    with open(inFile, encoding='UTF-8') as f:
        lines = f.readlines()
        data_length = lines.__len__()
        # print(lines[0])  # 先把 文件的第一行读取，第一行是向量模版
        for i in range(0, data_length):
            items = [float(i) for i in lines[i].replace('[', '').replace(']', '').split(",")]
            dataSet.append(items)

    return dataSet

def initCentroids(dataSet, k):
    # 初始化k个质心，随机获取
    return random.sample(dataSet, k)  # 从dataSet中随机获取k个数据项返回

def minDistance(dataSet, centroidList):
    # 对每个属于dataSet的item，计算item与centroidList中k个质心的欧式距离，找出距离最小的，
    # 并将item加入相应的簇类中

    clusterDict = dict()    # 用dict来保存簇类结果
    clusterIndex = dict()   # 用另一个dict来保存序号
    for index in range(dataSet.__len__()):
        vec1 = np.array(dataSet[index])  # 转换成array形式
        flag = 0  # 簇分类标记，记录与相应簇距离最近的那个簇
        minDis = float("inf")  # 初始化为最大值

        for i in range(len(centroidList)):
            vec2 = np.array(centroidList[i])
            distance = calcuDistance(vec1, vec2)  # 计算相应的欧式距离
            if distance < minDis:
                minDis = distance
                flag = i  # 循环结束时，flag保存的是与当前item距离最近的那个簇标记

        if flag not in clusterDict.keys():  # 簇标记不存在，进行初始化
            clusterDict[flag] = list()
            clusterIndex[flag] = list()

        clusterDict[flag].append(dataSet[index])  # 加入相应的类别中
        clusterIndex[flag].append(index)

    return (clusterIndex, clusterDict) # 返回新的聚类结果


def getCentroids(clusterDict):
    # 得到k个质心
    centroidList = list()
    for key in clusterDict.keys():
        centroid = np.mean(np.array(clusterDict[key]), axis=0)  # 计算每列的均值，即找到质心
        centroidList.append(centroid)

    return np.array(centroidList).tolist()

def getVar(clusterDict, centroidList):
    # 计算簇集合间的均方误差
    # 将簇类中各个向量与质心的距离进行累加求和

    sum = 0.0
    for key in clusterDict.keys():
        vec1 = np.array(centroidList[key])
        distance = 0.0
        for item in clusterDict[key]:
            vec2 = np.array(item)
            distance += calcuDistance(vec1, vec2)
        sum += distance

    return sum


if __name__ == '__main__':

    inFile = "canopy_tfidf_target.txt"  # 数据集文件
    dataSet = loadDataSet(inFile)  # 载入数据集


    centroidList = initCentroids(dataSet,155 )  # 初始化质心，设置k
    (clusterIndex, clusterDict) = minDistance(dataSet, centroidList)  # 第一次聚类迭代
    newVar = getVar(clusterDict, centroidList)  # 获得均方误差值，通过新旧均方误差来获得迭代终止条件

    oldVar = newVar-0.1  # 旧均方误差值初始化为-0.1
    print('***** 第1次迭代 *****')

    for key in clusterDict.keys():

        k = 2
        print('k个均值向量: ', centroidList)
        print('平均均方误差: ', newVar)
                                             # 该参数需要学生根据结果自行调整，不同的结果集参数是不一样的
        while abs(newVar - oldVar) >= 0.001:  # 当连续两次聚类结果小于0.001时，迭代结束,即迭代终止条件
            centroidList = getCentroids(clusterDict)  # 获得新的质心
            (clusterIndex, clusterDict) = minDistance(dataSet, centroidList)  # 新的聚类结果

            oldVar = newVar
            newVar = getVar(clusterDict, centroidList)

            print('***** 第%d次迭代 *****' % k)
            print('k个均值向量: ', centroidList)
            print( '平均均方误差: ', newVar)
            k += 1


    # 以下为 读取结果 然后把对应的数据放入不同的文件中
    # 打开源文件
    input_path = 'qianchengwuyou.xlsx'
    data = xlrd.open_workbook(input_path)
    table = data.sheets()[0]


    for key in clusterIndex.keys():

        # #新建一个excel文件
        target_file = xlwt.Workbook()
        target_table = target_file.add_sheet('target', cell_overwrite_ok=True)

        clusterItemList = clusterIndex[key]
        Listlength = clusterItemList.__len__()
        print('该类一共有 %d 个' % Listlength)
        # print(clusterItemList)
        for index in range(Listlength):
            for i in range(11):                                  # 读取到另一个文件里面
                    target_table.write(index,i,table.row_values(clusterItemList[index])[i])

        target_file.save('K-meansResult\\第%d类.xls' % (key+1))
    print('聚类完成')
