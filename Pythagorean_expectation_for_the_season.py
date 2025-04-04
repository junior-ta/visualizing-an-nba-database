#!/usr/bin/env python
# coding: utf-8

# In[205]:


import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statsmodels.formula.api as smf

gamesData=pd.read_csv(r"C:\Users\ttjrb\OneDrive\Desktop\University Important\summer 2024 work\projects\databases\ALL 1320 nba games 2022-23\games.csv")


# In[207]:


gamesData=gamesData[['home','away','h_pts','a_pts','date']]
gamesData=gamesData.rename(columns={'home':'h_team','away':'a_team'})


# In[217]:


gamesData['h_win']=0
for i in range(len(gamesData['h_pts'])):
    if gamesData['h_pts'].iloc[i]>gamesData['a_pts'].iloc[i]:
        gamesData.iloc[i,5]=1

gamesData['a_win']=np.where(gamesData['h_pts']<gamesData['a_pts'],1,0)

gamesData['count']=1
gamesData


# In[211]:


# performance of teams at home

home=gamesData.groupby('h_team')[['h_win','h_pts','a_pts','count']].sum().reset_index()
home=home.rename(columns={'h_team':'team','h_pts':'pts_h','a_pts':'opp_pts_h','count':'h_games'})


# In[213]:


# performance of teams on the road

away=gamesData.groupby('a_team')[['a_win','h_pts','a_pts','count']].sum().reset_index()
away=away.rename(columns={'a_team':'team','h_pts':'opp_pts_a','a_pts':'pts_a','count':'a_games'})
away


# In[179]:


#merging for each team

overall=pd.merge(home,away,on='team')


# In[181]:


#calculations

overall['wins']=overall['h_win']+overall['a_win']
overall['games_played']=overall['h_games']+overall['a_games']
overall['pts_scored']=overall['pts_h']+overall['pts_a']
overall['pts_opp']=overall['opp_pts_h']+overall['opp_pts_a']

#defining win% and pythagorean expectation
overall['win%']=overall['wins']/overall['games_played']
overall['p_expectation']=overall['pts_scored']**2/(overall['pts_scored']**2+overall['pts_opp']**2)

overall


# In[191]:


sns.relplot(x='p_expectation',y='win%',data=overall)


# In[201]:


overall.rename(columns={'win%': 'win_percent'}, inplace=True)
pyth_lm=smf.ols(formula= 'win_percent~p_expectation',data=overall).fit()
pyth_lm.summary()


# In[ ]:




