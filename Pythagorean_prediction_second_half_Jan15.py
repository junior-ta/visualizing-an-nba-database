#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statsmodels.formula.api as smf

gamesData=pd.read_csv(r"C:\Users\ttjrb\OneDrive\Desktop\University Important\summer 2024 work\projects\databases\ALL 1320 nba games 2022-23\games.csv")


# In[3]:


gamesData=gamesData[['home','away','h_pts','a_pts','date']]
gamesData=gamesData.rename(columns={'home':'h_team','away':'a_team'})


# In[4]:


#adding columns to specify whch team won
gamesData['h_win']=np.where(gamesData['h_pts']>gamesData['a_pts'],1,0)
gamesData['a_win']=np.where(gamesData['h_pts']<gamesData['a_pts'],1,0)

gamesData['count']=1
gamesData


# In[5]:


#splitting home games and away games for every team
home=gamesData[['h_team','h_pts','a_pts','h_win','count','date']]
home=home.rename(columns={'h_team':'team','h_pts':'pts','h_win':'win','a_pts':'opp_pts'})
away=gamesData[['a_team','a_pts','h_pts','a_win','count','date']]
away=away.rename(columns={'a_team':'team','a_pts':'pts','a_win':'win','h_pts':'opp_pts'})


# In[8]:


#concatenating home and away, meaning that one game is in the table 2 times (both for the home and the away team)
Data=pd.concat([home,away])
Data


# In[12]:


#parsing the dates to split the season in 2
Data['date']=np.where(Data['date'].notna(),Data['date'].str[0:4] + Data['date'].str[5:7] + Data['date'].str[8:10],0)

#converting dates to numeric
Data['date'] = pd.to_numeric(Data['date'], errors='coerce').fillna(0).astype(int)


# In[51]:


#Splitting the regular season into before and after the all star break

half1=Data[Data['date']<20230115]
half2=Data[Data['date']>20230115]


# In[57]:


#Half1 teams records and totals, win % and pythogorean expectation

half1=half1.groupby('team')[['win','pts','opp_pts','count']].sum().reset_index()
half1['win_perc']=half1['win']/half1['count']
half1['p_expectation']=half1['pts']**2/(half1['pts']**2+half1['opp_pts']**2)
half1


# In[59]:


#Half2 teams records and totals, win % and pythogorean expectation

half2=half2.groupby('team')[['win','pts','opp_pts','count']].sum().reset_index()
half2['win_perc']=half2['win']/half2['count']
half2['p_expectation']=half2['pts']**2/(half2['pts']**2+half2['opp_pts']**2)
half2


# In[61]:


predictor=pd.merge(half1,half2,on='team')
predictor=predictor[['team','win_perc_x','p_expectation_x','win_perc_y','p_expectation_y']]
predictor= predictor.rename(columns={'win_perc_x':'win_perc1st','p_expectation_x':'p_expectation1st','win_perc_y':'win_perc2nd','p_expectation_y':'p_expectation2nd'})


# In[63]:


predictor


# In[65]:


# First, plot Pythagorean Expectation against win percentage in the second half of the season
sns.relplot(x="p_expectation1st", y="win_perc2nd", data = predictor)


# In[66]:


# Now, compare this with a plot of win percentage from the first half of the season against win percentage
#in the second half of the season

sns.relplot(x="win_perc1st", y="win_perc2nd", data = predictor)


# In[68]:


# The two plots look similar
# We can be more precise still if we compare the correlation coefficients. The first row of the table shows the 
# correlation of win percentage in second half of the season against itself, win percentage in the first half of the season,
# Pythagorean Expectation in the first half of the season, and Pythagorean Expectation in the second half of the season.
# Our focus is on comparing the second and third columns.

predictorPL= predictor[['win_perc2nd','win_perc1st','p_expectation1st','p_expectation2nd']]
predictorPL.corr()


# In[70]:


keyvars = predictor.sort_values(by=['win_perc2nd'],ascending=False)
keyvars


# In[ ]:




