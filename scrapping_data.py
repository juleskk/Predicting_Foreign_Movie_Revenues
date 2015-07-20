
# coding: utf-8

# In[ ]:

import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
import pandas as pd
import pickle
from datetime import datetime
import statsmodels.api as sm
import matplotlib.pyplot as plt
from patsy import dmatrices

# Getting data from Box Office Mojo 

def make_soup(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    return soup
def get_movie_list_url():
    #returns the urls for the top 100 movies from 2000-2015
    movie_list_url= []
    years = range(2000,2015)
    
    for year in years:
        url = ('http://www.boxofficemojo.com/yearly/chart/'
               '?page=1&view=releasedate&view2=domestic&yr='
               + str(year) +'&adjust_yr=2015&p=.htm')
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        for link in soup.select('td > b > font > a[href^=/movies/?]'):
            movie_list_url.append('http://www.boxofficemojo.com' + link.get('href'))
            
    return movie_list_url

movie_list_url = get_movie_list_url()

def get_categories(movie_list_url):
    
    rows_list = []
    
    for url in movie_list_url:
        dict1 = {}
        soup = make_soup(url)
    
        title = str(soup.find_all('b')[1].text)
        x = str(soup.find_all('b')[3].text)
        if 'Domestic Lifetime Gross' in x:
            domestic = str(soup.find_all(class_='mp_box_content')[0].find_all('tr')[0].find_all('td')[1].text.strip())
            studio =  str(soup.find_all('b')[4].text)
            release = str(soup.find_all('b')[5].text)
            genre = str(soup.find_all('b')[6].text)
            runtime= str(soup.find_all('b')[7].text)
            rating = str(soup.find_all('b')[8].text)
            budget = str(soup.find_all('b')[9].text)
            
        else:
            domestic = str(soup.find_all('b')[2].text)
            studio = str(soup.find_all('b')[3].text)
            release = str(soup.find_all('b')[4].text)
            genre = str(soup.find_all('b')[5].text)
            runtime= str(soup.find_all('b')[6].text)
            rating = str(soup.find_all('b')[7].text)
            budget = str(soup.find_all('b')[8].text)
      
        try:
            foreign = str(soup.find_all(class_='mp_box_content')[0].find_all('tr')[1].find_all('td')[1].text.strip())
        except IndexError:
            foreign = 'Unknown'
        try:
            lead = str(soup.find_all(class_='mp_box_content')[2].find_all('tr')[2].find_all('td')[1].find_all('a')[0].text)
        except IndexError:
            lead = 'Unknown'
        
        dict1.update({'title': title,
                      'domestic': domestic,
                      'studio': studio,
                      'release': release,
                      'genre': genre,
                      'runtime': runtime,
                      'rating': rating,
                      'budget': budget,
                      'foreign': foreign,
                      'lead': lead})

        rows_list.append(dict1)
        
    if len(rows_list) % 50 == 0:
        with open('my_data_partial.pkl', 'w') as picklefile:
            pickle.dump(rows_list.items(), picklefile)
            print "dumped " + str(len(rows_list.items))
    
    return rows_list
    
rows_list = get_categories(movie_list_url)

with open('my_data_partial.pkl', 'w') as picklefile:
            pickle.dump(rows_list, picklefile)
# Supplemental budget information obtained from the Numbers, scraped using Chrome Scrapper 
budget = pd.read_csv('budgets.csv') 
budget.rename(columns=lambda x: x.strip(), inplace = True)
data = pickle.load( open( "my_data_partial.pkl", "rb" ) )
df = pd.DataFrame(data, columns = ['budget', 'domestic', 'foreign', 'genre', 'lead', 'rating', 'release', 'runtime', 'studio', 'title'])

# Merge the two datasets, supplementing missing values
df2 = pd.merge(df, budget, how = 'left', on = ['title', 'title'])
df2.ix[df2['budget_x'].isnull(),'budget_x'] = df2['budget_y']
df2.ix[df2['budget_x'] == 'N/A','budget_x'] = df2['budget_y']
df2.ix[df2['domestic_x'].isnull(), 'domestic_x'] = df2['domestic_y']
df2.ix[df2['domestic_x'] == 'N/A','domestic_x'] = df2['domestic_y']
df2.ix[df2['foreign_x'].isnull(), 'foreign_x'] = df2['foreign_y']
df2.ix[df2['foreign_x'] == 'N/A', 'foreign_x'] = df2['foreign_y']
df = pd.DataFrame(df2, columns = ['budget_x', 'domestic_x', 'foreign_x', 'genre', 'lead', 'rating', 'release_x', 'runtime', 'studio', 'title'])
df.rename(columns={'budget_x': 'budget', 'domestic_x': 'domestic', 'foreign_x': 'foreign', 'release_x':'release'}, inplace=True)


with open('final_data.pkl', 'w') as picklefile:
            pickle.dump(rows_list, picklefile)

