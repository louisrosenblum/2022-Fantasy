# 2022 Fantasy Script

import pandas as pd
import csv
import numpy as np
import requests
from bs4 import BeautifulSoup
import re

import warnings
warnings.filterwarnings("ignore")

# Define constants
ppr = 1
ppfd = 0

def normalize_last_season(df):

    df = df.drop('Year_last',axis=1)
    df = df.drop('Tm_last',axis=1)
    df = df.drop('Pos_last',axis=1)
    df = df.drop('No._last',axis=1)

    if('AV_last' in df.columns):
        df = df.drop('AV_last',axis=1)

    if('Awards_last' in df.columns):
        df = df.drop('Awards_last',axis=1)
    df = df.drop('A/G_last',axis=1)
    df = df.drop('R/G_last',axis=1)

    df['Rush_last'] = df['Rush_last']/df['G_last']
    df['Rush Yds_last'] = df['Rush Yds_last']/df['G_last']
    df['Rush TD_last'] = df['Rush TD_last']/df['G_last']
    df['Rush 1D_last'] = df['Rush 1D_last']/df['G_last']

    # Handle divide by zero for 0 rush attempts
    if(0 not in df['Rush_last'].values):
        df['Y/A_last'] = df['Rush Yds_last']/df['Rush_last']
    else:
        df['Y/A_last'] = 0

    
    
    df['Rec_last'] = df['Rec_last']/df['G_last']
    df['Rec Yds_last'] = df['Rec Yds_last']/df['G_last']
    df['Rec TD_last'] = df['Rec TD_last']/df['G_last']
    df['Rec 1D_last'] = df['Rec 1D_last']/df['G_last']

    if(0 not in df['Rec_last'].values):
        df['Y/R_last'] = df['Rec Yds_last']/df['Rec_last']
    else:
        df['Y/R_last'] = 0

    
    df['Ctch%_last'] = df['Rec_last']/df['Tgt_last']
    if(0 not in df['Tgt_last'].values):
        df['Y/Tgt_last'] = df['Rec Yds_last']/df['Tgt_last']
    else:
        df['Y/Tgt_last'] = 0
    df['Y/Tch_last'] = df['YScm_last']/df['Touch_last']
    df['Touch_last'] = df['Touch_last']/df['G_last']
    df['Tgt_last'] = df['Tgt_last']/df['G_last']   
    df['YScm_last'] = df['YScm_last']/df['G_last']
    df['RRTD_last'] = df['RRTD_last']/df['G_last']
    df['Fmb_last'] = df['Fmb_last']/df['G_last']
	
    df = df.rename(columns={
    "Age_last": "Last Season Age",
    "Rush Yds_last": "Last Season Rush Yds/G",
    "Rush TD_last": "Last Season Rush TD/G",
    "Rush 1D_last": "Last Season Rush 1D/G",
    "Rush Lng_last": "Last Season Rush Lng",
    "Y/A_last": "Last Season Yds/Att",
    "Tgt_last": "Last Season Tgt/G",
    "Rec_last": "Last Season Rec/G",
    "Rec TD_last": "Last Season Rec TD/G",
    "Rec 1D_last": "Last Season Rec 1D/G",
    "Rec Yds_last": "Last Season Rec Yds/G",
    "Y/R_last": "Last Season Yds/Rec",
    "Rec Lng_last": "Last Season Rec Lng",
    "Y/Tgt_last": "Last Season Yds/Tgt",
    "Y/Tch_last": "Last Season Yds/Tch",
    "Touch_last": "Last Season Touch/G",
    "YScm_last": "Last Season Scrim Yds/G",
    "Fmb_last": "Last Season Fmb/G",
    "RRTD_last": "Last Season TOT TDs/G",
    "Ctch%_last": "Last Season Catch %",
    "Rush_last": "Last Season Att/G"})


    df = df.drop('G_last',axis=1)
    df = df.drop('GS_last',axis=1)
    df = df.drop('Rush Yds/G_last',axis=1)
    df = df.drop('Rec Yds/G_last',axis=1)

    df = df.fillna(0)
    
    return(df)

def normalize_career(df,years):

    df['Age_career'] = df['Age_career']/years

    if('Rush Lng_career' in df.columns):
        df['Rush Lng_career'] = df['Rush Lng_career']/years
    else:
        df['Rush Lng_career'] = 0
    if('Rec Lng_career' in df.columns):
        df['Rec Lng_career'] = df['Rec Lng_career']/years
    else:
        df['Rec Lng_career'] = 0
    
    df['Rush_career'] = df['Rush_career']/df['G_career']
    df['Rush Yds_career'] = df['Rush Yds_career']/df['G_career']

    # Handle Rush TD missing from table
    df['Rush TD_career'] = df['Rush TD_career']/df['G_career']
    df['Rush 1D_career'] = df['Rush 1D_career']/df['G_career']

    # Handle divide by zero for 0 rush attempts
    if(0 not in df['Rush_career'].values):
        df['Y/A_career'] = df['Rush Yds_career']/df['Rush_career']
    else:
        df['Y/A_career'] = 0
        
    df['Tgt_career'] = df['Tgt_career']/df['G_career']
    df['Rec_career'] = df['Rec_career']/df['G_career']
    df['Rec Yds_career'] = df['Rec Yds_career']/df['G_career']
    df['Rec TD_career'] = df['Rec TD_career']/df['G_career']
    df['Rec 1D_career'] = df['Rec 1D_career']/df['G_career']

    # Handle divide by zeros
    if(0 not in df['Rec_career'].values):
        df['Y/R_career'] = df['Rec Yds_career']/df['Rec_career']
    else:
        df['Y/R_career'] = 0
    if(0 not in df['Tgt_career'].values):
        df['Ctch%_career'] = df['Rec_career']/df['Tgt_career']
    else:
        df['Ctch%_career'] = 0
    if(0 not in df['Tgt_career'].values):   
        df['Y/Tgt_career'] = df['Rec Yds_career']/df['Tgt_career']
    else:
        df['Y/Tgt_career'] = 0

    df['Y/Tch_career'] = df['YScm_career']/df['Touch_career']
    df['Touch_career'] = df['Touch_career']/df['G_career']
    df['YScm_career'] = df['YScm_career']/df['G_career']
    df['RRTD_career'] = df['RRTD_career']/df['G_career']
    df['Fmb_career'] = df['Fmb_career']/df['G_career']
    
    
    if('No._career' in df.columns):
        df = df.drop('No._career',axis=1)
    if('Rush Yds/G_career' in df.columns):
        df = df.drop('Rush Yds/G_career',axis=1)
    if('A/G_career' in df.columns):
        df = df.drop('A/G_career',axis=1)
    if('R/G_career' in df.columns):
        df = df.drop('R/G_career',axis=1)
    if('Rec Yds/G_career' in df.columns):
        df = df.drop('Rec Yds/G_career',axis=1)
    if('AV_career' in df.columns):
        df = df.drop('AV_career',axis=1)

    df = df.rename(columns={
    "Age_career": "Average Career Age",
    "Rush Yds_career": "Career Rush Yds/G",
    "Rush TD_career": "Career Rush TD/G",
    "Rush 1D_career": "Career Rush 1D/G",
    "Rush Lng_career": "Career Rush Lng",
    "Y/A_career": "Career Yds/Att",
    "Tgt_career": "Career Tgt/G",
    "Rec_career": "Career Rec/G",
    "Rec TD_career": "Career Rec TD/G",
    "Rec 1D_career": "Career Rec 1D/G",
    "Rec Yds_career": "Career Rec Yds/G",
    "Y/R_career": "Career Yds/Rec",
    "Rec Lng_career": "Career Rec Lng",
    "Y/Tgt_career": "Career Yds/Tgt",
    "Y/Tch_career": "Career Yds/Tch",
    "Touch_career": "Career Touch/G",
    "YScm_career": "Career Scrim Yds/G",
    "Fmb_career": "Career Fmb/G",
    "RRTD_career": "Career TOT TDs/G",
    "Ctch%_career": "Career Catch %",
    "Rush_career": "Career Att/G"})

    if('G_career' in df.columns):
        df = df.drop('G_career',axis=1)
    if('GS_career' in df.columns):
        df = df.drop('GS_career',axis=1)

    if('Pos_career' in df.columns):
        df = df.drop('Pos_career',axis=1)

    df = df.fillna(0)

    return(df)

def visit_player_page(name,url):
    try:
        table = pd.read_html(url, attrs = {'id': 'receiving_and_rushing'})[0]
        pos = 'wr'
    except:
        table = pd.read_html(url, attrs = {'id': 'rushing_and_receiving'})[0]
        pos = 'rb'

    print()
    print('-------------------------------------------------------------------------------------------')
    print(name)

    table = format_df(table,pos)

    # Handle relocated teams
    table.loc[table['Tm'] == 'OAK', 'Tm'] = 'LVR'
    table.loc[table['Tm'] == 'SDG', 'Tm'] = 'LAC'
    table.loc[table['Tm'] == 'STL', 'Tm'] = 'LAR'

    table.loc[table['Tm'] == 'LAC-SDG', 'Tm'] = 'LAC'
    table.loc[table['Tm'] == 'LVR-OAK', 'Tm'] = 'LVR'
    table.loc[table['Tm'] == 'LAR-STL', 'Tm'] = 'LAR'


    # Handle 2TM and 3TM in one season
    two_team_index = table.index[table['Tm']== '2TM']
    three_team_index = table.index[table['Tm']== '3TM']

    num_teams = len(table['Tm'].unique()) - 1
    
    teams = table['Tm'].unique()

    two_team_err = ['Jaydon Mickens','Tremon Smith']

    if('2TM' in teams):
        table = table.drop(labels=two_team_index+1,axis=0)
        # Handle case of 2TM but only played on one team
        if(name not in two_team_err):
            table = table.drop(labels=two_team_index+2,axis=0)
        # Account for 2TM in team list
        num_teams = num_teams - 1

    if('3TM' in teams):
        table = table.drop(three_team_index+1)
        table = table.drop(three_team_index+2)
        table = table.drop(three_team_index+3)
        # Account for 3TM in team list
        num_teams = num_teams - 1



    if(num_teams > 1):
        num_teams = num_teams + 1

    teams = [x for x in teams if x == x]

    # Drop rows for missed seasons
    if('Awards' in table):
        table['Awards'] = table['Awards'].fillna('')
        table = table[table["Awards"].str.contains("Missed season")==False]

        check = any("Missed season" in team for team in teams)
        if(check):
            num_teams = num_teams - 1
    elif('Tm' in table):
        table['Tm'] = table['Tm'].fillna('')
        table = table[table['Tm'].str.contains("Missed season")==False]

        check = any("Missed season" in team for team in teams)
        if(check):
            num_teams = num_teams - 1
        

    # Drop career row
    for i in range(num_teams):
        table = table.head(-1)

    num_rows = len(table)

    table = convert_datatypes(table)

    table = table.fillna(0)

    fp = (table['Rec'].iat[0] * ppr) + (table['RRTD'].iat[0] * 6) + (table['YScm'].iat[0] /10) + ((table['Rush 1D'].iat[0] + table['Rec 1D'].iat[0])*ppfd)

    request = requests.get(url)
    soup = BeautifulSoup(request.text,features="html.parser")

    try:
        match = re.search(r'href="(.*?)">College Stats<',str(soup))
        college_url = match.group(1)
        college_url = college_url.rstrip()
    except:
        return(None)

    try:
        table = pd.read_html(college_url, attrs = {'id': 'rushing'})[0]
        pos = 'rb'
    except:
        try:
            table = pd.read_html(college_url, attrs = {'id': 'receiving'})[0]
            pos = 'wr'
        # Handle 404 college player page
        except:
            return(None)

    table = format_college(table,pos)

    last_season_row = table.iloc[-1,:]

    last_season_row = normalize_row(last_season_row)

    last_season_row = last_season_row.drop(['Year','School','Conf','Class','Pos'])

    career_row = table.iloc[:,:].sum(numeric_only=True, axis=0)

    career_row = normalize_row(career_row)

    # Merge career and last season series
    career_row = career_row.add_suffix('_career')
    last_season_row = last_season_row.add_suffix('_last')
    train_row = pd.concat([career_row,last_season_row],axis = 0)

    labels = train_row.keys()

    labels = labels.insert(0,'Name')
    labels = labels.insert(1,'Next Year Fantasy Points')

    train_row['Name'] = name
    train_row['Next Year Fantasy Points'] = fp

    train_row = train_row.reindex(labels)

    print(train_row)

    df = pd.DataFrame([train_row.tolist()], columns=train_row.index)

    #print(df)

    return(df)

def normalize_row(df):

    df['Att'] = df['Att']/df['G']
    df['Rush Yds'] = df['Rush Yds']/df['G']
    df['Yds/Att'] = df['Rush Yds']/df['Att']
    df['Rush TDs'] = df['Rush TDs']/df['G']
    df['Rec'] = df['Rec']/df['G']
    df['Rec Yds'] = df['Rec Yds']/df['G']
    df['Yds/Rec'] = df['Rec Yds']/df['Rec']
    df['Rec TDs'] = df['Rec TDs']/df['G']
    df['Plays'] = df['Plays']/df['G']
    df['Scrim Yds'] = df['Scrim Yds']/df['G']
    df['Yds/Touch'] = df['Scrim Yds']/df['Plays']
    df['RRTD'] = df['RRTD']/df['G']

    df = df.rename({"Att": "Att/G",
                    "Rush Yds": "Rush Yds/G",
                    "Rush TDs": "Rush TDs/G",
                    "Rec": "Rec/G",
                    "Rec Yds": "Rec Yds/G",
                    "Rec TDs": "Rec TDs/G",
                    "Plays": "Touch/G",
                    "Scrim Yds": "Scrim Yds/G",
                    "RRTD": "RRTD/G"})

    df = df.drop('G')

    return(df)

def format_college(df,pos):
    df.columns = df.columns.droplevel()

    #print(df.columns)

    df = df[df.G.notnull()]

    df = df.fillna(0)

    if(pos == 'rb'):
        df.columns.values[7] = 'Rush Yds'
        df.columns.values[8] = 'Yds/Att'
        df.columns.values[9] = 'Rush TDs'
        df.columns.values[11] = 'Rec Yds'
        df.columns.values[12] = 'Yds/Rec'
        df.columns.values[13] = 'Rec TDs'
        df.columns.values[15] = 'Scrim Yds'
        df.columns.values[16] = 'Yds/Touch'
        df.columns.values[17] = 'RRTD'
    elif(pos == 'wr'):
        df.columns.values[7] = 'Rec Yds'
        df.columns.values[8] = 'Yds/Rec'
        df.columns.values[9] = 'Rec TDs'
        df.columns.values[11] = 'Rush Yds'
        df.columns.values[12] = 'Yds/Att'
        df.columns.values[13] = 'Rush TDs'
        df.columns.values[15] = 'Scrim Yds'
        df.columns.values[16] = 'Yds/Touch'
        df.columns.values[17] = 'RRTD'

    # Convert datatypes
    df['Att'] = pd.to_numeric(df['Att'], downcast = "float",errors='coerce')
    df['Rush Yds'] = pd.to_numeric(df['Rush Yds'], downcast = "float",errors='coerce')
    df['Rec'] = pd.to_numeric(df['Rec'], downcast = "float",errors='coerce')
    df['Rec Yds'] = pd.to_numeric(df['Rec Yds'], downcast = "float",errors='coerce')
    df['Plays'] = pd.to_numeric(df['Plays'], downcast = "float",errors='coerce')
    df['Scrim Yds'] = pd.to_numeric(df['Scrim Yds'], downcast = "float",errors='coerce')

    # Calculate rate statistics for higher precision
    df['Yds/Att'] = df['Rush Yds']/df['Att']
    df['Yds/Rec'] = df['Rec Yds']/df['Rec']
    df['Yds/Touch'] = df['Scrim Yds']/df['Plays']
    
    
    #print(df.columns)
    
    #with pd.option_context('display.max_rows', None,
                       #'display.max_columns', None,
                       #'display.precision', 3,
                       #): print(df)

    return(df)

