from numpy import *
def loadDataSet(postingList,classVec):
    # classVec #1 代表招聘，0代表大数据
    return postingList,classVec

def createVocabList(dataSet):
    vocabset =set([])
    for document in dataSet:
        vocabset = vocabset | set(document)  # 返回不重复的列表
    return list(vocabset)

def setOfWords2Vec(vocabList ,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word :%s is not in my Vocabulary!" % word)
    return returnVec

def trainNB0(trainMatrix,trainCategory):
    numTrainDocs=len(trainMatrix)
    numWords=len(trainMatrix[0])
    pAbusive=sum(trainCategory)/float(numTrainDocs)
    # 初始化概率 (这里是评分标准第二部分优化要修改的的地方1)
    p0Num = zeros(numWords);p1Num = zeros(numWords)
    p0Denom = 0.0; p1Denom = 0.0
    for i in range(numTrainDocs):
        # 向量相加
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    # 对每个元素做除法 (这里是评分标准第二部分优化要修改的地方2)
    p1Vet = p1Num/p1Denom
    p0Vet = p0Num/p0Denom
    return p0Vet,p1Vet,pAbusive

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
	# (这里是评分标准第二部分优化要修改的地方3)
    p1 = sum(vec2Classify*p1Vec)+pClass1
    p0 = sum(vec2Classify*p0Vec)+1.0-pClass1
    if p1 > p0:
        return 1
    else:
        return 0




