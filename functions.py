## principal functions and objects file

# clear sections are shown in comments
# go to docstrings for function purpose and arguments

import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import requests as req
load_dotenv()
import time


from sklearn.cluster import KMeans
import scipy.cluster.hierarchy as shc

import matplotlib.pyplot as plt
import seaborn as sns


import requests as req
from dotenv import load_dotenv
load_dotenv()
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("darkgrid")

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import nltk
import string

from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer, PorterStemmer
import re
tokenizer = RegexpTokenizer(r'\b\w{3,}\b')
stop_words = list(set(stopwords.words("english")))
stop_words += list(string.punctuation)
import bs4
from bs4 import BeautifulSoup
from nltk.util import ngrams
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

import warnings
import sqlalchemy
from sqlalchemy import create_engine

import wordcloud



#################################CLEANING#####################################
def preprocess_data(string):
    """As a precautionary measure we should try to remove any emails or websites that BS4 missed"""
    new_str = re.sub(r"\S+@\S+", '', string)
    new_str = re.sub(r"\S+.co\S+", '', new_str)
    new_str = re.sub(r"\S+.ed\S+", '', new_str)
    new_str_tok = tokenizer.tokenize(new_str)
    new_str_lemm = [lemmy.lemmatize(token) for token in new_str_tok]
    new_str_cont = ''
    for tok in new_str_lemm:
        new_str_cont += tok + ' '
    return new_str_cont

def gen_stopwords(additional_sw = ['data', 'experience', 'learning', 'science', 'machine', 'work', 'company', 'role', 'the', 'skills', ' data', '000', "data", "the", 'join', 'you']):
    new_stop_words = stop_words
    for sw in additional_sw:
        new_stop_words.append(sw)
    new_stop_words = list(set(new_stop_words))
    return new_stop_words


#################################API-REQUESTS#####################################



class APICaller:
    def __init__(self, base_url, token=None, ignore_token=False):
        self.token = os.getenv('TOKEN')
        if ignore_token==False:
            if len(self.token) == 0:
                raise ValueError('Missing API token!')
        self.base_url=base_url
        
    def retrieve_one(self,url_extension,location=None, date=None, date1=None):  
        if date1!=None:
            response = req.get(self.base_url+url_extension+f'{location}/StartDate={date}/EndDate={date1}/Json').json()
        elif (date!=None and date1==None):
            response = req.get(self.base_url+url_extension+f'{location}/Date={date}/Json').json()
        else:
            print(self.base_url+url_extension)
            response = req.get(self.base_url+url_extension).json()
        return response
    
    
    def retrieve_many(self,location_list, date_list, var, limit):
        data = []
        counter=0
        for location in location_list:
            for date in date_list:
                if counter==limit-1:
                    time.sleep(60)
                response = req.get(f'{self.url}/{key}/{location}/{date}/{var}').json()
                data.append(response)
                counter+=1
        data_df = pd.read_json(data)    
        return data_df



#################################SCRAPING#####################################


#################################TEXT MINING#####################################


def get_salary(dom, parser = 'html', regex_pattern_salary = ['£[0-9]*[,]*[0-9]+[ ]+[a]+'], 
               regex_pattern_interval=['£[0-9]*[,]*[0-9]+[ ]+[a]*[ ]+year', 
                                       '£[0-9]*[,]*[0-9]+[ ]+[a]*[ ]+month', 
                                       '£[0-9]*[,]*[0-9]+[ ]+[a]*[ ]+week',
                                       '£[0-9]*[,]*[0-9]+[ ]+[a]*[ ]+day',
                                       '£[0-9]*[,]*[0-9]+[ ]+[an]*[ ]+hour'],
              ):
    """Function that should be applied across the elements of a column in a pandas dataframe. 
    Parses a webpages html code using BeautifulSoup and a specified parser, after which it tries to identify
    salary mentions using regex. If multiple pattern occurrences are found, the function will return the 
    mean of the first two, based on the assumption that the web page would feature a string similar to :
     - Salary range: £25,000 - £32,000
     Args:
     dom - block of html code
     parser - (str) parser that BeautifulSoup should use, e.g. 'html' (default) or 'lxml'
     regex_pattern_salary - (list of str) lis of patterns for regex to use for retrieving the numerical data
     regex_pattern_interval - (list of str) list of patterns for regex to use for determining if the salary is
                            per year, per week, per month.
     
     Returns a TUPLE:
     salaries_final - (int) a single value of salary
     salary_period - (str) for what time period the salary is declared for: Y - per year; 
                         M - per month, H - per hour, W - per week, D - per day
     """
    dom = str(dom)
    soup = BeautifulSoup(dom, parser)
    # BS4 used to parse the dom and just retrieve the text, eliminating any html tags
    soup_str = soup.get_text()
    for regex_pattern in regex_pattern_salary:
        # iterating over the text using the numerical patterns to find salary mentions
        salary_tokenizer = RegexpTokenizer(regex_pattern)
        salaries = salary_tokenizer.tokenize(soup_str)
        # if we get several occurrences, we take the first two mentions only
        if len(salaries)>1:
            salaries_lst = [salaries[0], salaries[1]]
            # removing pound sympol, letters and any commas
            salaries_clean = [re.sub('£', '', salary) for salary in salaries_lst]
            salaries_clean = [re.sub('[a-zA-Z]', '', salary) for salary in salaries_clean]
            salaries_clean = [int(re.sub(',', '', salary)) for salary in salaries_clean]
            # final salary is the mean of the first two occurrences
            salaries_final = np.mean([salaries_clean[0], salaries_clean[1]])
        # if there's only 1 occurence we just take that one
        elif len(salaries)==1:
            salary_clean = re.sub('£', '', salaries[0])
            salary_clean = re.sub('[a-zA-Z]', '', salary_clean)           
            salary_clean = int(re.sub(',', '', salary_clean))
            salary_clean = int(salary_clean)
            salaries_final = salary_clean
        else:
            # for ease of dataframe manipulation down the line
            # posts with no detectable job are left with a NaN
            salaries_final = np.NaN
    
    for regex_pattern in regex_pattern_interval:
        # now iterating over the regex patterns in the interval list
        # trying to suss out if the mentioned salary is per year/month/week
        # break is added after each if partially for efficiency but also 
        # because of not wanting a latter interval str occurence to 
        # overwrite the original, e.g. if the post gives a per month salary first then
        # later repeats in weeks, but the function's stored salary numeric value is the 
        # one given in months, we want to avoid treating it as if in months
        interval_tokenizer = RegexpTokenizer(regex_pattern)
        intervals = interval_tokenizer.tokenize(soup_str)
        if (type(intervals)==list) and (len(intervals)>1):
            salary_interval = intervals[0]
#             print('INTERVAL', salary_interval)
            break
        elif type(intervals)==str:
            salary_interval = intervals
#             print('INTERVAL', salary_interval)
            break
        else:
            salary_interval = ''
            continue
        
    if (salary_interval!=''):    
        if 'month' in salary_interval:
            salaries_final_adjusted = salaries_final/159
#             print('SALARY PER MONTH is', salaries_final)
            salary_period = 'M'
        elif 'week' in salary_interval:
            salaries_final_adjusted =  salaries_final/36.5
#             print('SALARY PER MONTH is', salaries_final)
            salary_period = 'W'
        elif 'year' in salary_interval:
            salaries_final_adjusted = salaries_final/1898
#             print('SALARY PER YEAR is', salaries_final)
            salary_period = 'Y'
        elif 'day' in salary_interval:
            salaries_final_adjusted = salaries_final/7.3
#             print('SALARY PER DAY')
            salary_period = 'D'
        elif 'hour' in salary_interval:
            salaries_final_adjusted = salaries_final
#             print('SALARY PER HOUR')
            salary_period = 'H'
        else:
