"""
Functionality for scraping WSJ's news archive to get 
headlines and summaries.
"""

# load libraries and variables
import datetime
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd

from config import base_url, headline_class, webdriver_wait_time

# define functions
def get_sd_url(current_date):
	"""
	Get the URL for a single date.

	Args:
		current_date (datetime.date): date to build string off of
	Returns:
		URL string
	"""
	current_date_formatted = '{}{}{}'.format(current_date.strftime('%Y'), 
											 current_date.strftime('%m'),
											 current_date.strftime('%d'))
	URL = '{}{}'.format(base_url, current_date_formatted)
	return URL

def get_wsj_articles_sd(current_date, logging = False):
	"""
	Get WSJ article headlines and summaries for a single date.

	Args:
		current_date (datetime.date): date to grab articles from
	Returns:
		pandas DataFrame with fields:
			published_date | headline | summary
	"""
	# get URL, load page, extract main section
	URL = get_sd_url(current_date)
	driver = webdriver.Chrome()
	driver.get(URL)
	WebDriverWait(driver, webdriver_wait_time)
	if logging:
		print(driver.title)
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	main_sections = soup.find_all('main', id = 'main', role = 'main')

	# extract article headlines and summaries;
	# note we use a loop over main_sections just in
	# case, but it should only show up once
	headlines = []
	summaries = []
	for main_sec in main_sections:
		# get articles
		articles = main_sec.find_all('article')
		for article in articles:
			# get headline
			# NOTE - should replace this with regex in case the string at the end changes
			# re.compile('.*listing-col-.*')
			headline = article.find('div', class_ = headline_class)
			headlines.append(headline.getText())
		
			# get summary
			summary = article.find('p')
			summaries.append(summary.getText())

	# close page, put article info into dataframe and return
	driver.close()
	article_dat = pd.DataFrame({'published_date': current_date, 'headline': headlines, 'summary': summaries})
	return(article_dat)

def get_wsj_articles(start_date, end_date, logging = False):
	"""
	Get WSJ article headlines and summaries for supplied
	date range.

	Args:
		start_date (datetime.date): earliest date to get articles
		end_date (datetime.date): most recent date to get articles
	Returns
		pandas DataFrame with fields:
			published_date | headline | summary
	"""
	# loop through dates, adding data to list of DataFrames
	wsj_articles = []
	current_date = start_date
	one_day = datetime.timedelta(days = 1)
	while(current_date <= end_date):
		# get date's articles, iterate
		cd_articles = get_wsj_articles_sd(current_date, logging)
		wsj_articles.append(cd_articles)
		current_date += one_day

	# combine DataFrames into one and return
	wsj_articles = pd.concat(wsj_articles)
	return(wsj_articles)

# example usage
if __name__ == '__main__':
	# set variables
	start_time = time.time()
	start_date = datetime.date(2020, 4, 26)
	end_date = datetime.date(2020, 4, 28)

	# build table and print
	print(get_wsj_articles(start_date, end_date, logging = True))
	elapsed_time = round((time.time() - start_time) / 60, 2)
	print('------- Runtime: {} minutes -------'.format(elapsed_time))
