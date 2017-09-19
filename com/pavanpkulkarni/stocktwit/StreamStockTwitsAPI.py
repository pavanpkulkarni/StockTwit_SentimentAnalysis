
import json
import SentimentModule as s


names = ["AAPL", "MMM", "AXP", "T", "BA", "CAT", "CVX", "CSCO", "KO", "DIS", "DD", "XOM", "GE", "GS", "HD", "IBM", "INTL", "JNJ", "JPM", "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UTX", "UNH", "VZ", "V", "WMT", "NVS", "TM", "PTR", "WFC", "BABA",  "TWTR", "FB", "GOOG", "AAPL", "YHOO", "BP", "PEP","CTSH"]


TEST_DATA_FILENAME = "/Users/pavan/Documents/workspace_hu/StockTwit_SentimentAnalysis/data_set/test_data.json" 

test_data = json.load(open(TEST_DATA_FILENAME))


for i in names:
    for j in range(len(test_data[i])):
        tweet = test_data[i][j]['body'].encode("ascii", "ignore")
        sentiment_value, confidence = s.sentiment(tweet)
        print(tweet, sentiment_value, confidence)