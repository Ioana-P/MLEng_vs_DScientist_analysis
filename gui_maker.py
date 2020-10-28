import numpy as np
import time
# import requests as req
# from dotenv import load_dotenv
# load_dotenv()
import selenium as sl
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

# import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set_style("darkgrid")
# import string

# from nltk.corpus import stopwords
# from nltk.tokenize import RegexpTokenizer
# import re
# tokenizer = RegexpTokenizer(r'\b\w{3,}\b')
# stop_words = list(set(stopwords.words("english")))
# stop_words += list(string.punctuation)

from functions import JobPostScraper


import PySimpleGUI as sg 
import os.path
import pandas as pd 
import sqlalchemy as db
# import seaborn as sns
# import matplotlib.pyplot as plt




intro_layout = [[sg.Text("Welcome to the Indeed Job Post Scraper"), sg.Text(size=(40,1))],
                 [sg.Button("Scrape"), sg.Text(size=(15, 1), enable_events=True, key="-SCRAPE-"),
                 ], 
                 [sg.Button("Retrieve"), sg.Text(size=(15,1), enable_events=True, key="-RETRIEVE-")
                 ],
                 [sg.Button("Close")]
                 ]

scrape_layout = [[sg.Text("Scrape job data", (20,3)), sg.Text(size=(40,1))],
                [sg.Text("Search term", (20,1)), sg.In(size=(30,1), enable_events=True, key='-SEARCH-TERM-')],
                [sg.Text("Location", (20,1)), sg.In('London', size=(30,1), enable_events=True, key='-SEARCH-LOCATION-')],
                [sg.Text("Website URL", (20,1)), sg.In('https://www.indeed.co.uk', (30,1), enable_events=True, key='-ROOT-URL-')],                # [sg.Button("Go back"), sg.Text(size=(10,1), enable_events=True, key="-GO-BACK-")],
                [sg.Text("How many jobs?", (20,1)), sg.In('10', (5,1), enable_events=True, key='-NUM-JOBS-')],
                [sg.Text("Save as (filename)", (20,1)), sg.In('scraped_jobs_data', (30,1), enable_events=True, key='-FILENAME-')],
                [sg.Button("SCRAPE")],
                [sg.Button("Close")]
                ]

retrieve_layout = [[sg.Text("Retrieve job data"), sg.Text(size=(40,1))],
                # [sg.Text("Get data from jobs that have previously been scraped and stored"), sg.Text(10,2)],
                [sg.Text("Job title", (20,1)), sg.In(size=(15,1), enable_events=True, key='-JOB-TITLE-')],
                [sg.Text("Organisation name", (20,1)), sg.In(size=(15,1), enable_events=True, key='-ORG-NAME-')],
                [
                sg.Frame('Categories', layout=[ 
                        [sg.Text('What to select: ')],
                        [sg.Checkbox('Job description', default=False,key='-DESCR-')],
                        [sg.Checkbox('Salary',default=True,key='-SALARY-')],
                        [sg.Radio('Data Scientist',0, default=False, key='-Searched-DS-')],
                        [sg.Radio('Data Analyst', 0,default=False, key='-Searched-DA-')],
                        [sg.Radio('ML Engineer', 0,default=False, key='-Searched-ME-')]
                ]
                )
                ],
                [sg.Button("Specify salary time period"), sg.Text(size=(20,1), enable_events=True, key="-GO-RETRIEVE-")],
                # [sg.Button("Go back"), sg.Text(size=(10,1), enable_events=True, key="-GO-BACK-")],
                [sg.Button("Close")]
                ]

time_period_layout = [[sg.Text("What declared time period for salary data do you wish to access?"), sg.Text(size=(30,1))],
                     [sg.Frame('Time period', layout=[
                         [sg.Radio('Annual', 1, default=True, key='-YEARLY-')],
                         [sg.Radio('Monthly', 1, default=False, key='-MONTHLY-')],
                         [sg.Radio('Daily', 1, default=False, key='-DAILY-')]
                         ])],
                    [sg.Button("Go retrieve!"), sg.Text(size=(20,1), enable_events=True, key="-GO-RETRIEVE-")]
                     ]


intro_window = sg.Window("IndeedScraper", intro_layout)
scrape_window = sg.Window("Scrape indeed", scrape_layout)
retrieve_window = sg.Window("Retrieve", retrieve_layout)
time_period_window = sg.Window("Time Period", time_period_layout)

