import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,DateTime,Date,Time,Boolean,Float
from sqlalchemy import ForeignKey,and_
from sqlalchemy.orm import relationship
import config
import statsapi as mlb

_sql_alchemy_connection = (
                                f'mysql+mysqlconnector://'
                                f'{config.user}:{config.password}'
                                f'@{config.host}:{config.port}'
                                f'/{config.schema}'
                           )
## Create the engine 
db = sqlalchemy.create_engine(_sql_alchemy_connection,
                              echo = False,
                              connect_args = {'ssl_disabled' : True,})

## Create the base
Base = declarative_base()

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
    
##################
# Create schema for a GameTeamLink that includes up to 40 active players on the roster
################## 
class GameTeamLink(Base):
    __tablename__ = 'game_team_link'
    __table_args__ = {'extend_existing': True}
    
    game_id = Column(String(150),ForeignKey('games.id'),primary_key=True)
    team_id = Column(Integer,ForeignKey('teams.id'),primary_key=True)
    
    # add roster at the time of game 
    player_1_id = Column(Integer)
    player_2_id = Column(Integer)
    player_3_id = Column(Integer)
    player_4_id = Column(Integer)
    player_5_id = Column(Integer)
    player_6_id = Column(Integer)
    player_7_id = Column(Integer)
    player_8_id = Column(Integer)
    player_9_id = Column(Integer)
    player_10_id = Column(Integer)
    player_11_id = Column(Integer)
    player_12_id = Column(Integer)
    player_13_id = Column(Integer)
    player_14_id = Column(Integer)
    player_15_id = Column(Integer)
    player_16_id = Column(Integer)
    player_17_id = Column(Integer)
    player_18_id = Column(Integer)
    player_19_id = Column(Integer)
    player_20_id = Column(Integer)
    player_21_id = Column(Integer)
    player_22_id = Column(Integer)
    player_23_id = Column(Integer)
    player_24_id = Column(Integer)
    player_25_id = Column(Integer)
    player_26_id = Column(Integer)
    player_27_id = Column(Integer)
    player_28_id = Column(Integer)
    player_29_id = Column(Integer)
    player_30_id = Column(Integer)
    player_31_id = Column(Integer)
    player_32_id = Column(Integer)
    player_33_id = Column(Integer)
    player_34_id = Column(Integer)
    player_35_id = Column(Integer)
    player_36_id = Column(Integer)
    player_37_id = Column(Integer)
    player_38_id = Column(Integer)
    player_39_id = Column(Integer)
    player_40_id = Column(Integer)
    
    #relationships
    game = relationship('Game',back_populates='teams')
    team = relationship('Team',back_populates='games')

# update game and team tables 
Game.teams = relationship("GameTeamLink",back_populates='game')
Team.games = relationship("GameTeamLink",back_populates='team')

# Person table rough
class Person(Base):
    __tablename__ = 'people'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    fullName = Column(String(25))
    firstName = Column(String(25))
    lastName = Column(String(25))
    primaryNumber = Column(Integer)
    birthDate = Column(DateTime)
    currentAge = Column(Integer)
    birthCity = Column(String(25))
    birthCountry = Column(String(25))
    height = Column(String(25))
    weight = Column(Integer)
    active = Column(Boolean)
    primaryPosition_code = Column(String(10))
    primaryPosition_name = Column(String(25))
    primaryPosition_type = Column(String(25))
    primaryPosition_abbreviation = Column(String(25))
    gender = Column(String(5))
    isPlayer = Column(Boolean)
    isVerified = Column(Boolean)
    draftYear = Column(Integer)
    mlbDebutDate = Column(DateTime)
    batSide = Column(String(10))
    pitchHand = Column(String(10))
    nameSlug = Column(String(30))
    fullFMLName = Column(String(50))
    strikeZoneTop = Column(Float)
    strikeZoneBottom = Column(Float)
    
    def __repr__(self):
        return "<Person(nameSlug='%s')>" % self.nameSlug
    
class PersonPlayLink(Base):
    __tablename__='people_plays'
    __table_args__={'extend_existing':True}
    
    player_id = Column(Integer,ForeignKey('people.id'),primary_key=True)
    play_id = Column(String(200),ForeignKey('plays.id'),primary_key=True)
    
    player = relationship('Person',back_populates='plays')
    play = relationship('Play',back_populates='people')
    
Person.plays = relationship("PersonPlayLink",order_by=Play.startTime,back_populates='player',lazy='dynamic')
Play.people = relationship("PersonPlayLink",back_populates='play')
    

###################################
# Adding attributes to classes to make it easier to access info. Could be adjusted later
###################################
def players(self,session):
    for attr, value in self.__dict__.items():
        if attr.startswith("player") and value >0:
            yield session.query(Person).filter(Person.id==value).one()
GameTeamLink.players = players

def gtl__repr__(self):
    return "<GameTeam(game_id='%s',team_id='%s')>" % (
                        self.game_id,self.team_id)
GameTeamLink.__repr__ = gtl__repr__

# adding a game_players method to the Games table to return a list of active player ids
def game_players(self,session):
    home_away = {self.homeTeam_id:'home',self.awayTeam_id:'away'}
    return {home_away[x.team_id]:x.players(session) for x in self.teams}
Game.game_players = game_players

# adding another Game method to see all players in a game
def all_players(self):
    return [item for sublist in self.game_players() for item in sublist]
Game.all_players = all_players

#################################################################
# Functions for creating and adding records
#################################################################
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
                              event=result.get('event','null'),
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
                              locationName=team.get('locationName','null'),
                              league_id=team.get('league',{'id':'null'})['id'],
                              division_id=team.get('division',{'id':'null'})['id'])

            team_records.append(team_record)
        session.add_all(team_records)
        session.commit()

        
# Series of functions to create and add GameTeamLink records        
def get_roster_inputs(query):   
    roster_inputs = []
    for instance in query.all():
        roster_input_dict = {'date':datetime.strftime(instance.dateTime,'%Y-%m-%d'),
                             'season':instance.season,
                             'homeTeam':instance.homeTeam_id,
                             'awayTeam':instance.awayTeam_id,
                             }
        roster_inputs.append(roster_input_dict)
        
    return roster_inputs

def get_roster(roster_input_dict):
    #player_list = ['player_'+str(x) for x in range(1,41)]
    home = mlb.get('team_roster',
                   {'teamId':roster_input_dict['homeTeam'],
                    'rosterType':'active',
                    'season':roster_input_dict['season'],
                    'date':roster_input_dict['date']
                   })['roster']
    home_roster_ids = [x['person']['id'] for x in home]
    player_list = ['player_'+str(x) for x in range(1,len(home_roster_ids)+1)]
    home_roster_dict = {x:y for x,y in zip(player_list,home_roster_ids)}
    home_roster_dict['teamId'] = roster_input_dict['homeTeam']
    
    away = mlb.get('team_roster',
                   {'teamId':roster_input_dict['awayTeam'],
                    'rosterType':'active',
                    'season':roster_input_dict['season'],
                    'date':roster_input_dict['date']
                   })['roster']
    away_roster_ids = [x['person']['id'] for x in away]
    player_list = ['player_'+str(x) for x in range(1,len(away_roster_ids)+1)]
    away_roster_dict = {x:y for x,y in zip(player_list,away_roster_ids)}
    away_roster_dict['teamId']=roster_input_dict['awayTeam']
    return home_roster_dict,away_roster_dict

def create_GameTeamLink(game_ids):
    records = []
    for game_id in game_ids:
        game_query = session.query(Game).filter_by(id=game_id)
        roster_input_dicts = get_roster_inputs(game_query)
        home_roster,away_roster = get_roster(roster_input_dicts[0])
        rosters = [home_roster,away_roster]
#       rosters.append(roster)
        
        for roster in rosters:
            game_team_record = GameTeamLink(game_id=game_id,
                                            team_id=roster['teamId'],

                                            player_1_id = roster.get('player_1','null'),
                                            player_2_id = roster.get('player_2','null'),
                                            player_3_id = roster.get('player_3','null'),
                                            player_4_id = roster.get('player_4','null'),
                                            player_5_id = roster.get('player_5','null'),
                                            player_6_id = roster.get('player_6','null'),
                                            player_7_id = roster.get('player_7','null'),
                                            player_8_id = roster.get('player_8','null'),
                                            player_9_id = roster.get('player_9','null'),
                                            player_10_id = roster.get('player_10','null'),
                                            player_11_id = roster.get('player_11','null'),
                                            player_12_id = roster.get('player_12','null'),
                                            player_13_id = roster.get('player_13','null'),
                                            player_14_id = roster.get('player_14','null'),
                                            player_15_id = roster.get('player_15','null'),
                                            player_16_id = roster.get('player_16','null'),
                                            player_17_id = roster.get('player_17','null'),
                                            player_18_id = roster.get('player_18','null'),
                                            player_19_id = roster.get('player_19','null'),
                                            player_20_id = roster.get('player_20','null'),
                                            player_21_id = roster.get('player_21','null'),
                                            player_22_id = roster.get('player_22','null'),
                                            player_23_id = roster.get('player_23','null'),
                                            player_24_id = roster.get('player_24','null'),
                                            player_25_id = roster.get('player_25','null'),
                                            player_26_id = roster.get('player_26','null'),
                                            player_27_id = roster.get('player_27','null'),
                                            player_28_id = roster.get('player_28','null'),
                                            player_29_id = roster.get('player_29','null'),
                                            player_30_id = roster.get('player_30','null'),
                                            player_31_id = roster.get('player_31','null'),
                                            player_32_id = roster.get('player_32','null'),
                                            player_33_id = roster.get('player_33','null'),
                                            player_34_id = roster.get('player_34','null'),
                                            player_35_id = roster.get('player_35','null'),
                                            player_36_id = roster.get('player_36','null'),
                                            player_37_id = roster.get('player_37','null'),
                                            player_38_id = roster.get('player_38','null'),
                                            player_39_id = roster.get('player_39','null'),
                                            player_40_id = roster.get('player_40','null')
                                           )
            records.append(game_team_record)
    return records

def chunk(n,list_to_chunk):
    """
    takes in n, and a list to chunk. returns a list of lists with n length. The last chunk size may or may not 
    be equal to n. 
    """
    return [ list_to_chunk[i:i+n] for i in range(0,len(list_to_chunk),n) ]

def create_add_GameTeamLink(session,start=0,stop=None,chunk_size=50):   
    # collect game_ids from the games table 
    ids_list_test = session.query(Game.id).all()[start:stop]
    ids_list_test=[item for sublist in ids_list_test for item in sublist]

    # collect game_ids from the game_link table
    # I'll naturally have duplicates so I think I'll make it a set 
    already_added = list({item for sublist in session.query(GameTeamLink.game_id).all() for item in sublist})

    games_to_get = [game for game in ids_list_test if game not in already_added]
    
    list_of_chunks = chunk(chunk_size,games_to_get)
    count = 1
    
    for _chunk in list_of_chunks:
        try:
            print(f'starting chunk {count} out of {len(list_of_chunks)}')
            games_teams_to_add = create_GameTeamLink(_chunk)

            session.add_all(games_teams_to_add)
            session.commit()

            count = count+1
        except:
            print('chunk failed. Rolling back the session and trying the next chunk')
            session.rollback()
            continue 

def create_personRecord(personId):
    api_call = mlb.get('person',{'personId':personId})

    person = api_call['people'][0]
    person['birthDate'] = person.get('birthDate','1900-01-01')

    
    person_record = Person(id=person.get('id','null'),
                           fullName=person.get('fullName','null'),
                           firstName=person.get('firstName','null'),
                           lastName=person.get('lastName','null'),
                           primaryNumber=person.get('primaryNumber','null'),
                           birthDate=datetime.strptime(person.get('birthDate','1900-01-01'),'%Y-%m-%d'),
                           currentAge=person.get('currentAge','null'),
                           birthCity=person.get('birthCity','null'),
                           birthCountry=person.get('birthCountry','null'),
                           height=person.get('height','null'),
                           weight=person.get('weight','null'),
                           active=person.get('active','null'),
                           primaryPosition_code=person.get('primaryPosition',{'code':'null'})['code'],
                           primaryPosition_name=person.get('primaryPosition',{'name':'null'})['name'],
                           primaryPosition_type=person.get('primaryPosition',{'type':'null'})['type'],
                           primaryPosition_abbreviation=person.get('primaryPosition',{'abbreviation':'null'})['abbreviation'],
                           gender=person.get('gender','null'),
                           isPlayer=person.get('isPlayer','null'),
                           isVerified=person.get('isVerified','null'),
                           draftYear=person.get('draftYear','null'),
                           mlbDebutDate=datetime.strptime(person.get('mlbDebutDate','1900-01-01'),'%Y-%m-%d'),
                           batSide=person.get('batSide',{'description':'null'})['description'],
                           pitchHand=person.get('pitchHand',{'description':'null'})['description'],
                           nameSlug=person.get('nameSlug','null'),
                           fullFMLName=person.get('fullFMLName','null'),
                           strikeZoneTop=person.get('strikeZoneTop','null'),
                           strikeZoneBottom=person.get('strikeZoneBottom','null'),
                          )
    return person_record

def create_addPerson(session,personIds,chunk_size=50):
    already_added = [item for sublist in session.query(Person.id).all() for item in sublist]
    records=[]
    
    people_to_get = [person for person in personIds if person not in already_added]
    
    list_of_chunks = chunk(chunk_size,people_to_get)
    count=1
    
    for _chunk in list_of_chunks:
        try:
            print(f'starting chunk {count} out of {len(list_of_chunks)}')
            records = [create_personRecord(x) for x in _chunk]
            session.add_all(records)
            session.commit()
            count+=1
        except:
            print('chunk failed. rolling back session and trying the next chunk')
            session.rollback()
            count+=1
            continue
            

def relevant_stats(self,game_record,session,limit=None):
    """
    Method of the Person class. Takes in a game record 
    """
    date=game_record.dateTime
    probable_starters = [game_record.home_probablePitcher,game_record.away_probablePitcher]
    stat_line = {}
    
    if self.primaryPosition_type in ['Hitter','Outfielder','Infielder','Catcher']:
        query = session.query(Game,Play).\
                        filter(Game.id==Play.game_id).\
                        filter(and_(Game.type=='R',Game.dateTime<date)).\
                        filter(Play.batter_id==self.id).\
                        order_by(Game.dateTime.desc()).\
                        all()[:limit]
    if self.primaryPosition_type=='Pitcher':
        query = session.query(Game,Play).\
                        filter(Game.id==Play.game_id).\
                        filter(and_(Game.type=='R',Game.dateTime<date)).\
                        filter(Play.pitcher_id==self.id).\
                        order_by(Game.dateTime.desc()).\
                        all()[:limit]
    games={x[0] for x in query}
    plays=[x[1] for x in query]
    
    singles = [x for x in plays if x.event=='Single']
    doubles = [x for x in plays if x.event=='Double']
    triples = [x for x in plays if x.event=='Triple']
    home_runs = [x for x in plays if x.event=='Home Run']
    walks = [x for x in plays if x.event=='Walk']
    strikeouts = [x for x in plays if x.event in ['Strikeout','Strikeout Double Play']]
    HBP = [x for x in plays if x.event=='Hit By Pitch']
    GDP = [x for x in plays if x.event=='Grounded Into DP']
    IBB = [x for x in plays if x.event=='Intent Walk']
    sac = [x for x in plays if x.event in ['Sac Bunt','Sac Fly']]
    interference = [x for x in plays if x.event=='Catcher Interference']
    LO = [x for x in plays if x.event=='Lineout']
    PO = [x for x in plays if x.event=='Pop Out']
    FO = [x for x in plays if x.event=='Flyout']
    GO = [x for x in plays if x.event=='Groundout']
    
    ## pitcher stats 
    #starts
    #for hitters, this will mean they're the leadoff batter
    GS = {(x.inning,x.game_id) for x in plays if x.inning==1}
    #games finished isn't adding up correctly yet. I think it's because walk-offs aren't counted
    GF = {(x.inning,x.game_id) for x in plays 
          if x.inning==max([p.inning for p in x.game.plays]) 
          and x.count_outs==3}        
    plays_with_outs = [x for x in plays if x.hasOut==True]
    double_plays = [x for x in plays if x.event=='Grounded Into DP' or 'Double Play' in x.event]
    triple_plays = [x for x in plays if x.event=='Triple Play']
    outs = len(plays_with_outs)+len(double_plays)+(len(triple_plays)*2)
    
    #winning/losing/tied
    #how many times does a pitcher enter the game when team is losing/winning
    
#     inning_score = [{'game':x.game_id,'atBat':x.atBatIndex,'lead':(x.awayScore-x.homeScore)}
#                  if x.halfInning=='bottom'
#                  else 
#                  {'game':x.game_id,'atBat':x.atBatIndex,'lead':(x.homeScore-x.awayScore)}
#                  for x in plays 
#                  if x.inning==min(p.inning for p in x.game.plays if p.pitcher_id==self.id)
#                  ]
    
    
    stat_line['Position_type']=self.primaryPosition_type
    stat_line['games']=len(games)
    stat_line['PA'] = len(plays)
    stat_line['AB'] = len(plays)-len(walks)-len(HBP)-len(IBB)-len(sac)-len(interference)
    stat_line['hits']=len(singles)+len(doubles)+len(triples)+len(home_runs)
    stat_line['singles']=len(singles)
    stat_line['doubles']=len(doubles)
    stat_line['triples']=len(triples)
    stat_line['home_runs']=len(home_runs)
    stat_line['walks']=len(walks)
    stat_line['strikeouts']=len(strikeouts)
    stat_line['HBP']=len(HBP)
    stat_line['RBIs']=sum([x.rbi for x in plays])
    stat_line['GDP']=len(GDP)
    stat_line['IBB']=len(IBB)
    stat_line['sac']=len(sac)
    stat_line['LO']=len(LO)
    stat_line['PO']=len(PO)
    stat_line['FO']=len(FO)
    stat_line['GO']=len(GO)
    
    stat_line['GS']=len(GS)
    stat_line['GF']=len(GF)
        
    if 'Pitcher' in stat_line['Position_type']:
        stat_line['IP']=outs/3
    # is this pitcher generally a starter?    
    # pitchers who start the game less than 12th of their appearances are labeled relief
        if stat_line['GS']<stat_line['games']/12:
            stat_line['Position_type']='Pitcher_relief'
        else:
            stat_line['Position_type']='Pitcher_starter'
    
    # is this pitcher TODAY's starter?
    if self.id in probable_starters:
        stat_line['Position_type']='Probable_startingPitcher'            
    
    if 'Pitcher' not in stat_line['Position_type']:
        stat_line['IP']=0
    #saves/holds
    #stats for relief pitchers
    #stat_line['save_situations']=len([x for x in inning_score])       
    return stat_line

Person.relevant_stats = relevant_stats

def game_player_stats(self,session,limit=None):
    home_player_stats = [x.relevant_stats(self,session,limit) for x in self.game_players(session)['home']]
    away_player_stats = [x.relevant_stats(self,session,limit) for x in self.game_players(session)['away']]
    
    #home_score = max([x.homeScore for x in self.plays])
    #away_score = max([x.awayScore for x in self.plays])
    
    for x in home_player_stats:
        x['home']=1
        #x['score']=home_score
    for y in away_player_stats:     
        y['home']=-1
        #y['score']=away_score
    
    player_stats = [home_player_stats, away_player_stats]
    
    return [item for sublist in player_stats for item in sublist]

Game.player_stats = game_player_stats

def player_agg_stats(self,session,limit=None):
    game_dicts=self.player_stats(session,limit)
    player_dicts=[]
    for player in game_dicts:
        if player['games']==0:
            player['games']=-1
        player_dict = {'ID':self.id}
        player_dict['position'] = player['Position_type']
        player_dict['home'] = player['home']
        
        player_dict['PA_per_Game'] = player['PA']/player['games']
        
        try:
            player_dict['BA'] = player['hits']/player['AB']
        except ZeroDivisionError:
            player_dict['BA']=0
            
        try:
            player_dict['OBP'] = (
                                    (player['hits']+player['walks']+player['HBP']+player['IBB'])
                                    /
                                    (player['AB']+player['walks']+player['HBP']+player['IBB']+player['sac'])
                                  )
        except ZeroDivisionError:
            player_dict['OBP']=0
        
        try:
            player_dict['SLG'] = (
                                    ((player['singles']*1)+(player['doubles']*2)+
                                    (player['triples']*1)+(player['home_runs']*1))
                                    /
                                    (player['AB'])
                                  )
        except ZeroDivisionError:
            player_dict['SLG']=0
            
        if player['walks']+player['HBP']>0:
            player_dict['SOW'] = player['strikeouts']/(player['walks']+player['HBP'])
        else:
            player_dict['SOW'] = 0
        
        try:
            player_dict['H9'] = 9*player['hits']/player['IP']
            player_dict['HR9'] = 9*player['home_runs']/player['IP']
            player_dict['SO9'] = 9*player['strikeouts']/player['IP']
            player_dict['WHIP'] = player['walks']+player['HBP']+player['hits']/player['IP']
        except (ZeroDivisionError,KeyError):
            player_dict['H9'] = 0
            player_dict['HR9'] = 0
            player_dict['SO9'] = 0
            player_dict['WHIP'] = 0
        
        # proportion of groundouts, flyouts, popouts, lineouts to ABs
        if player['AB']>0:
            player_dict['GO_O'] = player['GO']/player['AB']
            player_dict['FO_O'] = player['FO']/player['AB']
            player_dict['PO_O'] = player['PO']/player['AB']
            player_dict['LO_O'] = player['LO']/player['AB']
        else:
            player_dict['GO_O'] = 0
            player_dict['FO_O'] = 0
            player_dict['PO_O'] = 0
            player_dict['LO_O'] = 0
        player_dicts.append(player_dict)
    return player_dicts

Game.agg_stats = player_agg_stats
