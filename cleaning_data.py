
# coding: utf-8


import pickle
import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
import pandas as pd
import pickle
import datetime as dt
import statsmodels.api as sm
import matplotlib.pyplot as plt
from patsy import dmatrices

data = pickle.load( open( "final_data.pkl", "rb" ) )
df = pd.DataFrame(data, columns = ['budget', 'domestic', 'foreign', 'genre', 'lead', 'rating', 'release', 'runtime', 'studio', 'title'])

budget = pd.read_csv('budgets.csv')
budget.rename(columns=lambda x: x.strip(), inplace = True)

df2 = pd.merge(df, budget, how = 'left', on = ['title', 'title'])

df2.ix[df2['budget_x'].isnull(),'budget_x'] = df2['budget_y']
df2.ix[df2['budget_x'] == 'N/A','budget_x'] = df2['budget_y']
df2.ix[df2['domestic_x'].isnull(), 'domestic_x'] = df2['domestic_y']
df2.ix[df2['domestic_x'] == 'N/A','domestic_x'] = df2['domestic_y']
df2.ix[df2['foreign_x'].isnull(), 'foreign_x'] = df2['foreign_y']
df2.ix[df2['foreign_x'] == 'N/A', 'foreign_x'] = df2['foreign_y']

df = pd.DataFrame(df2, columns = ['budget_x', 'domestic_x', 'foreign_x', 'genre', 'lead', 'rating', 'release_x', 'runtime', 'studio', 'title'])
df.rename(columns={'budget_x': 'budget', 'domestic_x': 'domestic', 'foreign_x': 'foreign', 'release_x':'release'}, inplace=True)
df['budget'] = df['budget'].astype('str')


def make_millions():
    # convert budget from string to float
    lst = []
    for row in df['budget']:
        if 'million' in row:
            temp = row.split()[0]
            temp = str(temp) + str('000000')
            lst.append(temp)
        else:
            lst.append(row)
    return lst

def clean_data(df):
#     # get rid of extraneous symbols 
    df = df.applymap(lambda x: x.strip('$'))
    df = df.applymap(lambda x: x.replace(',', ''))
    df = df.applymap(lambda x: x.replace('.', ''))
    
    return df

def convert_runtime():
    # get runtime in minutes format 
    lst = []
    for row in df['runtime']:
        temp = row.split()
        temph = int(temp[0])
        tempm = int(temp[2])
        time = (temph*60) + tempm
        lst.append(time)
    return lst


def make_genres2():
    # make genres based on first word (ie. 'sci-fi, 'family')
    temp = []
    for row in df['genre']:
        temp.append(row.split()[0])
    return temp

def make_genres3():
    # make genres based on last word (ie. comedy, drama)
    temp2 = []
    for row in df['genre']:
        if len(row.split()) > 1:
            temp2.append(row.split()[-1])
        else:
            temp2.append(row.split()[0])
    return temp2

make_millions()
df = clean_data(df)
df['budget'] = make_millions()

df['release'] = pd.to_datetime(df['release'])
df['year'] = [row.year for row in df['release']]
df['month'] = [row.month for row in df['release']]
df['runtime'] = convert_runtime()


df.dropna(subset=['budget', 'foreign'], how='all')

df = df[df.budget != 'nan']
df = df[df.foreign != 'Unknown']
df = df[df.foreign != 'n/a']
df['budget'] = df['budget'].astype(int)
df['foreign'] = df['foreign'].astype(int)
df['domestic'] = df['domestic'].astype(int)
df['genre2'] = temp 
df['genre3'] = temp2


# Make new genre categories 
temp = []
for row in df['genre']:
    temp.append(row.split()[0])
df['genre2'] = temp 

temp2 = []
for row in df['genre']:
    if len(row.split()) > 1:
        temp2.append(row.split()[-1])
    else:
        temp2.append(row.split()[0])

df['genre3'] = temp2

with open('final_data.pkl', 'w') as picklefile:
            pickle.dump(df, picklefile)


# In[ ]:




# In[ ]:



