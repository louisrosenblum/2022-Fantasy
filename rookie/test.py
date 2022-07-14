# 2022 Fantasy Script

import pandas as pd
import csv
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import time

import warnings
warnings.filterwarnings("ignore")

delay = 1.5

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

def format_df(df,pos):
    df.columns = df.columns.droplevel()

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

    print(df)

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

    return(df)

def visit_player_page(url,name):
    try:
        table = pd.read_html(url, attrs = {'id': 'receiving'})[0]
        pos = 'wr'
    except:
        try:
            table = pd.read_html(url, attrs = {'id': 'rushing'})[0]
            pos = 'rb'
        except:
            return None

    table = format_df(table,pos)
    
    #with pd.option_context('display.max_rows', None,
                       #'display.max_columns', None,
                       #'display.precision', 3,
                       #): print(table)
    
    table['Year'] = table['Year'].str.replace('*','')

    grade = table.loc[table['Year'] == '2021', 'Class'].iloc[0]

    eligible = ((grade == 'JR') or (grade == 'SR') or (len(table) >= 3))

    # Skip player if not at junior standing
    if(not eligible):
        return(None)

    last_season_row = table.iloc[-1,:]

    last_season_row = normalize_row(last_season_row)

    last_season_row = last_season_row.drop(['Year','School','Conf','Class','Pos'])

    career_row = table.iloc[:,:].sum(numeric_only=True, axis=0)

    career_row = normalize_row(career_row)

    # Merge career and last season series
    career_row = career_row.add_suffix('_career')
    last_season_row = last_season_row.add_suffix('_last')
    test_row = pd.concat([career_row,last_season_row],axis = 0)

    labels = test_row.keys()

    labels = labels.insert(0,'Name')
    test_row['Name'] = name

    test_row = test_row.reindex(labels)

    print(test_row)

    df = pd.DataFrame([test_row.tolist()], columns=test_row.index)

    return(df)
    
# Start at main scrimmage page
rec_url = 'https://www.sports-reference.com/cfb/years/2021-receiving.html'
rush_url = 'https://www.sports-reference.com/cfb/years/2021-rushing.html'
base_url = 'https://www.sports-reference.com'

player_links = dict()

rec_table = pd.read_html(rec_url, attrs = {'id': 'receiving'})[0]
rush_table = pd.read_html(rush_url, attrs = {'id': 'rushing'})[0]

request = requests.get(rec_url)
soup = BeautifulSoup(request.text,features="html.parser")

# Create dict of player links    
for link in soup.findAll('a'):
    match = re.search(r'>(.*?)<',str(link))
    name = match.group(1)
    name = name.rstrip()
    player_url = link.get('href')

    player_links[name] = base_url + player_url

request = requests.get(rush_url)
soup = BeautifulSoup(request.text,features="html.parser")

# Create dict of player links    
for link in soup.findAll('a'):
    match = re.search(r'>(.*?)<',str(link))
    name = match.group(1)
    name = name.rstrip()

    if(name not in player_links.keys()):
        player_url = link.get('href')

        player_links[name] = base_url + player_url

# Drop multi-index
rec_table.columns = rec_table.columns.droplevel()
rush_table.columns = rush_table.columns.droplevel()

player_list = list()

# Iterate over Receiving table
for i in range(len(rec_table)):
    time.sleep(delay)
    name = rec_table.loc[i,'Player']
    name = name.replace('*','')

    #print(name)

    if(name == 'Player'):
        continue

    player_list.append(name)
    
    url = player_links[name]

    df = visit_player_page(url,name)

    if(i == 0):
        test_buffer = df
    else:
        test_buffer = pd.concat([test_buffer, df],ignore_index=True,axis=0)

# Iterate over rushing table
for i in range(len(rush_table)):
    time.sleep(delay)
    name = rush_table.loc[i,'Player']
    name = name.replace('*','')

    #print(name)

    if(name == 'Player') or (name in player_list):
        continue
    
    url = player_links[name]

    df = visit_player_page(url,name)

    test_buffer = pd.concat([test_buffer, df],ignore_index=True,axis=0)

test_buffer = test_buffer.fillna(0)    
test_buffer.to_csv('test.csv',index=False)
