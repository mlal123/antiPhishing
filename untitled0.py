# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 17:13:45 2018

@author: mangz
"""

class NBClassifier:
    trainPositive = []
    trainNegative = []
    
    def __init__(self): 
 
    def train(self, trainData):
        total = 0
        numPhish = 0
        for (email, label) in trainData:
            if label == 'spam':
                numPhish += 1
            total += 1
            self.processEmail(email, label)
        self.pA = numPhish / float(total)
        self.pNotA = (total - numPhish) / float(total)
    
    def processEmail(self, body, label):
        for word in body:
            if label == 'spam':
                trainPositive[word] = trainPositive.get(word, 0) + 1
                self.positiveTotal += 1
            else:
                trainNegative[word] = trainNegative.get(word, 0) + 1
                self.negativeTotal += 1
                
    def conditionalWord(self, word, spam):
        alpha = 1
        if spam:
            return (trainPositive.get(word, 0) + alpha) / float(positiveTotal + alpha*numWords)