def format_df(df,pos):
    df.columns = df.columns.droplevel()

    if(pos == 'wr'):
        df.columns.values[9] = 'Rec Yds'
        df.columns.values[11] = 'Rec TD'
        df.columns.values[12] = 'Rec 1D'
        df.columns.values[13] = 'Rec Lng'
        df.columns.values[15] = 'Rec Yds/G'
        df.columns.values[19] = 'Rush Yds'
        df.columns.values[20] = 'Rush TD'
        df.columns.values[21] = 'Rush 1D'
        df.columns.values[22] = 'Rush Lng'
        df.columns.values[24] = 'Rush Yds/G'

    elif(pos == 'rb'):
        df.columns.values[8] = 'Rush Yds'
        df.columns.values[9] = 'Rush TD'
        df.columns.values[10] = 'Rush 1D'
        df.columns.values[11] = 'Rush Lng'
        df.columns.values[13] = 'Rush Yds/G'
        df.columns.values[17] = 'Rec Yds'
        df.columns.values[19] = 'Rec TD'
        df.columns.values[20] = 'Rec 1D'
        df.columns.values[21] = 'Rec Lng'
        df.columns.values[23] = 'Rec Yds/G'

    return(df)

def convert_datatypes(df):
        
    # Convert column datatypes
    df['Age'] = pd.to_numeric(df['Age'], downcast = "float",errors='coerce')
    df['Tgt'] = pd.to_numeric(df['Tgt'], downcast = "float")
    df['G'] = pd.to_numeric(df['G'], downcast = "float")
    df['Rec Yds'] = pd.to_numeric(df['Rec Yds'], downcast = "float")
    df['Rush'] = pd.to_numeric(df['Rush'], downcast = "float")
    df['Ctch%'] = pd.to_numeric(df['Ctch%'], downcast = "float",errors='coerce')
    df['Rush Yds'] = pd.to_numeric(df['Rush Yds'], downcast = "float")
    df['Rec TD'] = pd.to_numeric(df['Rec TD'], downcast = "float")
    df['Rush TD'] = pd.to_numeric(df['Rush TD'], downcast = "float")
    df['Rec 1D'] = pd.to_numeric(df['Rec 1D'], downcast = "float")
    df['Rush 1D'] = pd.to_numeric(df['Rush 1D'], downcast = "float")
    df['Touch'] = pd.to_numeric(df['Touch'], downcast = "float")
    df['Y/Tch'] = pd.to_numeric(df['Y/Tch'], downcast = "float")
    df['Fmb'] = pd.to_numeric(df['Fmb'], downcast = "float")
    df['Rec'] = pd.to_numeric(df['Rec'], downcast = "float",errors='coerce')
    df['YScm'] = pd.to_numeric(df['YScm'], downcast = "float",errors='coerce')
    df['RRTD'] = pd.to_numeric(df['RRTD'], downcast = "float",errors='coerce') 

    return(df)

# Start at main scrimmage page
url = 'https://www.pro-football-reference.com/years/2021/scrimmage.htm'
base_url = 'https://www.pro-football-reference.com'

player_links = dict()

table = pd.read_html(url, attrs = {'id': 'receiving_and_rushing'})[0]

request = requests.get(url)
soup = BeautifulSoup(request.text,features="html.parser")

# Create dict of player links    
for link in soup.findAll('a'):
    match = re.search(r'>(.*?)<',str(link))
    name = match.group(1)
    name = name.rstrip()
    player_url = link.get('href')

    player_links[name] = base_url + player_url

# Drop multindex 
table.columns = table.columns.droplevel()
table = table.drop(columns=['Rk','Tm','GS','R/G','Y/G','A/G'])

# Sanitize player names
table["Player"] = table["Player"].str.replace("*","")
table["Player"] = table["Player"].str.replace("+","")
table = table.loc[table["Player"] != 'Player']

# Add column with player page URLs
table['hyper_link'] = table['Player'].map(player_links)

