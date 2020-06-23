# (WORK IN PROGRESS) Exploring the London Data Science job market

Advice and information about the job market for Data Scienstists and Machine Learning (ML) Engineers abounds on the internet. 
I wanted to have a look for myself at my own sampled data and see what conclusions I could draw from it.

This project was undertaken for 3 reasons: 
1. To investigate and test hypotheses about Data Scientists, Data Analysts and ML Engineers;
2. To test presuppositions about the job market for Data Scientists / Analysts ML Engineers and
3. To demonstrate and practice data retrieval via webscraping. 

*One important caveat I must mention about the data is this: although all of the data neatly categorised as either DS, DA or MLEng is shown clearly in my data analysis and exploration, if you had to go through each job post by title you will find plenty that say "Business Analyst", "Data Engineer" or "Data Science Researcher". This is because the main method by which the data was extracted was by entering the search terms and thus the jobs are categoried **by which search term retrieved them**. This speaks volumes to the fact that:
a) there is significant semantic overlap between these terms;
b) Many such job posts include the job search terms not in the title but in the description and 
c) That our data acquisition process relies on the inner functioning of indeed.co.uk's internal search engine.

###### Therefore I retrieved Data Scientist and ML Engineer job post data from Indeed.co.uk in late May 2020 using Selenium webdriver and BeautifulSoup. The same was done on 23rd of June for Data Analyst
###### I wrangled and analysed the data in Pandas, MNLTK, Seaborn and Matplotlib. 


##### Here are 3 concrete questions I wanted to answer with this project:
1. How many job posts for this sector advertise their salary?
2. Are there any skills that differentiate the two types of job?
3. How many of the jobs seem to indicate that remote/flexible working is an option?

# Findings in brief (this list is still being expanded):

## AWS and cloud technology
* from analysing the job descriptions of both job types,the only salient major difference is mentions of AWS (Amazon Web services) are three times as high across ML Eng jobs (>600) than DS jobs (~200);
* Looking at mentions per job post:
    * the % ML jobs that mention AWS is:  32.65%
    * the % DS jobs that mention AWS is:  20.0%
* Looking at mean number of mentions of AWS:
    * (Excluding posts that DON'T mention AWS), the mean number of times an ML job post mentions AWS is 2.78
    * (Excluding posts that DON'T mention AWS), the mean number of times an DS job post mentions AWS is 1.83
* for the same search but with a broader list of terms (e.g. 'GCP', 'cloud', 'azure'), we get:
    * Excluding posts that DON'T mention cloud services at all, the mean number of times an ML job post mentions cloud services is 3.39
    * Excluding posts that DON'T mention cloud services at all, the mean number of times an DS job post mentions cloud services is 2.22
    
## Advertising salary:
From the sample of 2211 jobs we collected, the percentage of job posts where we have been unable to detect salary information is 61.7%

Looking at the breakdown 
    * The percentage of DS jobs in our sample that openly state any kind of salary range is     37.06
    * The percentage of ML Eng jobs in our sample that openly state any kind of salary range is 32.21
    * The percentage of DA jobs in our sample that openly state any kind of salary range is


    
_____________________________________________________________________________________________________________________________

### The Data at a Glance (EDA)
![hourly_pay](https://github.com/Ioana-P/MLEng_vs_DScientist_analysis/blob/master/salary_per_hour.jpeg)


![yearly_salary](https://github.com/Ioana-P/MLEng_vs_DScientist_analysis/blob/master/yearly_salary_dist.jpeg)


_____________________________________________________________________________________________________________________________

### Statistical tests comparing salaries between ML Engineers and Data Scientists


Limitations of data: small sample size of 421 total (202 for DS; 219 for ML Engineers)

* [WIP]

_____________________________________________________________________________________________________________________________


### Insights and possible actions
[WIP]
* So far the advice of focusing on SQL is solid advice for either type of job
* Experience with AWS is helpful with ML Engineering positions, although it's not clear _how_ helpful


### Filing system:

Notebooks
1. Modelling_and_insights.ipynb - empty for the moment
2. Model_building_and_optimization.ipynb - empty for the moment
3. EDA.ipynb - exploration of the data, text data primarily, followed by salary data.
4b. Data_preprocessing.ipynb - preprocessing of the text, extraction of salary and review information was done here
4a_data_extraction_and_cleaning.ipynb - webscraping and html mining was tested and refined iteratively here

functions.py - refactored code lives here, for eda,cleaning, webscraping.

Folders
* clean_data - folder containing clean data and any additional summary data generated
* raw_data - data as it was when imported / downloaded / scraped into my repository
* archive - any additional files and subfolders will be here