#             print('salary stated for interval that is not comprehended - not reliable long-term data')
            salaries_final = np.NaN
            salart_period = np.NaN
            salaries_final_adjusted = np.NaN
    else:
        salary_period = np.NaN
        salaries_final_adjusted = np.NaN
    
    return salaries_final, salaries_final_adjusted, salary_period





#################################DATA TRANSFORMATION#####################################
def get_num_reviews(text, regex_pattern = '[0-9]*[,]*[0-9]* review[s]*'):
    """Function that should be applied across the elements of a column in a pandas dataframe. 
    Goes through the text trying to find a pattern for the number of reviews left using regex. 
    An occurrence of 0 will just return a nan
     Args:
     text - (str) input text
     regex_pattern - (str) pattern for regex to use for retrieving data
     
     Returns :
     num_review - a single
     """
    text = str(text)
    
    reviews = re.findall(regex_pattern, text)
    if reviews==[]:
        num_review_int= np.NaN
    else:
        num_review = reviews[-1]
        num_review_clean = re.sub(',', '', num_review)
        num_review_int = int(re.sub('review[s]*', '', num_review_clean))
    return num_review_int




#################################EDA#####################################

def plot_freqdist_from_series(pd_series, tokenizer_obj, stop_words_list, 
                              title = 'Term Frequency distribution', num_terms=20, 
                              figsize = (10,10), ngram_number=1, lower_case=True):
    """Function that takes in a Pandas Series or column of a DataFrame and plots the Frequency Distribution
    of termns within that list of documents.
    Args:
    pd_series - either a standalone Pandas Series object or a dataframe column, e.g. df.job_description
    tokenizer_obj - (obj) a tokenizer object, normally of the NLTK variety
    num_terms - (int) how many of the top terms to plot on the Freq Dist, default 20
    stop_words - (list of str) list of stop words to exclude from final corpus
    figsize - (tuple of 2 integers) size of matplotlib plot, default is (10,10)
    ngram_numer - (int) what size ngrams to use, expects 1, 2 or 3. Default is 1.
                Values outside that list will just return the default. 
    lower_case - (bool) whether to return all words lowercased or not
    
    
    Plot of the Frequency Distribution of the words in the corpus, using NLTK's built in FreqDist function.

    Returns:
    f_dist_dict - (dict) unigram / bigrams as keys; frequency as value
    """
    all_text_lst = []
    for string in pd_series.tolist():
        output_txt = ''
        tokenized_str = tokenizer_obj.tokenize(string)
        for word in tokenized_str:
            if word.lower() not in stop_words_list:
                if lower_case:
#                     all_text += word.lower() + ' '   
                    output_txt += word.lower() + ' '
                else:
#                     all_text += word + ' '  
                    output_txt += word + ' '
        ngram_list = list(nltk.ngrams(output_txt.split(' ')[:-1], n=ngram_number))
        for ngram in ngram_list:
            all_text_lst.append(ngram)
    
    f_dist = FreqDist(all_text_lst)

    f_dist_dict = dict(f_dist)
    
    plt.figure(figsize=figsize)
    plt.title(title)
    f_dist.plot(num_terms)
    plt.show();

    return f_dist_dict

def gen_cloud(data, max_words_num, 
              background_color = 'black', height = 300, 
              randomstate=42, fig_size=(12,12),
             cloud_title='Word Cloud'):
    cloud = wordcloud.WordCloud(max_words=max_words_num, background_color=background_color, height=height, random_state=randomstate)
    plt.figure(figsize=fig_size)
    cloud.generate(' '.join(data))
    plt.imshow(cloud)
    plt.title(cloud_title)
    plt.axis("off")
    plt.show();




#################################SUMMARY TABLES CREATION#####################################



#############################MODEL BUILDING, GRIDSEARCH AND PIPELINES#####################################


#############################MODEL EVALUATION (METZ, ROC CURVE, CONF_MAT)#####################################

