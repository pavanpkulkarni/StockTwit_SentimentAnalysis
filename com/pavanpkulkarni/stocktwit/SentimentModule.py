import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize



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

word_features_f = open("/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/all_pickles/word_features.pickle", "rb")
word_features = pickle.load(word_features_f)
word_features_f.close()

open_file = open("/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/all_pickles/NaiveBayes_classifier.pickle", "rb")
NaiveBayes_classifier = pickle.load(open_file)
open_file.close()

open_file = open("/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/all_pickles/MNB_classifier.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open("/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/all_pickles/BernoulliNB_classifier.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open("/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/all_pickles/LogisticRegression_classifier.pickle", "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()

open_file = open("/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/all_pickles/LinearSVC_classifier.pickle", "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()

voted_classifier = VoteClassifier(
                                  NaiveBayes_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier,
                                  LinearSVC_classifier)

def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats), voted_classifier.confidence(feats)

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features
