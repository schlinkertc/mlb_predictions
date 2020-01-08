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