import pandas as pd
import math

#https://www.youtube.com/watch?v=hXNbFNCgPfY

'''
tf(w) = Number of times the word appears in a document/Total number of words in a document

idf(w) = log(Total Number of documents/Number of documents that contains word w)

The tfidf score of a word, w is  tf(w) * idf(w)
'''
def computeTF(wordDict, doc):
    tfDict = {}
    bow = doc.split(" ")
    bowCount = len(bow)
    for word, count in wordDict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict

def computeIDF(docList):
    idfDict = {}
    N = len(docList)

    #counts the number of document tht contain a word w
    idfDict = dict.fromkeys(docList[0].keys(), 0)
    print("1. compute idf")
    print(idfDict)
    print("2")
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1

    #divide N by denominator above, take the log of that
    for word, val in idfDict.items():
        idfDict[word] = math.log(N/float(val))

    return idfDict

def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val * idfs[word]
    return tfidf

def convertToDic(wordSet, docA, docB):
    #create dictionaries to keep word count
    wordDictA = dict.fromkeys(wordSet, 0)
    #print(wordDictA)
    wordDictB = dict.fromkeys(wordSet, 0)
    #print(wordDictB)
    #count the words in bags
    bowA = docA.split(" ")
    bowB = docB.split(" ")
    for word in bowA:
        wordDictA[word] += 1
    for word in bowB:
        wordDictB[word] += 1

    df = pd.DataFrame([wordDictA, wordDictB])

    print(df.to_string())

    return wordDictA, wordDictB

def combine_docs(docA, docB):
    bowA = docA.split(" ")
    bowB = docB. split(" ")

    wordSet = set(bowA).union(set(bowB))

    return wordSet

if __name__ == '__main__':
    docA = "The cat sat on my face"
    docB = "The dog sat on my bed"

    wordSet = combine_docs(docA, docB)
    wordDictA, wordDictB = convertToDic(wordSet, docA, docB)

    tfBowA = computeTF(wordDictA, docA)
    print(tfBowA)

    tfBowB = computeTF(wordDictB, docB)
    print(tfBowB)

    idfs = computeIDF([wordDictA, wordDictB])

    print(idfs)

    tfidfBowA = computeTFIDF(tfBowA, idfs)
    print(tfidfBowA)
    tfidfBowB = computeTFIDF(tfBowB, idfs)
    print(tfidfBowB)

    '''Above tfidfBowA, tfidfBowB will be printed in pandas dataframe'''

    df = pd.DataFrame([tfidfBowA, tfidfBowB])

    print(df.to_string())