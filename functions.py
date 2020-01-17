# gamePks are stored in CSVs in the project directory
# This function reads the CSVs and stores them in memory as a dictionary
import pandas as pd
import numpy as np
from os import walk
import re
import csv

def get_gamePks(seasons):
    """
    uses the 'season' endpoint of the mlb api to get gamePks and write them to csvs for each season.
    """
    import statsapi as mlb
    import csv
    import time
    import sys
    
    gamePks_path = "/Users/schlinkertc/code/mlb_predictions/gamePks"
    
    from os import walk
    import re
    
    # walk the gamePks directory to find the seasons that we've already added 
    f = []
    for (dirpath, dirnames, filenames) in walk(gamePks_path):
        f.extend(filenames)
        break
    years = [re.findall('[^.csv]+',x) for x in f]
    already_added = [int(item) for sublist in years for item in sublist if item[0] in ['1','2']]
    
    seasons = list(set(seasons)-set(already_added))
    
    gamePks = {}
    for season in seasons:
        mlb.get('season',{'sportId':1,'seasonId':str(season)})
        try:
            games = mlb.schedule(start_date=f'02/01/{season}',
                                    end_date=f'11/30/{season}',
                                    sportId=1)
            pks = [x['game_id'] for x in games]
            print(pks[0])
            
            gamePks[season]=pks
            print(len(gamePks))
            with open(gamePks_path + f'/{season}.csv', 'w',newline='') as myfile:
                wr = csv.writer(myfile,quoting=csv.QUOTE_ALL)
                wr.writerow(gamePks[season])
        except ValueError as err:
            print(f'{season} failed. Error: {err} Waiting 10 seconds before resuming')
            time.sleep(10)
            #seasons.append(season)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
            
        
    return gamePks   

def read_gamePks():
    gamePks_path = "/Users/schlinkertc/code/mlb_predictions/gamePks"
    f = []
    for (dirpath, dirnames, filenames) in walk(gamePks_path):
        f.extend(filenames)
        break
    pk_paths = [gamePks_path + '/' + x for x in f if x[0]!= '.']
    
    gamePks = {}
    for path in pk_paths:
        season = re.findall('/gamePks/([^.csv]+)',path)
        with open(path, 'r') as f:
            reader = csv.reader(f)
            seasonPks = list(reader)
        gamePks[season[0]] = [item for sublist in seasonPks for item in sublist]
    return gamePks

def getGame_df():    
    game_df = pd.read_csv('games_file.csv')

    game_df['wind'].fillna('unknown mph',inplace=True)

    game_df['wind_speed']=game_df.apply(lambda x: x['wind'].split('mph')[0],axis=1)

    game_df['wind_speed'].replace('unknown ',np.nan,inplace=True)

    game_df['wind_speed']=game_df.apply(lambda x: int(x['wind_speed']) if type(x['wind_speed'])==str else x['wind_speed'],axis=1)

    game_df['wind_direction']=game_df.apply(lambda x: x['wind'].split('mph')[1],axis=1)

    def parse_windDir(string):
        try:
            string = string.split(', ')[1]
        except:
            pass
        if string == '':
            string='Calm'
        if string=='none':
            string='Calm'
        if string=='None':
            string='Calm'
        return string 

    game_df['wind_direction']=game_df.apply(lambda x: parse_windDir(x['wind_direction']),axis=1)
    game_df.drop(columns=['wind'],inplace=True)

    return game_df
def load_dataset(session):
    """
    Takes in a sql alch session, returns df with game scores added. merges with 'ID' column.
    """
    df = pd.read_csv('dataset.csv')
    game_scores = session.execute("""select 
                                         games.id,
                                         max(plays.homeScore) as home_score,
                                         max(plays.awayScore) as home_score
                                     from
                                         MLB_Stats.games
                                     inner join
                                         MLB_Stats.plays
                                         on
                                         games.id=plays.game_id
                                     where
                                         games.`type`='R'
                                     group by 
                                         games.id;""").fetchall()
    game_scores=pd.DataFrame.from_records(game_scores,columns=['ID','home_score','away_score'])

    df=pd.merge(right=game_scores,
            left=df,
            right_on='ID',
            left_on='ID')
    return df
