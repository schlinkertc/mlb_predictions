import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,DateTime,Date,Time,Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import config

## Create the base
Base = declarative_base()

#_sql_alchemy_connection = (
                                #f'mysql+mysqlconnector://'
                                #f'{config.user}:{config.password}'
                                #f'@{config.host}:{config.port}'
                                #f'/{config.schema}'
                           #)
## Create the engine 
#db = sqlalchemy.create_engine(_sql_alchemy_connection,
                              #echo = False,
                              #connect_args = {'ssl_disabled' : True})



# Declare mapping for the game table 
class Game(Base):
    __tablename__ = 'games'
    __table_args__ = {'extend_existing': True}
    
    pk = Column(Integer)
    type = Column(String(1))
    doubleHeader = Column(String(1))
    id = Column(String(150), primary_key=True,unique=True)
    gamedayType = Column(String(1))
    tiebreaker = Column(String(1))
    gameNumber = Column(Integer)
    calenderEventId = Column(String(50))
    season = Column(Integer)
    
    dateTime = Column(DateTime)
    originalDate = Column(Date)
    dayNight = Column(String(12))
    time = Column(Time)
    
    abstractGameState = Column(String(12))
    codedGameState = Column(String(3))
    detailedState = Column(String(12))
    statusCode = Column(String(3))
    abstractGameCode = Column(String(3))
    
    homeTeam_id = Column(Integer)
    awayTeam_id = Column(Integer)
    
    condition = Column(String(25))
    temp = Column(Integer)
    wind = Column(String(50))
    
    venue_id = Column(Integer)
    
    home_probablePitcher = Column(Integer)
    away_probablePitcher = Column(Integer)
    
    def __repr__(self): 
        return "<Game(pk='%s',id='%s')>" % (
                        self.pk, self.id)
    
# Declare the mapping for the Plays table 
class Play(Base):
    __tablename__= 'plays'
    __table_args__ = {'extend_existing': True} 
    
    id = Column(String(200),primary_key=True,unique=True)
    type = Column(String(10))
    event = Column(String(25))
    eventType = Column(String(25))
    description = Column(String(250))
    rbi = Column(Integer)
    awayScore = Column(Integer)
    homeScore = Column(Integer)
    
    atBatIndex = Column(Integer)
    halfInning = Column(String(10))
    inning = Column(Integer)
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    isComplete = Column(Boolean)
    isScoringPlay = Column(Boolean)
    hasReview = Column(Boolean)
    hasOut = Column(Boolean)
    captivatingIndex = Column(Integer)
    
    batter_id = Column(Integer)
    pitcher_id = Column(Integer)
    
    count_balls = Column(Integer)
    count_strikes = Column(Integer)
    count_outs = Column(Integer)
    
    num_pitches = Column(Integer)
    num_actions = Column(Integer)
    num_runners = Column(Integer)
    
    #game_pk = Column(Integer,ForeignKey('games.pk'),nullable=False)
    game_id = Column(String(150),ForeignKey('games.id'))
    
    game = relationship("Game",back_populates="plays")
    
    def __repr__(self):
        return "<Play(game_id='%s',atBatIndex='%s')>" % (
                     self.game_id,self.atBatIndex)

Game.plays = relationship(
    "Play",order_by=Play.id,back_populates='game')

class Team(Base):
    __tablename__ = 'teams'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    venue_id = Column(Integer)
    teamCode = Column(String(10))
    abbreviation = Column(String(10))
    teamName = Column(String(25))
    locationName = Column(String(25))
    league_id = Column(Integer)
    division_id = Column(Integer)
    
    def __repr__(self):
        return "<Team(name='%s')>" % self.name

