
# coding: utf-8

# In[1]:

import pickle
import pandas as pd
import pickle
import statsmodels.api as sm
import matplotlib.pyplot as plt
from patsy import dmatrices
import patsy
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import ShuffleSplit
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from sklearn import linear_model, datasets

get_ipython().magic(u'matplotlib inline')
data = pickle.load( open( "final_data.pkl", "rb" ) )
df = pd.DataFrame(data, columns = ['budget', 'domestic', 'foreign', 'genre', 'lead', 'rating', 'release', 'runtime', 'studio', 'title', 'year', 'month', 'genre2', 'genre3'])
df.head()


# In[ ]:

# Testing Lars, Ridge, Lasso

lars = linear_model.LarsCV()
y, X = dmatrices('foreign ~ budget + C(genre3) + runtime + C(rating) + C(month) + C(year) -1', 
                 data=df.set_index('title'), return_type='dataframe')
y1 = np.squeeze(y)
lars.fit(X, y1)
preds = pd.DataFrame(zip(X.index, lars.predict(X)), columns = ['title', 'yhat'])
rmse = np.sqrt(((lars.predict(X) - y1) ** 2).mean())
r2 = lars.score(X, y1)


# In[ ]:

# Lars plot
df2 = df.loc[df['title'] != "Avatar"]
sns.set_style("ticks")
sns.despine(offset=10, trim=True)
fig = plt.figure(figsize=(13,12))
ax = fig.add_subplot(111)
ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False)  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left() 
plt.ylim(-20000000, df2.foreign.max()+ 10000000)
plt.xlim(-50000000, df2.yhat.max() + 10000000)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.0f')%(x*1e-8)))
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.0f')%(x*1e-8)))
plt.xticks(fontsize=20)  
plt.yticks(fontsize=20)  

sns.regplot('yhat', 'foreign', data=df2, color = '#3FD0A0', scatter_kws={"s": 80})
plt.ylabel('Foreign Gross: $Y_i$', fontsize = 20)
plt.xlabel('Predicted Foreign Gross: $\hat{Y}_i$', fontsize=25) 
fig.savefig('temp.png', transparent=True)

# Lars residual plot

sns.set_style("ticks")
sns.despine(offset=10, trim=True)
fig = plt.figure(figsize=(13,12))
ax = fig.add_subplot(111)
ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False)  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left() 
plt.ylim(-500000000, 700000000)
plt.xlim(-50000000, 600000000)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.0f')%(x*1e-8)))
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.0f')%(x*1e-8)))
plt.xticks(fontsize=20)  
plt.yticks(fontsize=20)  
sns.residplot('yhat', 'foreign', data=df2, color = '#226b53', scatter_kws={"s": 80}, lowess = True)

ax.set_xlabel('')
plt.ylabel('Residuals', fontsize=20) 
fig.savefig('temp.png', transparent=True)

# Movie genre bar graph

sns.set(style = 'white')
fig = plt.figure(figsize=(26,12))
ax = fig.add_subplot(111)
ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False)  
ax.spines["bottom"].set_visible(False)  
ax.spines["left"].set_visible(False)
ax.set_ylabel('')
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.0f')%(x*1e-1)))
plt.xticks(fontsize=20)  
plt.yticks(fontsize=20) 
sns.barplot('coef','label', data=temp, color = '#226b53')
ax.set_ylabel('')
ax.set_xlabel('\beta', fontsize=20)

# Line plot of foreign vs. domestic  
years = df.groupby(['year'], as_index=False).sum()
years['year'] = df['year'].astype('str')
years['year2'] = range(1,16)
domestic = years['domestic']
foreign = years['foreign']
year = years['year2'] 
sns.set_style("ticks")
sns.despine(offset=10, trim=True)
fig = plt.figure(figsize=(26,12))
ax = fig.add_subplot(111)
ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False)  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left() 
ax.set_xticklabels(range(2000, 2016, 2), fontsize=30)  
ax.set_yticklabels(range(6, 20), fontsize=30)  
line1, = plt.plot(year, foreign, linestyle='--', color ='#226b53', label = 'Foreign')
line2, = plt.plot(year, domestic, color = '#3FD0A0', label = 'Domestic')
plt.legend(frameon = True, loc = 2, fontsize = 30)
ax.set_ylabel('Gross (in billion USD)', fontsize = 30)
plt.xlim(.5, max(year))
fig.savefig('temp.png', transparent=True)
plt.ylim(0,max(ydata)+ystep)
ax.set_title('Total Gross by Year')

# Reg plot of foreign vs. domestic
sns.set_style("ticks")
sns.despine(offset=10, trim=True)
fig = plt.figure(figsize=(26,12))
ax = fig.add_subplot(111)
ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False)  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left() 
df2 = df.loc[df['title'] != "Avatar"]
plt.ylim(-10000000, df2.foreign.max()+ 10000000)
plt.xlim(-10000000, df2.domestic.max() + 10000000)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.0f')%(x*1e-8)))
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.0f')%(x*1e-8)))
plt.xticks(fontsize=25)  
plt.yticks(fontsize=25)  
sns.regplot('domestic', 'foreign', data=df2, color = '#3FD0A0', scatter_kws={"s": 80})
plt.ylabel("Foreign Gross (in 10 million USD)", fontsize=25)  
plt.xlabel("Domestic Gross (in 10 million USD)", fontsize=25) 
fig.savefig('temp.png', transparent=True)

# Full model 
y, X = dmatrices('foreign ~ budget + budget:C(genre3) + C(month) + C(year) +C(rating) + runtime + budget*runtime -1', data=df, return_type='dataframe')
X2 = sm.add_constant(X)
X_digits = np.array(X2)
y_digits = np.array(y)
n_samples = X2.shape[0]
cv = ShuffleSplit(n_samples, n_iter=20, test_size=0.3, random_state=3)
regr = linear_model.LinearRegression()
scores = cross_validation.cross_val_score(regr, X_digits, y_digits, scoring='mean_squared_error', cv=cv)
x = scores.mean()
x1 = x * -1
rmse = np.sqrt(x1)

