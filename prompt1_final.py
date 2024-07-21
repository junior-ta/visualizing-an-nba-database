import csv
import pandas as pd
import matplotlib.pyplot as plt

basic= pd.read_csv(r"C:\Users\ttjrb\OneDrive\Desktop\University Important\summer 2024 work\projects\databases\ALL 1320 nba games 2022-23\basic.csv",usecols=('name','SEC','FGpct','3PM','3Ppct','FTM','FTpct','ORB','TRB','AST','STL','BLK','TOV','PTS','plusminusPTS'))
advanced=pd.read_csv(r"C:\Users\ttjrb\OneDrive\Desktop\University Important\summer 2024 work\projects\databases\ALL 1320 nba games 2022-23\advanced.csv",usecols=('USGpct','DEFRTG'))


df=pd.concat([basic,advanced], axis=1)

playerNames= df['name'].unique()
len(playerNames)

dfTemp=df.set_index('name')

eligiblePlayersList=[]
statsCategoriesList= dfTemp.columns
resultList=[]
for player in playerNames:
    iteration= dfTemp.loc[player]
    if len(iteration)>58:
        eligiblePlayersList.append(player)
        avg= iteration.mean()
        playerStatsList=[]      
        for i in range(len(statsCategoriesList)):
            playerStatsList.append(avg[statsCategoriesList[i]])            
        playerDict={}
        for i in range(len(statsCategoriesList)):
            playerDict[statsCategoriesList[i]]= playerStatsList[i]
        resultList.append(playerDict)

playersAvg=pd.DataFrame(resultList)
playersAvg.insert(0,'name',eligiblePlayersList)

def topKLeader(category,K):
    statsSorted=playersAvg.sort_values(category,ascending=False)
    statsForVisualization= statsSorted.head(K)[category]
    namesForVisualization= statsSorted.head(K)['name']

    plt.bar(namesForVisualization, statsForVisualization,width=0.3)
    plt.title('Top '+ str(K)+'  '+category+' players in the NBA 2022/23')
    plt.xlabel('players')
    plt.ylabel(category)
    plt.show()

#par1= input('what category leaders do you need?')
#par2=int(input('how many leader do you need'))
#topKLeader(par1, par2)