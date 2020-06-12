#  coding: utf-8
import bayes2
import jiebaWithStopwords
import xlwt
import xlrd
from numpy import *
import matplotlib .pyplot as plt

# 训练文件并分词
input_path = input(">")+".xls"
output_path = input(">")+".xls"
input_path2 = input(">")+".xls"
output_path2 = input(">")+".xls"

# output_path = "ansj_target.xls"
#
# output_path2 = "crawl_target.xls"

jiebaWithStopwords.jiebafenci(input_path,output_path)
jiebaWithStopwords.jiebafenci(input_path2,output_path2)
# 读取分词后的文件保存在数组中
postingList, classVec = jiebaWithStopwords.readExcel(output_path, output_path2)
listOPosts, listClasses = bayes2.loadDataSet(postingList, classVec)
# 将训练分词的后的转换为数字向量
myVocabList = bayes2.createVocabList(listOPosts)
print("开始训练")
trainMat = []
for postinDoc in listOPosts:
    trainMat.append(bayes2.setOfWords2Vec(myVocabList, postinDoc))
p0v, p1V, pAb = bayes2.trainNB0(array(trainMat), array(listClasses))
print("训练结束")

# 读取需要测试的文件并分词
input_testPath = 'test.xls'
output_testPath = 'test_target.xls'
jiebaWithStopwords.jiebafenci(input_testPath, output_testPath)
testEntity = jiebaWithStopwords.readTestExcel(output_testPath)
source = xlrd.open_workbook(input_testPath)
table = source.sheets()[0]
zhaopianExcl = xlwt.Workbook()
zhaopi_table = zhaopianExcl.add_sheet('target', cell_overwrite_ok=True)
bigdataExcl = xlwt.Workbook()
bigdata_table = bigdataExcl.add_sheet('target', cell_overwrite_ok=True)
k = 0
m = 0
print("测试开始")
for i in range(testEntity.__len__()):
    # 将测试文件转换为数字向量
    thisDoc = array(bayes2.setOfWords2Vec(myVocabList,testEntity[i]))
    classifiedFlag = bayes2.classifyNB(thisDoc,p0v,p1V,pAb);
    if classifiedFlag == 1:
        # 写入招聘文件
        for j in range(2):
            zhaopi_table.write(k, j, table.row_values(i)[j])
        k += 1
    else:
        # 写入大数据文件
        for j in range(2):
            bigdata_table.write(m, j, table.row_values(i)[j])
        m += 1
zhaopianExcl.save('zhaopin.xls')
bigdataExcl.save('bigData.xls')
print("测试完成")
# 画图
labels = 'zhaopin', 'bigData'
sizes = k, m
colors = 'lightgreen', 'gold'
explode = 0.1, 0.05
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct ='%1.1f%%', shadow=True, startangle=50)
plt.axis('equal')
plt.title('Result')
plt.show()

