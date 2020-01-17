# gamePks are stored in CSVs in the project directory
# This function reads the CSVs and stores them in memory as a dictionary
from os import walk
import re
import csv
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