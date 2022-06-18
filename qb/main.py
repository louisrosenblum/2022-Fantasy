# 2022 Fantasy Script

import pandas as pd
import csv
import numpy as np
import requests
from bs4 import BeautifulSoup
import re

# Point per passing TD
ppptd = 6

def convert_datatypes(df):

    # Convert column datatypes
    df['Passing Yds'] = pd.to_numeric(df['Passing Yds'], downcast = "float",errors='coerce')
    df['Passing TD'] = pd.to_numeric(df['Passing TD'], downcast = "float",errors='coerce')
    df['Int'] = pd.to_numeric(df['Int'], downcast = "float",errors='coerce')
    df['Rushing Yds'] = pd.to_numeric(df['Rushing Yds'], downcast = "float",errors='coerce')
    df['RRTD'] = pd.to_numeric(df['RRTD'], downcast = "float",errors='coerce')

    return(df)

def normalize_career(df,years):

    df['Cmp'] = df['Cmp']/df['G']
    df['Att'] = df['Att']/df['G']
    df['Cmp%'] = df['Cmp']/df['Att']
    df['Passing Yds'] = df['Passing Yds']/df['G']
    df['Passing TD'] = df['Passing TD']/df['G']
    df['Passing 1D'] = df['Passing 1D']/df['G']
    df['Passing Lng'] = df['Passing Lng']/years
    df['Passing Yds/A'] = df['Passing Yds/A']/years
    df['Int'] = df['Int']/df['G']
    df['TD%'] = df['TD%']/years
    df['Int%'] = df['Int%']/years
    df['AY/A'] = df['AY/A']/years
    df['Y/C'] = df['Y/C']/years
    df['Rate'] = df['Rate']/years
    df['Sk'] = df['Sk']/df['G']
    df['Sk%'] = df['Sk%']/years
    df['NY/A'] = df['NY/A']/years
    df['ANY/A'] = df['ANY/A']/years
    df['4QC'] = df['4QC']/df['G']
    df['GWD'] = df['GWD']/df['G']
    df['Rush'] = df['Rush']/df['G']
    df['Rushing Yds'] = df['Rushing Yds']/df['G']
    df['Rushing 1D'] = df['Rushing 1D']/df['G']
    df['Rushing Lng'] = df['Rushing Lng']/years
    df['Rushing Yds/Att'] = df['Rushing Yds']/df['Rush']
    df['Sack Yds Lost'] = df['Sack Yds Lost']/df['G']
    df['RRTD'] = df['RRTD']/df['G']
    df['Fmb'] = df['Fmb']/df['G']

    df = df.rename(columns={
        "Att": "Att/G",
        "Fmb": "Fmb/G",
        "RRTD": "RRTD/G",
        "Rush": "Rush/G",
        "Rushing Yds": "Rushing Yds/G",
        "Rushing 1D": "Rushing 1D/G",
        "4QC": "4QC/G",
        "GWD": "4QC/G",
        "Int": "Int/G",
        "Sk": "Sacks/G",
        "Y/C": "Yds/Cmp",
        "Sack Yds Lost": "Sack Yds Lost/G",
        "Passing Yds": "Passing Yds/G",
        "Passing TD": "Passing TD/G",
        "Passing 1D": "Passing 1D/G",
        "Cmp": "Cmp/G"})

    df = df.drop('G',axis=1)

    return(df)

def normalize_last(df):
    
    df['Cmp'] = df['Cmp']/df['G']
    df['Att'] = df['Att']/df['G']
    df['Cmp%'] = df['Cmp']/df['Att']
    df['Passing Yds'] = df['Passing Yds']/df['G']
    df['Passing TD'] = df['Passing TD']/df['G']
    df['Passing 1D'] = df['Passing 1D']/df['G']
    df['Int'] = df['Int']/df['G']
    df['Sk'] = df['Sk']/df['G']
    df['4QC'] = df['4QC']/df['G']
    df['GWD'] = df['GWD']/df['G']
    df['Rush'] = df['Rush']/df['G']
    df['Rushing Yds'] = df['Rushing Yds']/df['G']
    df['Rushing 1D'] = df['Rushing 1D']/df['G']
    df['Rushing Yds/Att'] = df['Rushing Yds']/df['Rush']
    df['Sack Yds Lost'] = df['Sack Yds Lost']/df['G']
    df['RRTD'] = df['RRTD']/df['G']
    df['Fmb'] = df['Fmb']/df['G']

    df = df.rename(columns={
        "Att": "Att/G",
        "Fmb": "Fmb/G",
        "RRTD": "RRTD/G",
        "Rush": "Rush/G",
        "Rushing Yds": "Rush Yds/G",
        "Rushing 1D": "Rush 1D/G",
        "4QC": "4QC/G",
        "GWD": "4QC/G",
        "Int": "Int/G",
        "Sk": "Sacks/G",
        "Y/C": "Yds/Cmp",
        "Sack Yds Lost": "Sack Yds Lost/G",
        "Passing Yds": "Passing Yds/G",
        "Passing TD": "Passing TD/G",
        "Passing 1D": "Passing 1D/G",
        "Cmp": "Cmp/G"})

    df = df.drop('G',axis=1)
    df = df.drop('Year',axis=1)

    return(df)

def visit_player_page(name,url):

    print(name)

    train_df = None

    passing = pd.read_html(url, attrs = {'id': 'passing'})[0]

    # Rename duplicate columns
    passing.columns.values[11] = 'Passing Yds'
    passing.columns.values[16] = 'Passing 1D'
    passing.columns.values[17] = 'Passing Lng'
    passing.columns.values[18] = 'Passing Yds/A'
    passing.columns.values[25] = 'Sack Yds Lost'

    passing.drop('QBrec',axis=1,inplace=True)

    passing = passing.rename(columns={
        "TD": "Passing TD"})


    try:
        rushing = pd.read_html(url, attrs = {'id': 'rushing_and_receiving'})[0]
    except:
        return(None,None)

    # Drop multindex from rushing table
    rushing.columns = rushing.columns.droplevel()

    # Rename duplicate columns
    rushing.columns.values[8] = 'Rushing Yds'
    rushing.columns.values[10] = 'Rushing 1D'
    rushing.columns.values[11] = 'Rushing Lng'
    rushing.columns.values[12] = 'Rushing Yds/Att'

    # Drop duplicate columns from rush table
    rushing.drop('G',axis=1,inplace=True)
    rushing.drop('Age',axis=1,inplace=True)
    rushing.drop('TD',axis=1,inplace=True)
    rushing.drop('Yds',axis=1,inplace=True)
    rushing.drop('1D',axis=1,inplace=True)
    rushing.drop('Lng',axis=1,inplace=True)

    # Delete rows that aren't present in both passing and rushing tables
    pass_years = passing['Year'].unique().tolist()
    rush_years = rushing['Year'].unique().tolist()

    passing = format_df(passing)
    rushing = format_df(rushing)

    passing = passing[passing.Year.isin(rush_years) == True]
    rushing = rushing[rushing.Year.isin(pass_years) == True]
    
    df = pd.merge(passing, rushing, on='Year', how='outer',suffixes=['_passing','_rushing'])

    df['Year'] = df['Year'].str.replace('*','')
    df['Year'] = df['Year'].str.replace('+','')

    df = df.drop('Tm_passing',axis=1)
    df = df.drop('Pos_passing',axis=1)
    df = df.drop('No._passing',axis=1)
    df = df.drop('GS_passing',axis=1)
    df = df.drop('Y/G_passing',axis=1)
    df = df.drop('QBR',axis=1)

    if('AV' in df.columns):
        df = df.drop('AV',axis=1)
    
    if('Awards' in df.columns):
        df = df.drop('Awards',axis=1)
    df = df.drop('Tm_rushing',axis=1)
    df = df.drop('Pos_rushing',axis=1)
    df = df.drop('No._rushing',axis=1)
    df = df.drop('GS_rushing',axis=1)
    df = df.drop('Y/G_rushing',axis=1)
    df = df.drop('A/G',axis=1)
    df = df.drop('Tgt',axis=1)
    df = df.drop('Rec',axis=1)
    df = df.drop('Y/R',axis=1)
    df = df.drop('R/G',axis=1)
    df = df.drop('Ctch%',axis=1)
    df = df.drop('Y/Tgt',axis=1)
    df = df.drop('Touch',axis=1)
    df = df.drop('Y/Tch',axis=1)
    df = df.drop('YScm',axis=1)

    num_rows = len(df)
    df = df.fillna(0)

    df = convert_datatypes(df)

    # Create training dataframe
    if(num_rows > 1):        
        for i in range(num_rows-1):
            year = df.loc[i,'Year']
            next_year = int(year) + 1

            if(str(next_year) in df['Year'].values):
                next_year_row = df.loc[df['Year'] == str(next_year)]
            else:
                continue
            
            passing_yds = next_year_row['Passing Yds'].unique()[0] * 0.04
            passing_td =  next_year_row['Passing TD'].unique()[0] * ppptd
            picks = next_year_row['Int'].unique()[0] * (-2)
            rush_yds = next_year_row['Rushing Yds'].unique()[0] * 0.1
            rrtd = next_year_row['RRTD'].unique()[0] * 6

            fp = passing_yds + passing_td + picks + rush_yds + rrtd
        
            career_row = df.iloc[0:i+1,:].sum(numeric_only=True, axis=0)

            last_season_row = df.iloc[i,:]

            career_df = pd.DataFrame(career_row)
            last_season_df = pd.DataFrame(last_season_row)

            career_df = career_df.T
            last_season_df = last_season_df.T

            career_df.reset_index(drop=True, inplace=True)
            last_season_df.reset_index(drop=True, inplace=True)

            career_df['Next Year Fantasy Points'] = fp
            
            career_df = normalize_career(career_df,i+1)
            last_season_df = normalize_last(last_season_df)

            career_df.columns = [str(col) + '_career' for col in career_df.columns]
            last_season_df.columns = [str(col) + '_last' for col in last_season_df.columns]

            career_df['Name'] = name

            train_row = pd.concat([career_df,last_season_df],axis = 1)

            if(i == 0):
                train_df = train_row
            else:
                train_df = pd.concat([train_df,train_row], axis=0)

    else:
        train_df = None

    # Create testing dataframe
    career_row = df.iloc[0:num_rows,:].sum(numeric_only=True, axis=0)
    

    last_season_row = df.iloc[num_rows-1,:]

    career_df = pd.DataFrame(career_row)
    last_season_df = pd.DataFrame(last_season_row)

    career_df = career_df.T
    last_season_df = last_season_df.T

    career_df.reset_index(drop=True, inplace=True)
    last_season_df.reset_index(drop=True, inplace=True)

    career_df = normalize_career(career_df,num_rows)
    last_season_df = normalize_last(last_season_df)

    career_df.columns = [str(col) + '_career' for col in career_df.columns]
    last_season_df.columns = [str(col) + '_last' for col in last_season_df.columns]

    career_df['Name'] = name

    test_row = pd.concat([career_df,last_season_df],axis = 1)

    test_df = test_row

    return(train_df,test_df)

def format_df(df):
    # Handle relocated teams
    df.loc[df['Tm'] == 'OAK', 'Tm'] = 'LVR'
    df.loc[df['Tm'] == 'SDG', 'Tm'] = 'LAC'
    df.loc[df['Tm'] == 'STL', 'Tm'] = 'LAR'

    df.loc[df['Tm'] == 'LAC-SDG', 'Tm'] = 'LAC'
    df.loc[df['Tm'] == 'LVR-OAK', 'Tm'] = 'LVR'
    df.loc[df['Tm'] == 'LAR-STL', 'Tm'] = 'LAR'

    num_teams = len(df['Tm'].unique()) - 1

    # Handle 2TM and 3TM in one season
    two_team_index = df.index[df['Tm']== '2TM']
    three_team_index = df.index[df['Tm']== '3TM']

    two_team_err = list()
    
    teams = df['Tm'].unique()

    if('2TM' in teams):
        df = df.drop(labels=two_team_index+1,axis=0)
        # Handle case of 2TM but only played on one team
        if(name not in two_team_err):
            df = df.drop(labels=two_team_index+2,axis=0)
        # Account for 2TM in team list
        num_teams = num_teams - 1

    if('3TM' in teams):
        df = df.drop(three_team_index+1)
        df = df.drop(three_team_index+2)
        df = df.drop(three_team_index+3)
        # Account for 3TM in team list
        num_teams = num_teams - 1

        if(num_teams > 1):
            num_teams = num_teams + 1

    teams = [x for x in teams if x == x]

    # Drop rows for missed seasons
    if('Awards' in df):
        df['Awards'] = df['Awards'].fillna('')
        df = df[df["Awards"].str.contains("Missed season")==False]

        check = any("Missed season" in team for team in teams)
        if(check):
            num_teams = num_teams - 1
    elif('Tm' in df):
        df['Tm'] = df['Tm'].fillna('')
        df = df[df['Tm'].str.contains("Missed season")==False]

        check = any("Missed season" in team for team in teams)
        if(check):
            num_teams = num_teams - 1

    if(num_teams > 1):
        num_teams = num_teams + 1
        
    # Drop career row
    for i in range(num_teams):
        
        df = df.head(-1)
    
    return(df)

# Start at main scrimmage page
url = 'https://www.pro-football-reference.com/years/2021/passing.htm'
base_url = 'https://www.pro-football-reference.com'

player_links = dict()

table = pd.read_html(url, attrs = {'id': 'passing'})[0]

request = requests.get(url)
soup = BeautifulSoup(request.text,features="html.parser")

# Create dict of player links    
for link in soup.findAll('a'):
    match = re.search(r'>(.*?)<',str(link))
    name = match.group(1)
    name = name.rstrip()
    player_url = link.get('href')

    player_links[name] = base_url + player_url

# Sanitize player names
table["Player"] = table["Player"].str.replace("*","")
table["Player"] = table["Player"].str.replace("+","")
table = table.loc[table["Player"] != 'Player']

# Add column with player page URLs
table['hyper_link'] = table['Player'].map(player_links)

print(table)

table.to_csv('passing.csv')

num_rows = len(table)

err = ['Josh Johnson', 'Riley Dixon', 'Ty Long']

for i in range(num_rows):
    if(table['Player'].iat[i] in err):
        continue
    if(i == 0):
        train_buffer, test_buffer = visit_player_page(table['Player'].iat[i],table['hyper_link'].iat[i])
    else:
        train_df, test_df = visit_player_page(table['Player'].iat[i],table['hyper_link'].iat[i])
        train_buffer = pd.concat([train_buffer, train_df],ignore_index=True,axis=0)
        test_buffer = pd.concat([test_buffer, test_df],ignore_index=True,axis=0)

# Post-processing
name = train_buffer.pop('Name')
fp = train_buffer.pop('Next Year Fantasy Points_career')

train_buffer.insert(0, 'Name', name)
train_buffer.insert(1, 'Next Year Fantasy Points', fp)

name2 = test_buffer.pop('Name')
test_buffer.insert(0,'Name',name2)

train_buffer.to_csv('train.csv',index=False)
test_buffer.to_csv('test.csv',index=False)

# Generatre projections
exec(open("predict.py").read())

#train_df, test_df = visit_player_page('Tom Brady','https://www.pro-football-reference.com/players/B/BradTo00.htm')

#train_df.to_csv('train_brady.csv')
#test_df.to_csv('test_brady.csv')
