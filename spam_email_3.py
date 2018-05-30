import nltk
import os
import random
from collections import Counter
from nltk import NaiveBayesClassifier, classify
from nltk import word_tokenize, WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

stoplist = stopwords.words('english')
classifier = None

def init_lists(folder):
    #function to open folder and create list of emails
	a_list = []
	file_list = os.listdir(folder)
	for a_file in file_list:
		f = open(folder + a_file, encoding="Latin-1")
		a_list.append(f.read())
	f.close()
	return a_list

def preprocess(sentence):
    #need to normalize the data
    #returns result of preprocessing operations
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(sentence)
    return [lemmatizer.lemmatize(word.lower()) for word in tokens]


def get_features(text, setting):
    if setting == 'bow':
        return {word: count for word, count in Counter(preprocess(text)).items() if not word in stoplist}
    else:
        return {word: True for word in preprocess(text) if not word in stoplist}

def train(features, samples_proportion):
    #train data
    train_size = int(len(features) * samples_proportion)
    train_set, test_set = features[:train_size], features[train_size:]
    #print('Training set _size = ' + str(len(train_set)) + ' emails')
   # print('Test size = ' + str(len(test_set)) + ' emails')
    
    classifier = NaiveBayesClassifier.train(train_set)
    return train_set, test_set, classifier

def evaluate(train_set, test_set, classifier):
   print ('Accuracy on the training set = ' + str(classify.accuracy(classifier, train_set)))
   print ('Accuracy of the test set = ' + str(classify.accuracy(classifier, test_set)))
   
    #shows the top # most informative words in classifying spam or not
   classifier.show_most_informative_features(20)

def process_message(message, lower_case = True, stem = True, stop_words = True, gram = 2):
    if lower_case:
        message = message.lower()
    words = word_tokenize(message)
    words = [w for w in words if len(w) > 2]
    if gram > 1:
        w = []
        for i in range(len(words) - gram + 1):
            w += [' '.join(words[i:i + gram])]
        return w
    if stop_words:
        sw = stopwords.words('english')
        words = [word for word in words if word not in sw]
    if stem:
        stemmer = PorterStemmer()
        words = [stemmer.stem(word) for word in words]   
    return words

def spam_or_ham(text, classifier):
    
    email_body = get_features(text, 'bow')
    print(email_body)
    nb = classifier.classify(email_body)
    return nb

def getClassifier():
    return classifier

    
