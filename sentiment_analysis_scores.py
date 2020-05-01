"""
Compile sentiment analysis scores for a dataset of news articles.
"""

# load libraries
import datetime

import pandas as pd
# from nltk.corpus import stopwords
# from nltk import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from get_wsj_articles import get_wsj_articles

# set variables
start_date = datetime.date(2020, 4, 28)
end_date = datetime.date(2020, 4, 28)

# download article data
articles = get_wsj_articles(start_date, end_date)
print(articles.dtypes)

# HERE - 

# tokenize, remove stop words, remove punctuation, lower case
# -- does this stuff matter *shrug*

# loop through articles, tagging sentiment
n_articles = len(articles.index)
analyzer = SentimentIntensityAnalyzer()
for i in range(n_articles):
	headline = articles.loc[i]['headline']
	summary = articles.loc[i]['summary']
	headline_score = analyzer.polarity_scores(headline)
	print(i)
	print(headline)
	print(headline_score)
	# print("{:-<65} {}".format(headline, str(headline_score)))
	# print(headline)
	# print(type(headline))
	# print(summary)

