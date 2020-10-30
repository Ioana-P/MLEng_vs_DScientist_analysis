import sys
import streamlit as st 
import pandas as pd 
import numpy as np
import plotly.figure_factory as ff
import plotly
import plotly_express as px
import nltk
import string
import matplotlib.pyplot as plt
import wordcloud
from PIL import Image

from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer, PorterStemmer
import re
tokenizer = RegexpTokenizer(r'\b\w{3,}\b')
stop_words = list(set(stopwords.words("english")))
stop_words += list(string.punctuation)
sys.path.insert(1, '../')
from functions import gen_stopwords, gen_cloud, plot_freqdist_from_series, plot_term_bar

st.title("""
         Visualising data-centred roles""")

st.markdown('## __1. Salary data__')

st.write("""
        Plotting and comparing the salaries for data scientists, data 
        analysts and machine learning engineers. \n
        Data was scraped off indeed.co.uk.
        """)
@st.cache(suppress_st_warning=True)
def get_salary_data(url):
    df = pd.read_csv(url, 
                index_col=0, 
                error_bad_lines=False
                )
    st.write(df.head())
    df = df[['job_title', 'company', 'salary_from_page_source_as_stated', 
            'job_search_term', 'salary_from_page_source_time_period']]

    return df

salary_annual_df = get_salary_data('https://raw.githubusercontent.com/Ioana-P/MLEng_vs_DScientist_analysis/master/clean_data/salary_test.csv')
salary_annual_df.rename({'salary_from_page_source_as_stated': 'salary'}, axis=1, inplace=True)
salary_annual_df.salary.dropna(inplace=True)
st.write(salary_annual_df.groupby('job_search_term').describe().round(1))

data_plot_lst = []
final_df= None

st.sidebar.write("Salary analysis")
option_salary_period = st.sidebar.selectbox(
                'Which salary periods to look at (recommend annual: "Y")?',
                salary_annual_df.salary_from_page_source_time_period.unique())

'Looking at ', option_salary_period, ' salary period.'

option_jobs = st.sidebar.multiselect('Which group of jobs to look at for salary?',
                                    salary_annual_df.job_search_term.unique())

mask_jobs = salary_annual_df['job_search_term'].isin(option_jobs)
final_df = salary_annual_df[mask_jobs]

st.sidebar.write("Text analysis")

# @st.cache(allow_output_mutation=1)
# def sub_data(search_term, data_list, data):
#     new_data = data.loc[data.job_search_term==f'title: "{search_term}"']
#     data_list.append(new_data)
#     return data_list

if final_df.size == 0:
    print("Using all data")

    fig = px.histogram(salary_annual_df, x = 'salary',
                        color='job_search_term', marginal='box', 
                        # hover_name=['job_title'], 
                        hover_data=['job_title', 'company', 'salary'], 
                        opacity=0.6, 
                        )
    st.plotly_chart(fig, use_container_width=True)
else:
    fig = px.histogram(final_df, x = 'salary', 
                        color='job_search_term',
                        marginal='box',
                        hover_data=['job_title', 'company', 'salary']
                        )
    st.plotly_chart(fig, use_container_width=False)



@st.cache(suppress_st_warning=True)
def get_text_data(url):
    text = pd.read_csv(url, 
                index_col = 0,
                error_bad_lines=False,
                )
    text = text.loc[~text['job_descr'].isna()]
    return text

text_df = get_text_data('https://raw.githubusercontent.com/Ioana-P/MLEng_vs_DScientist_analysis/dev_gui/clean_data/OCT_snapshot_text.csv')

st.markdown('## __2. Text data__')
st.write("Snapshot of the text data")
st.write(text_df.head())
global datastopwords 
datastopwords = gen_stopwords()

option_WC_jobs = st.sidebar.multiselect('Which group of jobs to do wordcloud?',
                                    text_df.job_search_term.unique(), 
                                    )
WC_mask_jobs = text_df['job_search_term'].isin(option_WC_jobs)
text_df = text_df[WC_mask_jobs]


st.markdown("### Word cloud for all jobs")
def gen_cloud(data, max_words_num : int, stop_words = None,
              background_color = 'black', height = 300, 
              randomstate=42, fig_size=(100,100),
             cloud_title='Word Cloud', 
             cloud_height = 300, cloud_width = 200, cloud_max_font = 100
             ):
    
    text_data = ' '.join(data)
    if len(stop_words)!=0:
        text_data_clean = []
        for word in text_data.split(' '):
            if word.lower() not in stop_words:
                text_data_clean.append(word)
        text_data_clean = ' '.join(text_data_clean)
    else:
        text_data_clean = text_data
    plt.figure(figsize=fig_size)

    cloud = wordcloud.WordCloud(max_words=max_words_num, 
                                background_color=background_color, 
                                height=cloud_height, width = cloud_width, 
                                max_font_size= cloud_max_font,
                                random_state=randomstate)
    cloud.generate(text_data_clean)
    plt.figure(figsize=(100,100))
    fig, axes = plt.subplots(1, 2, gridspec_kw={'width_ratios':[3,2]}, )
    axes[0].imshow(cloud, interpolation='bilinear')
    for ax in axes:
        ax.set_axis_off()
    st.pyplot(fig)
    
    plt.figure(figsize=fig_size)

    plt.imshow(cloud)
    plt.title(cloud_title)
    plt.axis("off")
    plt.figure(figsize=fig_size)

    plt.show()
    return 

max_word = st.sidebar.slider("Max words", 10, 100, 20)
max_font = st.sidebar.slider("Max Font Size", 50, 350, 60)
wc_height = st.sidebar.slider("Plot Height", 20, 500, 300)
wc_width = st.sidebar.slider("Plot Width", 20, 500, 200)

background_color = st.sidebar.selectbox("Background color", ['black', 'white', 'blue', 'grey'], 1)

if st.sidebar.button("Plot"):
    st.write(f"Number of documents {len(text_df.job_descr)}")
    gen_cloud(text_df.job_descr, max_word, datastopwords, 
              background_color, cloud_title='Word cloud for all jobs',
              cloud_height = wc_height, cloud_width = wc_width, cloud_max_font = max_font)

# # fn for the UI
# def main():
#     st.write("# Trying out the sidebar too now!")
#     st.write("[By Ioana P](https://github.com/Ioana-P)")
#     max_word = st.sidebar.slider("Max words", 200, 3000, 200)
#     max_font = st.sidebar.slider("Max Font Size", 50, 350, 60)
#     # random = st.sidebar.slider("Random State", 30, 100, 42 )
#     # image = st.file_uploader("Choose a file(preferably a silhouette)")
#     text = st.text_area("Add text ..")
#     if st.button("Plot"):
#             # st.write("### Original image")
#             # image = np.array(Image.open(image))
#             # st.image(image, width=100, use_column_width=True)
#             # st.write("### Word cloud")
#             # st.write(cloud(image, text, max_word, max_font, random), use_column_width=True)
#         gen_cloud(text_df.job_descr, max_word, datastopwords, 'white', cloud_title='Word cloud for all jobs')

# if __name__=="main":
#     main()
