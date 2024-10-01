import csv
import pandas as pd
import matplotlib.pyplot as plt
import os
os.chdir(r'C:\Users\ttjrb\OneDrive\Desktop\University Important\summer 2024 work\projects\Visualizing nba database')
import prompt1_final as p1

basic= pd.read_csv(r"C:\Users\ttjrb\OneDrive\Desktop\University Important\summer 2024 work\projects\databases\ALL 1320 nba games 2022-23\basic.csv",usecols=('name','SEC','FGpct','3PM','3Ppct','FTM','FTpct','ORB','TRB','AST','STL','BLK','TOV','PTS','plusminusPTS'))
advanced=pd.read_csv(r"C:\Users\ttjrb\OneDrive\Desktop\University Important\summer 2024 work\projects\databases\ALL 1320 nba games 2022-23\advanced.csv",usecols=('USGpct','DEFRTG'))
gamesData=pd.read_csv(r"C:\Users\ttjrb\OneDrive\Desktop\University Important\summer 2024 work\projects\databases\ALL 1320 nba games 2022-23\games.csv")
matchupsData=pd.read_csv(r"C:\Users\ttjrb\OneDrive\Desktop\University Important\summer 2024 work\projects\databases\ALL 1320 nba games 2022-23\matchups.csv")
teamsAdvanced=pd.read_csv(r"C:\Users\ttjrb\OneDrive\Desktop\University Important\summer 2024 work\projects\databases\ALL 1320 nba games 2022-23\team_advanced.csv")


#prompt1: Showing the top K leaders in a particular stat on a bar chart
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





#prompt 2: Displaying the top 5 NBA leaders for all the stats requested by the user
def top5NStats():
    categories= ['SEC','FGpct','3PM','3Ppct','FTM','FTpct','ORB','TRB','AST','STL','BLK','TOV','PTS','plusminusPTS','USGpct','DEFRTG']
    displayedCategories=[]
    
    while True:
        category= input('''Enter the stats category (Press Q when you are done)
        #Input options: 
        'SEC'= Time played(in Seconds),
        'FGpct'= field goal percentage,
        '3PM'= 3pts made,
        '3Ppct'= 3pts percentage,
        'FTM'= Free throw made,
        'FTpct'=Free throw percentage,
        'ORB'=offensive rebound,
        'TRB'=rebounds,
        'AST'= Assists,
        'STL'= Steal,
        'BLK'= Block,
        'TOV'= Turnovers,
        'PTS'= Points,
        'plusminusPTS'= box plus minus,
        'USGpct'= Usage percentage,
        'DEFRTG'= Defensive rating''')

        if category.lower()=='q':
            break
        if category in categories:
            displayedCategories.append(category)
        else:
            print("enter a valid stat")


    for category in displayedCategories:
        statsSorted= p1.playersAvg.sort_values(category,ascending=False)
        print("Top 5  "+category+" players in the NBA:")
        print(statsSorted.head())
        print("\n"+"\n")

    print('THANK YOU FOR USING MY SERVICE, BYE.') 





#3 prompt: Displaying the top or bottom k NBA teams by wins
teams= gamesData['home'].unique()
teamsRecordsList=[]

for team in teams:   
    teamRecord={}
    df1= gamesData[gamesData['home']==team]
    homeWin=0
    homeLost=0
    for i in range(len(df1)):
        if df1['h_pts'].iloc[i]>df1['a_pts'].iloc[i]:
            homeWin+=1
        else:
            homeLost+=1

 
    df2= gamesData[gamesData['away']==team]
    awayWin=0
    awayLost=0
    for i in range(len(df2)):
        if df2['h_pts'].iloc[i]<df2['a_pts'].iloc[i]:
            awayWin+=1
        else:
            awayLost+=1


    teamRecord['name']= team
    teamRecord['homeWin']=homeWin
    teamRecord['awayWin']=awayWin
    teamRecord['totalWins']=homeWin+awayWin
    teamRecord['homeLost']=homeLost
    teamRecord['awayLost']=awayLost
    teamRecord['totalLosts']=homeLost+awayLost

    teamsRecordsList.append(teamRecord)

teamsRecords=pd.DataFrame(teamsRecordsList)

def teamsRanking(order,k):
    order=order.lower()

    if k in range(1,31):
        if order=="top":
            topk=teamsRecords.sort_values('totalWins', ascending=False).head(k)


            plt.barh(topk['name'],topk['totalWins'])
            plt.ylabel('teams')
            plt.xlabel('wins')
            plt.title('top '+ str(k)+ ' teams in the nba')
            plt.gca().invert_yaxis()
            plt.show()
        

        if order=="bottom":
                bottomk=teamsRecords.sort_values('totalWins', ascending=False).tail(k)

                plt.barh(bottomk['name'],bottomk['totalWins'])
                plt.ylabel('teams')
                plt.xlabel('wins')
                plt.title('bottom '+ str(k)+ ' teams in the nba')
                plt.show()
             
        else:
            return print('order should either be "top" or "bottom" ')
    else:
        return print('the number of teams ranges from 1 to 30')
    


#4 prompt: Displaying scoring totals marks (>150,>125,>110,>100,<90…)
allScores=[]

for i in range(len(gamesData['h_pts'])):
    allScores.append(gamesData['h_pts'].iloc[i])
for i in range(len(gamesData['a_pts'])):
    allScores.append(gamesData['a_pts'].iloc[i])

#classifying the points using given marks
allScoresCount={}

for score in allScores:
#>150
    if score>150:
        if ">150" in allScoresCount:
            allScoresCount[">150"]+=1
        else:
            allScoresCount[">150"]=1
#>125
    if score>125:
        if ">125" in allScoresCount:
            allScoresCount[">125"]+=1
        else:
            allScoresCount[">125"]=1
#>110
    if score>110:
        if ">110" in allScoresCount:
            allScoresCount[">110"]+=1
        else:
            allScoresCount[">110"]=1
#>100
    if score>100:
        if ">100" in allScoresCount:
            allScoresCount[">100"]+=1
        else:
            allScoresCount[">100"]=1
#>90
    if score>90:
        if ">90" in allScoresCount:
            allScoresCount[">90"]+=1
        else:
            allScoresCount[">90"]=1
#<90
    if score<90:
        if "<90" in allScoresCount:
            allScoresCount["<90"]+=1
        else:
            allScoresCount["<90"]=1


desiredOrder=['>90', '>150','>100', '>110', '>125', '<90' ]
allScoresCountSorted={key: allScoresCount[key] for key in desiredOrder}


allScoresCountKeys=[]
allScoresCountValues=[]

for i in allScoresCountSorted:
    allScoresCountKeys.append(i)
    allScoresCountValues.append(allScoresCountSorted[i])

plt.pie(allScoresCountValues,labels=allScoresCountKeys)
plt.title("The most frequent pts marks of the season")
plt.show()




#5 prompt: Show how many times has a stat being done and optionally who did them
df=pd.concat([basic,advanced], axis=1)
df.head()

def statsFrequency(category,value):
    records= input("Do you want to see the records? (Y for yes and N for no)")
    if records.lower()== "y":
        print("frequency: " + str(len(df[df[category]==value])))
        return df[df[category]==value]
    if records.lower()== "n":
        return print("frequency: " + str(len(df[df[category]==value])))
    



#6 prompt: Linear chart to show the evolution of pace within the season
n=len(teamsAdvanced)
split=n//4

#creating 2 lists for the data visualization, one with the average for a percentage of the season and another one with the given percentage of the season
percentage=["25%","50%","75%","100%"]
splitn=[teamsAdvanced.iloc[:split],teamsAdvanced.iloc[split:(2*split)], teamsAdvanced.iloc[(2*split):(3*split)], teamsAdvanced.iloc[(3*split):]]
paceList=[]

for split in splitn:
    pace=split['pace'].mean()
    paceList.append(pace)

plt.plot(percentage,paceList,marker="o")
plt.title('linear progression of pace for the season 2022')
plt.xlabel('season evolution')
plt.ylabel('pace')
plt.show()




#7 prompt: Produce a csv file with the most recurrent matchups of the season

#create an empty dataframe with the desired columns
df=pd.DataFrame(columns=['name','matchup','time','pts'])

players= matchupsData['ofplayer'].unique()
i=0


#extract the list of unique players that played during this season
players= matchupsData['ofplayer'].unique()
i=0

#iterating every player and isolationg all their matchups data in a new data frame
for player in players:
    playerLoc= matchupsData[matchupsData['ofplayer']==player]

#extract the list of unique players the actual player (iteration) had a matchup against
    playerMatchups= playerLoc['deplayer'].unique()

#iterating every player from the matchups list and finding the sum of the matchup time and of the points scored
    for matchup in playerMatchups:
        matchupTime= playerLoc[playerLoc['deplayer']==matchup]['matchupSEC'].sum()
        matchupPts= playerLoc[playerLoc['deplayer']==matchup]['playerPTS'].sum()

#appending each matchup total stats to the pre-created dataframe
        df.loc[i]=[player,matchup,matchupTime,matchupPts]
        i+=1

df
#df[df["name"]=="Joel Embiid"].sort_values('pts', ascending=False)
#df.sort_values('time',ascending=False)
#df.sort_values('time',ascending=False).to_csv("most recurrent matchups (from prompt7).csv",index=False)