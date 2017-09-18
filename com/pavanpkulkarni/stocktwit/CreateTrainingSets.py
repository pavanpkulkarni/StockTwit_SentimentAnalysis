'''
Created on Sep 6, 2017

@author: pavan
'''

import urllib2
import json
import datetime
from pprint import pprint
from nltk.tokenize import word_tokenize
import nltk
import random


TEST_DATA_FILENAME = "/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/data_set/test_data.json" 
BEARISH_TRAIN_DATA_FILENAME = "/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/data_set/bearish_train_data_.json" 
BULLISH_TRAIN_DATA_FILENAME = "/Users/pavan/Documents/workspace_hu/StockTwit_Analysis/data_set/bullish_train_data_.json"

names = ["AAPL", "MMM", "AXP", "T", "BA", "CAT", "CVX", "CSCO", "KO", "DIS", "DD", "XOM", "GE", "GS", "HD", "IBM", "INTL", "JNJ", "JPM", "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UTX", "UNH", "VZ", "V", "WMT", "NVS", "TM", "PTR", "WFC", "BABA",  "TWTR", "FB", "GOOG", "AAPL", "YHOO", "BP", "PEP","CTSH"]


def get_tweets(ticker):
    url = "https://api.stocktwits.com/api/2/streams/symbol/{0}.json".format(ticker)
    connection = urllib2.urlopen(url)
    data = connection.read()
    connection.close()
    return json.loads(data)

def get_tweets_list_for_test(tickers):
    ret = {}
    for ticker in tickers:
        print "Getting data for", ticker
        try:
            data = get_tweets(ticker)
            symbol = data['symbol']['symbol']
            msgs = []
            for i in range(len(data['messages'])):
                if data['messages'][i]['entities']['sentiment'] is None:
                    msgs.append(data['messages'][i])
            ret.update({symbol : msgs})
        except Exception as e:
            print e
            print "Error getting", ticker
    return ret


def get_tweets_list_for_train_bullish(tickers):
    ret = {}
    for ticker in tickers:
        print "Getting data for", ticker
        try:
            data = get_tweets(ticker)
            symbol = data['symbol']['symbol']
            msgs = []
            for i in range(len(data['messages'])):
                if data['messages'][i]['entities']['sentiment'] is not None:
                    if data['messages'][i]['entities']['sentiment']['basic'] == 'Bullish':
                        msgs.append(data['messages'][i])
            
            ret.update({symbol : msgs})
        except Exception as e:
            print e
            print "Error getting", ticker
    return ret


def get_tweets_list_for_train_bearish(tickers):
    ret = {}
    for ticker in tickers:
        print "Getting data for", ticker
        try:
            data = get_tweets(ticker)
            symbol = data['symbol']['symbol']
            msgs = []
            for i in range(len(data['messages'])):
                if data['messages'][i]['entities']['sentiment'] is not None:    
                    if data['messages'][i]['entities']['sentiment']['basic'] == 'Bearish':
                        msgs.append(data['messages'][i])
            
            ret.update({symbol : msgs})
        except Exception as e:
            print e
            print "Error getting", ticker
    return ret

# schema for original and msgs: ticker (key) : msgs (value, list)
def append(original, msgs):
    print "Appending tweets"
    for ticker in msgs.keys():
        if ticker not in original.keys():
            original[ticker] = msgs[ticker]
        else:
            for msg in msgs[ticker]:
                if msg not in original[ticker]:  # check for duplicates
                    original[ticker].append(msg)
    return original

def read_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def write_file(filename, d):
    with open(filename, 'w+') as f:
        print "Dumping DATA to", filename
        json.dump(d, f)

if __name__ == "__main__":

    # Generate Test Data Set
    old_test = read_file(TEST_DATA_FILENAME)
    new_test = get_tweets_list_for_test(names)
    #print "Test Data Set : ", json.dumps(new_test)
    new_test = append(old_test, new_test)
    write_file(TEST_DATA_FILENAME, new_test)
  
    # Generate Train Data Set for Bearish
    old_bear_train = read_file(BEARISH_TRAIN_DATA_FILENAME)
    new_bear_train = get_tweets_list_for_train_bearish(names)
    #print " Bearish Train Data Set : ", json.dumps(new_bear_train)
    new_bear_train = append(old_bear_train, new_bear_train)
    write_file(BEARISH_TRAIN_DATA_FILENAME, new_bear_train)   
    
    # Generate Train Data Set for Bullish
    old_bull_train = read_file(BULLISH_TRAIN_DATA_FILENAME)
    new_bull_train = get_tweets_list_for_train_bullish(names)
    #print " Bullish Train Data Set : ", json.dumps(new_bull_train)
    new_bull_train = append(old_bull_train, new_bull_train)
    write_file(BULLISH_TRAIN_DATA_FILENAME, new_bull_train) 