search_dict = {'search_Job_title': '',
                'search_Org_name': '',
                'search_DA':False,
                'search_DS':True,
                'search_ME':False,
                'salary_period':'Y',
                'get_Job_description': False,
                'get_Job_salary': True}
scrape_dict = {'search_term':'',
                'location':'London',
                'root_url':'https://www.indeed.co.uk',
                'num_jobs':10,
                'file_name':'scraped_jobs_data'}

current_window = intro_window

while True:
    event, values = current_window.read()
    #end program if user closes window or
    #presses the OK button
    if event == "Close" or event == sg.WIN_CLOSED:
        break
    elif event =="Scrape":
        current_window.close()
        current_window = scrape_window
    elif event =='SCRAPE':
        print("Still in build")
        #assigning values into the scrape dict with the inputs
        scrape_dict['root_url']= values['-ROOT-URL-']
        scrape_dict['search_term']= values['-SEARCH-TERM-']
        scrape_dict['location']= values['-SEARCH-LOCATION-']
        scrape_dict['num_jobs']= int(values['-NUM-JOBS-'])
        #calling webscraper from functions.py
        job_scraper = JobPostScraper(scrape_dict['root_url'], 
                                    scrape_dict['search_term'],
                                    scrape_dict['location'], 
                                    scrape_dict['num_jobs'])

        job_url_df = job_scraper.get_job_link_urls()
        job_scraper.get_job_text_html(job_url_df, headless=False)
        new_jobs_df = job_scraper.get_jobs_df()
        current_time = time.asctime().replace(' ', '_')
        filename = scrape_dict['file_name']+current_time
        new_jobs_df.to_csv(f'{filename}.csv', columns = new_jobs_df.columns)
        print("Scraping job done!")
        break
    elif event =="Retrieve":
        print("Getting stored data")
        engine = db.create_engine('sqlite:///preprocessing_nb/scraped_jobs.sqlite')
        connection = engine.connect()
        current_window.close()
        current_window = retrieve_window
    elif event=='Specify salary time period':
        search_dict['search_Job_title'] = values['-JOB-TITLE-']
        search_dict['search_Org_name'] = values['-ORG-NAME-']
        search_dict['get_Job_salary'] = values['-SALARY-']
        search_dict['get_Job_description'] = values['-DESCR-']
        search_dict['search_DS'] = values['-Searched-DS-']
        search_dict['search_DA'] = values['-Searched-DA-']
        search_dict['search_ME'] = values['-Searched-ME-']
        current_window.close()
        current_window = time_period_window
    elif event =="Go retrieve!":
        if values['-YEARLY-']==True:
            search_dict['salary_period'] = 'Y'
        elif values['-MONTHLY-']==True:
            search_dict['salary_period'] = 'M'
        elif values['-DAILY-']==True:
            search_dict['salary_period'] = 'D'    

        table = pd.read_sql_query(f"""
                            SELECT s.Job_Id, Job_Name, Org_Name, Salary
                            FROM salaries s JOIN job_search j ON s.Job_Id == j.Job_Id 
                            JOIN salary_period p on s.Job_Id == p.Job_Id
                            WHERE (Salary IS NOT NULL AND 
                                   j.Searched_data_scientist == {search_dict['search_DS']} AND
                                   j.Searched_data_analyst == {search_dict['search_DA']} AND
                                   j.Searched_machine_learning_engineer == {search_dict['search_ME']} AND
                                   p.Salary_Time_Period == '{search_dict['salary_period']}') 
                            LIMIT 10
                             """, connection)
        if search_dict['search_Job_title'] != '':
            title_search = search_dict['search_Job_title']
            cur_table = table.loc[table.Job_Name.str.contains(f'(?<![\w\d]){title_search}(?![\w\d])')]
        else:
            cur_table = table

        if search_dict['search_Org_name'] != '':
            org_search = search_dict['search_Org_name']
            cur_table = cur_table.loc[table.Org_Name.str.contains(f'(?<![\w\d]){org_search}(?![\w\d])')]
        
        pd.set_option('display.expand_frame_repr', False)
        print(cur_table)
        # sns.distplot(cur_table.Salary.values, bins=10, kde=False)
        # plt.show()
    # elif event=="Go back":
    #     current_window = intro_window
        

current_window.close()
