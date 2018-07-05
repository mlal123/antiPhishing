# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 14:41:33 2018

@author: mangz
"""

import pandas as pd

""" 
def computeTF(wordDict, bow):
    tfDict = {}
    bowCount = len(bow)
    for word, count in wordDict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict

def computeIDF(docList):
    import math
    idfDict = {}
    N = len(docList)
    
    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / float(val))
        
    return idfDict

def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val*idfs[word]
    return tfidf
############################################

docA = "The car is driven on the road"
docB = "We are taking the car on a big journey with the entire family on the road"

bowA = docA.split(" ")
bowB = docB.split(" ")

wordSet = bowA + bowB

wordDictA = dict.fromkeys(wordSet, 0)
wordDictB = dict.fromkeys(wordSet, 0)

for word in bowA:
    wordDictA[word] += 1
    
for word in bowB:
    wordDictB[word] += 1

tfbowA = computeTF(wordDictA, bowA)
tfbowB = computeTF(wordDictB, bowB)

idfs = computeIDF([wordDictA, wordDictB])

#print(idfs)

tfidfBowA = computeTFIDF(tfbowA, idfs)
tfidfBowB = computeTFIDF(tfbowB, idfs)
"""

####################################################
docA = "The car is driven on the road"
docB = "We are taking the car on a big journey with the entire family on the road"

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words='english', analyzer = 'word', ngram_range = (1,2))
response = vectorizer.fit_transform([docA, docB])

feature_names = vectorizer.get_feature_names()
idf = vectorizer.idf_
for col in response.nonzero()[1]:
    print (feature_names[col], ' - ', response[0, col])

#################################################################
    
url = 'https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv'
sms = pd.read_table(url, header=None, names=['label', 'message'])