# Rename duplicate columns
table.columns.values[6] = 'Rec Yds'
table.columns.values[8] = 'Rec TD'
table.columns.values[9] = 'Rec 1D'
table.columns.values[10] = 'Rec Lng'
table.columns.values[14] = 'Rush Yds'
table.columns.values[15] = 'Rush TD'
table.columns.values[16] = 'Rush 1D'
table.columns.values[17] = 'Rush Lng'
table.columns.values[18] = 'Yds/Att'

# Convert columns to numeric
table['Tgt'] = pd.to_numeric(table['Tgt'], downcast = "float")
table['G'] = pd.to_numeric(table['G'], downcast = "float")
table['Rec Yds'] = pd.to_numeric(table['Rec Yds'], downcast = "float")
table['Att'] = pd.to_numeric(table['Att'], downcast = "float")
table['Ctch%'] = table['Ctch%'].str.rstrip('%').astype('float') / 100.0
table['Rush Yds'] = pd.to_numeric(table['Rush Yds'], downcast = "float")
table['Rec TD'] = pd.to_numeric(table['Rec TD'], downcast = "float")
table['Rec 1D'] = pd.to_numeric(table['Rec 1D'], downcast = "float")
table['Touch'] = pd.to_numeric(table['Touch'], downcast = "float")
table['Y/Tch'] = pd.to_numeric(table['Y/Tch'], downcast = "float")
table['Fmb'] = pd.to_numeric(table['Fmb'], downcast = "float")
table['Rec'] = pd.to_numeric(table['Rec'], downcast = "float",errors='coerce')
table['YScm'] = pd.to_numeric(table['YScm'], downcast = "float",errors='coerce')
table['RRTD'] = pd.to_numeric(table['RRTD'], downcast = "float",errors='coerce')

# Convert to rate statistics
table['Tgt'] = table['Tgt']/table['G']
table['Rec'] = table['Rec']/table['G']
table['Rec Yds'] = table['Rec Yds']/table['G']
table['Att'] = table['Att']/table['G']
table['Rush Yds'] = table['Rush Yds']/table['G']
table['Rec TD'] = table['Rec TD']/table['G']
table['Rec 1D'] = table['Rec 1D']/table['G']
table['Yds/Att'] = table['Rush Yds']/table['Att']
table['Touch'] = table['Touch']/table['G']
table['YScm'] = table['YScm']/table['G']
table['Y/Tch'] = table['YScm']/table['Touch']
table['RRTD'] = table['RRTD']/table['G']
table['Fmb'] = table['Fmb']/table['G']

table = table.rename(columns={
    "Tgt": "Tgt/G",
    "Rec": "Rec/G",
    "Rec Yds": "Rec Yds/G",
    "Y/R": "Yds/Rec",
    "Y/Tgt": "Yds/Tgt",
    "Att": "Att/G",
    "Rush Yds": "Rush Yds/G",
    "Rec TD": "Rec TD/G",
    "Rec 1D": "Rec 1D/G",
    "Touch": "Touch/G",
    "YScm": "Scrim Yds/G",
    "Y/Tch": "Yds/Touch",
    "RRTD": "RRTD/G",
    "Fmb": "Fmb/G"})


# Print table
#print(table)

# Write table to CSV
table.to_csv('scrim.csv')

num_rows = len(table)

for i in range(num_rows):
    if(i == 0):
        train_buffer = visit_player_page(table['Player'].iat[i],table['hyper_link'].iat[i])
    else:
        train_df = visit_player_page(table['Player'].iat[i],table['hyper_link'].iat[i])
        train_buffer = pd.concat([train_buffer, train_df],ignore_index=True,axis=0)

# Post-processing
#name = train_buffer.pop('Name')
#fp = train_buffer.pop('Next Year Fantasy Points')

#train_buffer.insert(0, 'Name', name)
#train_buffer.insert(1, 'Next Year Fantasy Points', fp)

#name2 = test_buffer.pop('Name_career')
#test_buffer.insert(0,'Name',name2)

train_buffer = train_buffer.fillna(0)

train_buffer.to_csv('train.csv',index=False)
#test_buffer.to_csv('test.csv',index=False)

# Generatre projections
#exec(open("predict.py").read())


