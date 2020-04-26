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

sns.set_style("darkgrid")

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import nltk
from sklearn.linear_model import LogisticRegression
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.metrics import confusion_matrix, multilabel_confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import train_test_split, GridSearchCV
from matplotlib import cm
import numpy as np
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve
from sklearn.metrics import f1_score
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import silhouette_score
import string

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re
tokenizer = RegexpTokenizer(r'\b\w{3,}\b')
stop_words = list(set(stopwords.words("english")))
stop_words += list(string.punctuation)
# stop_words += ['__', '___']

# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')





#################################CLEANING#####################################




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





#################################DATA TRANSFORMATION#####################################



#################################EDA#####################################



#################################SUMMARY TABLES CREATION#####################################



#############################MODEL BUILDING, GRIDSEARCH AND PIPELINES#####################################


#############################MODEL EVALUATION (METZ, ROC CURVE, CONF_MAT)#####################################