###
# Functions for creating and adding records
###
# Create instances of the mapped class for games and plays  
def create_gameRecord_playsRecords(pk,session,commit=True):
    """
    This function takes in a gamepk and a sql alchemy session, calls the 'game' api endpoint, and turns the information into a
    mapped class instance for that game as well as all the plays in that game. When commit=True, the 
    function will also add these instances to a sqlalchemy session and commit them to the database. 
    """
    import statsapi as mlb
    from datetime import datetime
    import time
    already_added_pk = [item for sublist in db.execute('select pk from games').fetchall() for item in sublist]
    
    if int(pk) not in already_added_pk:
        api_call = mlb.get('game',{'gamePk':pk})

        gameData = api_call['gameData']
        game = gameData['game']
        _datetime = gameData['datetime']
        status = gameData['status']
        weather = gameData['weather']
        probablePitchers = gameData['probablePitchers']

        liveData = api_call['liveData']
        all_plays = liveData['plays']['allPlays']
    
        already_added = [item for sublist in db.execute('select id from games').fetchall() for item in sublist]
    

        game_record = Game(pk=game['pk'],
                     type=game['type'],
                     doubleHeader=game['doubleHeader'],
                     id=game['id'],
                     gamedayType=game['gamedayType'],
                     tiebreaker=game['tiebreaker'],
                     gameNumber=game['gameNumber'],
                     calenderEventId=game['calendarEventID'],
                     season=game['season'],

                     dateTime=datetime.strptime(_datetime['dateTime'],'%Y-%m-%dT%H:%M:%SZ'),
                     originalDate=datetime.strptime(_datetime['originalDate'],"%Y-%m-%d"),
                     dayNight=_datetime['dayNight'],
                     time=datetime.strptime(_datetime['time']+_datetime['ampm'],"%H:%M%p"),

                     abstractGameState=status['abstractGameState'],
                     codedGameState=status['codedGameState'],
                     detailedState=status['detailedState'],
                     statusCode=status['statusCode'],
                     abstractGameCode=status['abstractGameCode'],

                     homeTeam_id=gameData['teams']['home']['id'],
                     awayTeam_id=gameData['teams']['away']['id'],

                     condition=weather.get('condition','null'),
                     temp=weather.get('temp','null'),
                     wind=weather.get('wind','null'),

                     venue_id=gameData['venue']['id'],

                     home_probablePitcher=probablePitchers.get('home',{'null':'null'}).get('id','null'),
                     away_probablePitcher=probablePitchers.get('away',{'null':'null'}).get('id','null') 
                     )
        play_records = []
        for play in all_plays:
            result = play['result']
            about = play['about']
            batter = play.get('matchup',{'batter':'null'})['batter']
            pitcher = play.get('matchup',{'pitcher':'null'})['pitcher']
            count = play['count']

            play_record = Play(id=str(game['pk'])+game['id']+str(about['atBatIndex']),
                              type=result['type'],
                              event=result['event'],
                              eventType=result.get('eventType','null'),
                              description=result.get('description','null'),
                              rbi=result.get('rbi','null'),
                              awayScore=result.get('awayScore','null'),
                              homeScore=result.get('homeScore','null'),

                              atBatIndex=about.get('atBatIndex','null'),
                              halfInning=about['halfInning'],
                              inning=about['inning'],
                              startTime=datetime.strptime(about.get('startTime','1900-01-01T01:01:1.0Z'),'%Y-%m-%dT%H:%M:%S.%fZ'),
                              endTime=datetime.strptime(about.get('endTime','1900-01-01T01:01:01.0Z'),'%Y-%m-%dT%H:%M:%S.%fZ'),
                              isComplete=about.get('isComplete','null'),
                              isScoringPlay=about.get('isScoringPlay','null'),
                              hasReview=about.get('hasReview','null'),
                              hasOut=about.get('hasOut','null'),
                              captivatingIndex=about.get('captivatingIndex','null'),

                              batter_id=batter.get('id','null'),
                              pitcher_id=pitcher.get('id','null'),

                              count_balls=count.get('balls','null'),
                              count_strikes=count.get('striks','null'),
                              count_outs=count.get('outs','null'),

                              num_pitches=len(play['pitchIndex']),
                              num_actions=len(play['actionIndex']),
                              num_runners=len(play['runners']),

                              game_id=game['id'] 
                              )
            play_records.append(play_record)
            
        if commit:
            session.add(game_record)
            session.commit()

            session.add_all(play_records)
            session.commit()
    else:
        pass
    #return game_record,play_records
    
def create_addTeam(team_ids,session):
    team_query = session.query(Team).all()
    already_added = [instance.id for instance in team_query]
    
    team_records=[]
    for team_id in team_ids:
        if team_id not in already_added:
            team = mlb.get('team',{'teamId':team_id})['teams'][0]

            team_record = Team(id=team['id'],
                              name=team['name'],
                              venue_id=team['venue']['id'],
                              teamCode=team['teamCode'],
                              abbreviation=team['abbreviation'],
                              teamName=team['teamName'],
                              locationName=team['locationName'],
                              league_id=team['league']['id'],
                              division_id=team.get('division',{'id':'null'})['id'])

            team_records.append(team_record)
        session.add_all(team_records)
        session.commit()
    else:
        print('duplicate')