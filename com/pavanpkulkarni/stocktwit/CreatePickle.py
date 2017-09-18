import nltk
import random
#from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
from pprint import pprint
import json

#Change the paths 
TEST_DATA_FILENAME = "/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/data_set/test_data.json" 
BEARISH_TRAIN_DATA_FILENAME = "/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/data_set/bearish_train_data_.json" 
BULLISH_TRAIN_DATA_FILENAME = "/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/data_set/bullish_train_data_.json"

names = ["AAPL", "MMM", "AXP", "T", "BA", "CAT", "CVX", "CSCO", "KO", "DIS", "DD", "XOM", "GE", "GS", "HD", "IBM", "INTL", "JNJ", "JPM", "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UTX", "UNH", "VZ", "V", "WMT", "NVS", "TM", "PTR", "WFC", "BABA",  "TWTR", "FB", "GOOG", "AAPL", "YHOO", "BP", "PEP"]


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf
    
bullish_pos = json.load(open(BULLISH_TRAIN_DATA_FILENAME))
bearish_neg = json.load(open(BEARISH_TRAIN_DATA_FILENAME))

# move this up here
all_words = []
documents_bull = ""
documents_bear = ""
all_tweets = []      
#  j is adject, r is adverb, and v is verb

#allowed_word_types = ["J","R","V","N"]
allowed_word_types = ["J", "R", "V"]


for i in names:
    for j in range(len(bullish_pos[i])):
        all_tweets.append((bullish_pos[i][j]['body'].encode("ascii", "ignore"), bullish_pos[i][j]['entities']['sentiment']['basic'].encode("ascii", "ignore")))
        words = word_tokenize(bullish_pos[i][j]['body'].encode("ascii", "ignore"))
        pos = nltk.pos_tag(words)
        for w in pos:
            if w[1][0] in allowed_word_types:
                all_words.append(w[0].lower()) 
                       
for i in names:
    for j in range(len(bearish_neg[i])):
        all_tweets.append((bearish_neg[i][j]['body'].encode("ascii", "ignore"), bearish_neg[i][j]['entities']['sentiment']['basic'].encode("ascii", "ignore")))
        words = word_tokenize(bearish_neg[i][j]['body'].encode("ascii", "ignore"))
        pos = nltk.pos_tag(words)
        for w in pos:
            if w[1][0] in allowed_word_types:
                all_words.append(w[0].lower()) 


print "Document lenght is : ", len(all_tweets)
print "all_words length is : ", len(all_words)

print "Started pickling all_tweets"
save_all_tweets = open("/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/all_pickles/all_tweets.pickle","wb")
pickle.dump(all_tweets, save_all_tweets)
save_all_tweets.close()
print "End pickling all_tweets"

all_words = nltk.FreqDist(all_words)
print "Most COmmon 200 Words [FreqDistribution] : ", all_words.most_common(200)

word_features = list(all_words.keys())[:5000]
print "Word Features : ", len(word_features)

print "Started pickling word_feature"
save_word_features = open("/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/all_pickles/word_features.pickle","wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()
print "End pickling word_feature"


def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

featuresets = [(find_features(rev), category) for (rev, category) in all_tweets]

print "Started pickling featuresets"
save_featuresets = open("/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/all_pickles/featuresets.pickle","wb")
pickle.dump(featuresets, save_featuresets)
save_word_features.close()
print "End pickling featuresets"

random.shuffle(featuresets)
print( "Lenght of featuresets : ", len(featuresets))

testing_set = featuresets[:10]
training_set = featuresets[11:]

#http://www.nltk.org/_modules/nltk/classify/naivebayes.html

NaiveBayes_classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(NaiveBayes_classifier, testing_set))*100)
save_classifier = open("/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/all_pickles/NaiveBayes_classifier.pickle","wb")
pickle.dump(NaiveBayes_classifier, save_classifier)
save_classifier.close()

# http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html
# The multinomial Naive Bayes classifier is suitable for classification with discrete features (e.g., word counts for text classification). 
# The multinomial distribution normally requires integer feature counts.

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)
save_classifier = open("/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/all_pickles/MNB_classifier.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

# http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.BernoulliNB.html
# Like MultinomialNB, this classifier is suitable for discrete data. 
# The difference is that while MultinomialNB works with occurrence counts, BernoulliNB is designed for binary/boolean features.

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)
save_classifier = open("/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/all_pickles/BernoulliNB_classifier.pickle","wb")
pickle.dump(BernoulliNB_classifier, save_classifier)
save_classifier.close()

#http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)
save_classifier = open("/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/all_pickles/LogisticRegression_classifier.pickle","wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()

#http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html
# Similar to SVC with parameter kernel=’linear’, but implemented in terms of liblinear rather than libsvm, so it has more flexibility 
# in the choice of penalties and loss functions and should scale better to large numbers of samples

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)
save_classifier = open("/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/all_pickles/LinearSVC_classifier.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()


voted_classifier = VoteClassifier(
                                  NaiveBayes_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier,
                                  LinearSVC_classifier)

print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set))*100)
 
