# -*- coding: utf-8 -*-
# python结巴分词使用停用词版本，根据输入的excel文件分词后输出到另一个excel中
import xlrd
import xlwt
import jieba

def jiebafenci(input_path,output_path):
    jieba.load_userdict('userwords.txt')  # userwords.txt 为文件类对象或自定义词典
    # 读取停用词文件
    with open('stopwords.txt', encoding='UTF-8') as f:
        stoplist = f.readlines()                        # 读取所有的数据到 list 中
        for i in range(stoplist.__len__()):
            stoplist[i] = stoplist[i].strip('\n')    #去掉换行符

        f.close()

    #打开源文件
    data = xlrd.open_workbook(input_path)

    #新建一个excel文件
    target_file = xlwt.Workbook()
    target_table = target_file.add_sheet('target',cell_overwrite_ok=True)

    table = data.sheets()[0]  # 读取excel文件的第一张表
    nrows = table.nrows       # 行数

    #下面进行分词处理，并去除停用词
    for index in range(nrows):
        segs = jieba.lcut(table.row_values(index)[0])   # 对第一列进行jieba分词处理
        segs = [word for word in list(segs) if word not in stoplist]    # 去除在停用词中的词语
        target_table.write(index, 0, ','.join(segs))    # 把结果写入到文件中

    target_file.save(output_path)
#读取分词后的数据
def readExcel(output_path,output_path2):
    postingList =[]
    classVec =[]
    #读取excl文件
    book = xlrd.open_workbook(output_path)
    table = book.sheets()[0]
    nrows = table.nrows
    for index in range(nrows):
        segs = table.row_values(index)[0].split(',')
        postingList.append(segs)
        classVec.append(1)

    book = xlrd.open_workbook(output_path2)
    table = book.sheets()[0]
    nrows = table.nrows
    for index in range(nrows):
        segs = table.row_values(index)[0].split(',')
        postingList.append(segs)
        classVec.append(0)
    return postingList, classVec
#读取test文件
def readTestExcel(input_path):
    postingList = []
    classVec = []
    # 读取excl文件
    book = xlrd.open_workbook(input_path)
    table = book.sheets()[0]
    nrows = table.nrows
    for index in range(nrows):
        segs = table.row_values(index)[0].split(',')
        postingList.append(segs)
    return postingList
