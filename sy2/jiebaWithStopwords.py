# -*- coding: utf-8 -*-
# python结巴分词使用停用词版本，根据输入的excel文件分词后输出到另一个excel中

import xlrd
import xlwt
import jieba

input_path = 'qianchengwuyou.xlsx'          # 输入文件
output_path = 'ansj_target.xls'         # 输出文件

jieba.load_userdict('userwords.txt')  # userwords.txt 为文件类对象或自定义词典

# 读取停用词文件
with open('stopwords.txt', encoding='UTF-8') as f:
    stoplist = f.readlines()                        # 读取所有的数据到 list 中
    for i in range(stoplist.__len__()):
        stoplist[i] = stoplist[i].strip('\n')    #去掉换行符

f.close()

data = xlrd.open_workbook(input_path)
table = data.sheets()[0]  # 读取excel文件的第一张表
nrows = table.nrows       # 行数

# #新建一个excel文件
target_file = xlwt.Workbook()
target_table = target_file.add_sheet('target',cell_overwrite_ok=True)

#下面进行分词处理，并去除停用词
for index in range(nrows):
    segs = jieba.lcut(table.row_values(index)[5])   # 对第四列进行jieba分词处理
    segs = [word for word in list(segs) if word not in stoplist]    # 去除在停用词中的词语
    target_table.write(index, 0, ','.join(segs))    # 把结果写入到文件中

target_file.save(output_path)