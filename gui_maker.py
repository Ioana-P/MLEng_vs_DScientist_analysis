# import pandas as pd
# import numpy as np
# import os
# import time
# import requests as req
# from dotenv import load_dotenv
# load_dotenv()
# import selenium as sl
# from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
# from selenium import webdriver
# from bs4 import BeautifulSoup
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium import webdriver 
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec
# from selenium.webdriver.common.action_chains import ActionChains

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

# from functions import JobPostScraper


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

intro_window = sg.Window("IndeedScraper", intro_layout)


retrieve_layout = [[sg.Text("Retrieve job data"), sg.Text(size=(40,1))],
                # [sg.Text("Get data from jobs that have previously been scraped and stored"), sg.Text(10,2)],
                [sg.Text("Job title"), sg.In(size=(15,1), enable_events=True, key='-JOB-TITLE-')],
                [sg.Text("Organisation name"), sg.In(size=(15,1), enable_events=True, key='-ORG-NAME-')],
                [
                sg.Frame('Categories', layout=[ 
                        [sg.Text('What to select: ')],
                        [sg.Checkbox('Job description', default=False,key='-DESCR-')],
                        [sg.Checkbox('Salary', default=True,key='-SALARY-')],
                        [sg.Checkbox('Data Scientist', default=False, key='-Searched-DS-')],
                        [sg.Checkbox('Data Analyst', default=False, key='-Searched-DA-')],
                        [sg.Checkbox('ML Engineer', default=False, key='-Searched-ME-')]
                ]
                )
                ],
                [sg.Button("Go!"), sg.Text(size=(20,1), enable_events=True, key="-GO-RETRIEVE-")],
                [sg.Button("Go back"), sg.Text(size=(10,1), enable_events=True, key="-GO-BACK-")],
                [sg.Button("Close")]
                ]

# time_period_layout = [[sg.Text("What declared time period for salary data do you wish to access?"), sg.Text(size=(30,1))],
#                      [sg.Frame(layout=[
#                          sg.Checkbox('Annual', default=True, key='-YEARLY-'),
#                          sg.Checkbox('Monthly', default=False, key='-MONTHLY-'),
#                          sg.Checkbox('Daily', default=False, key='-DAILY-')]],
#                     [sg.Button("Go!"), sg.Text(size=(20,1), enable_events=True, key="-GO-RETRIEVE-")]
#                      ])]]

retrieve_window = sg.Window("Retrieve", retrieve_layout)

search_dict = {'search_Job_title': '',
                'search_Org_name': '',
                'search_DA':False,
                'search_DS':True,
                'search_ME':False,
                'salary_period':'Y',
                'get_Job_description': False,
                'get_Job_salary': True}

current_window = intro_window
while True:
    event, values = current_window.read()
    #end program if user closes window or
    #presses the OK button
    if event == "Close" or event == sg.WIN_CLOSED:
        break
    elif event =="Scrape":
        print("Still in build")
        break
    elif event =="Retrieve":
        print("Still in build")
        engine = db.create_engine('sqlite:///preprocessing_nb/scraped_jobs.sqlite')
        connection = engine.connect()
        current_window.close()
        current_window = retrieve_window
    elif event =="Go!":
        search_dict['search_Job_title'] = values['-JOB-TITLE-']
        search_dict['search_Org_name'] = values['-ORG-NAME-']
        search_dict['get_Job_salary'] = values['-SALARY-']
        search_dict['get_Job_description'] = values['-DESCR-']
        search_dict['search_DS'] = values['-Searched-DS-']
        search_dict['search_DA'] = values['-Searched-DA-']
        search_dict['search_ME'] = values['-Searched-ME-']

        table = pd.read_sql_query(f"""
                            SELECT s.Job_Id, Job_Name, Org_Name, Salary
                            FROM salaries s JOIN job_search j ON s.Job_Id == j.Job_Id
                            WHERE (Salary IS NOT NULL AND 
                                   j.Searched_data_scientist == {search_dict['search_DS']} AND
                                   j.Searched_data_analyst == {search_dict['search_DA']} AND
                                   j.Searched_machine_learning_engineer == {search_dict['search_ME']})
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
        else:
            cur_table = cur_table
        pd.set_option('display.expand_frame_repr', False)
        print(cur_table)
        # sns.distplot(cur_table.Salary.values, bins=10, kde=False)
        # plt.show()
    elif event=="Go back":
        current_window.close()
        current_window = intro_window
        

current_window.close()
