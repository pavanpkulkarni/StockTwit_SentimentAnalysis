# StockTwit_SentimentAnalysis

### Prerequisites  
1. python 2.7 - [Installation Instruction](https://www.python.org/download/releases/2.7/)
2. git - [Installation Instruction](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)


### To Run :  
1. Clone the repo :   
`git clone https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis.git`
2. You might have to change the locations of TEST_DATA_FILENAME, BEARISH_TRAIN_DATA_FILENAME, BULLISH_TRAIN_DATA_FILENAME.  
3. Run the [TestSentimentModule.py](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/blob/master/com/pavanpkulkarni/stocktwit/TestSentimentModule.py)


### CreateDataSets :  
This module crates 3 data sets and stores them in [data_set](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/tree/master/data_set) :
1. [**test_data.json**](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/blob/master/data_set/test_data.json) - Contains all tweets with no sentiment labels
2. [**bearish_train_data_.json**](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/blob/master/data_set/bearish_train_data_.json) - Contains all tweets with `Bearish` label
3. [**bullish_train_data_.json**](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/blob/master/data_set/bullish_train_data_.json) - Contains all tweets with `Bullish` label

### CreatePickle :
This module does the following:
1. Tokenize, remove stop_words and add POS taggers to all the words from [bearish_train_data_.json](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/blob/master/data_set/bearish_train_data_.json) and [bullish_train_data_.json](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/blob/master/data_set/bullish_train_data_.json)
2. Find features for each token of the text that is passed to the method find_feature()
3. Pickle all the time consuming operations like :  

   1. [**all_tweets.pickle**](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/tree/master/all_pickles) - Contains all the tweets combined from both [bearish_train_data_.json](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/blob/master/data_set/bearish_train_data_.json) and [bullish_train_data_.json](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/blob/master/data_set/bullish_train_data_.json)
   2. [**word_features.pickle**](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/tree/master/all_pickles) - Contains top 5000 words that are stipped off of stop_words and all the POS tagged words 
   3. [**featuresets.pickle**](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/tree/master/all_pickles) - Contains all the words associated with the corresponding features.
   4. [**NaiveBayes_classifier.pickle**](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/tree/master/all_pickles) - Naive Bayes Algorithm. Read more [here](http://www.nltk.org/_modules/nltk/classify/naivebayes.html)  
   5. [**MNB_classifier.pickle**](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/tree/master/all_pickles) - Multinomial Naive Bayes classifier. Read more [here](http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html)  
   6. [**BernoulliNB_classifier.pickle**](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/tree/master/all_pickles) - Bernoulli Naiye Bayes Calssifier. Read more [here](http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.BernoulliNB.html)
   7. [**LogisticRegression_classifier.pickle**](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/tree/master/all_pickles) - Logistic Regression classifier. Read more [here](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)   
   8. [**LinearSVC_classifier.pickle**](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/tree/master/all_pickles) - Linear Support Vector Classification. Read more [here](http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html)  
 

### SentimentModule
This module is the actual running module. We load the pickle and provide the best possible results based on Voting system. 

### StreamStockTwitsAPI
Pass [test.json](https://github.com/pavanpkulkarni/StockTwit_SentimentAnalysis/blob/master/data_set/test_data.json) to get sentiment for each tweet.  

## Architecture Diagram :  


**Overview** :  


<img src="images/StockTwits_Overview.png" width="650" height="300">  



**Detailed Architecture** :  


<img src="images/StockTwits_Detailed_Architecture.png" width="650" height="500">  


