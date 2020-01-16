import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,DateTime,Date,Time,Boolean,Float
from sqlalchemy import ForeignKey,and_
from sqlalchemy.orm import relationship
import config
import statsapi as mlb

# _sql_alchemy_connection = (
#                                 f'mysql+mysqlconnector://'
#                                 f'{config.user}:{config.password}'
#                                 f'@{config.host}:{config.port}'
#                                 f'/{config.schema}'
#                            )
# ## Create the engine 
# db = sqlalchemy.create_engine(_sql_alchemy_connection,
#                               echo = False,
#                               connect_args = {'ssl_disabled' : True,})

# ## Create the base
Base = declarative_base()

class cumulative_stats(Base):
    __tablename__ = 'cumulative_stats'
    __table_args__ = {'extend_existing': True}
    
    player_id = Column(Integer,ForeignKey('people.id'),primary_key=True)
    game_id = Column(String(150),ForeignKey('games.id'),primary_key=True)
    
    play = relationship('Play',back_populates='people')
    
Person.plays = relationship("PersonPlayLink",order_by=Play.startTime,back_populates='player',lazy='dynamic')
Play.people = relationship("PersonPlayLink",back_populates='play')

def relevant_stats2(self,game_record,session,limit=1000):    
    import numpy as np
    from datetime import datetime
    date=datetime.strftime(game_record.dateTime,'%Y%m%d')
    
    probable_starters = [game_record.home_probablePitcher,game_record.away_probablePitcher]
    stat_line = {}
    
    if self.primaryPosition_type in ['Hitter','Outfielder','Infielder','Catcher']:
        query = session.execute(f"""select
            g.id,
            p.id,
            p.`event`,
            p.halfInning,
            p.inning,
            p.atBatIndex,
            p.hasOut,
            p.RBI,
            p.count_outs,
            p.num_pitches
        from 
            MLB_Stats.games g
        right join
            MLB_Stats.plays p
            on 
            g.id=p.game_id
        where
            p.batter_id={self.id}
            and 
            date(g.`dateTime`)<date({date})
            and
            g.type='R'
        order by 
            p.startTime desc;""").fetchall()
    
    if self.primaryPosition_type=='Pitcher':
        query = session.execute(f"""select
            g.id,
            p.id,
            p.`event`,
            p.halfInning,
            p.inning,
            p.atBatIndex,
            p.hasOut,
            p.RBI,
            p.count_outs,
            p.num_pitches
        from 
            MLB_Stats.games g
        right join
            MLB_Stats.plays p
            on 
            g.id=p.game_id
        where
            p.pitcher_id={self.id}
            and 
            date(g.`dateTime`)<date({date})
            and
            g.type='R'
        order by 
            p.startTime desc;""").fetchall()
        
    plays=([
        {'game_id':q[0],'play_id':q[1],
         'event':q[2],'halfInning':q[3],
         'inning':q[4],'atBatIndex':q[5],
         'hasOut':q[6],'RBI':q[7],
         'count_outs':q[8],
         'num_pitches':q[9]} 
        for q in query])
    games={x[0] for x in query}

    
    singles = [x for x in plays if x['event']=='Single']
    doubles = [x for x in plays if x['event']=='Double']
    triples = [x for x in plays if x['event']=='Triple']
    home_runs = [x for x in plays if x['event']=='Home Run']
    walks = [x for x in plays if x['event']=='Walk']
    strikeouts = [x for x in plays if x['event'] in ['Strikeout','Strikeout Double Play']]
    HBP = [x for x in plays if x['event']=='Hit By Pitch']
    GDP = [x for x in plays if x['event']=='Grounded Into DP']
    IBB = [x for x in plays if x['event']=='Intent Walk']
    sac = [x for x in plays if x['event'] in ['Sac Bunt','Sac Fly']]
    interference = [x for x in plays if x['event']=='Catcher Interference']
    LO = [x for x in plays if x['event']=='Lineout']
    PO = [x for x in plays if x['event']=='Pop Out']
    FO = [x for x in plays if x['event']=='Flyout']
    GO = [x for x in plays if x['event']=='Groundout']
    
    ## pitcher stats 
    #starts
    #for hitters, this will mean they're the leadoff batter
    GS = {(x['inning'],x['game_id']) for x in plays if x['inning']==1}
    #games finished isn't adding up correctly yet. I think it's because walk-offs aren't counted
#     GF = {(x['inning'],x['game_id']) for x in plays 
#           if x['inning']==max([p.inning for p in x.game.plays]) 
#           and x.count_outs==3}        
    plays_with_outs = [x for x in plays if x['hasOut']==True]
    double_plays = [x for x in plays if x['event']=='Grounded Into DP' or 'Double Play' in x['event']]
    triple_plays = [x for x in plays if x['event']=='Triple Play']
    outs = len(plays_with_outs)+len(double_plays)+(len(triple_plays)*2)
    
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
    stat_line['RBIs']=sum([x['RBI'] for x in plays])
    stat_line['GDP']=len(GDP)
    stat_line['IBB']=len(IBB)
    stat_line['sac']=len(sac)
    stat_line['LO']=len(LO)
    stat_line['PO']=len(PO)
    stat_line['FO']=len(FO)
    stat_line['GO']=len(GO)
    stat_line['pitches_perPA']=np.mean([x['num_pitches'] for x in plays])
    
    stat_line['GS']=len(GS)
    #stat_line['GF']=len(GF)
        
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
