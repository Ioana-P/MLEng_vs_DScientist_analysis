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


intro_layout = [[sg.Text("Welcome to the Indeed Job Post Scraper"), sg.Text(size=(40,1))],
                 [sg.Button("Scrape"), sg.Text(size=(15, 1), enable_events=True, key="-SCRAPE-"),
                 ], 
                 [sg.Button("Retrieve"), sg.Text(size=(15,1), enable_events=True, key="-RETRIEVE-")
                 ],
                 [sg.Button("Close")]
                 ]

intro_window = sg.Window("IndeedScraper", intro_layout)


retrieve_layout = [[sg.Text("Retrieve job data"), sg.Text(size=(40,1))],
                [sg.Text("Job title"), sg.In(size=(15,1), enable_events=True, key='-JOB-TITLE-')],
                # [sg.Text("Company"), sg.In(size=(15,1), enable_events=True, key='-COMPANY-NAME-')],
                # [sg.Frame(layout=[
                [sg.Checkbox('Job description', default=False,key='-DESCR-'),
                sg.Checkbox('Salary', 
                default=True,key='-SALARY-')],
                [sg.Button("Go!"), sg.Text(size=(20,1), enable_events=True, key="-GO-RETRIEVE-")]
                ]

retrieve_window = sg.Window("Retrieve", retrieve_layout)

search_dict = {'Job_title': '',
                'Job_description': False,
                'Job_salary': True}

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
        current_window.close()
        current_window = retrieve_window
    elif event =="Go!":
        current_window.close()
        print(values['-JOB-TITLE-'])
        print(values['-SALARY-'])
        break

current_window.close()
