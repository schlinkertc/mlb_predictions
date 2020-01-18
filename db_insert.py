## need to import files/libraries, but this is the code i used to put the games in for 2018

game_pk_dict=functions.read_gamePks()

games_2018 = game_pk_dict['2018']
games_2018 = [int(x) for x in games_2018]
game_ids = [item for sublist in session.query(Game.pk).all() for item in sublist]
games_to_add = [x for x in games_2018 if x not in game_ids]


[sql_alch_schema.create_gameRecord_playsRecords(x,session) for x in games_to_add]

current_team_ids = {item for sublist in session.query(Team.id).all() for item in sublist}
new_team_ids = {item for sublist in session.query(Game.homeTeam_id,Game.awayTeam_id).all() for item in sublist}
new_team_ids = new_team_ids-current_team_ids

# sql_alch_schema.create_addTeam(list(new_team_ids),session)

current_gameTeams = {item for sublist in session.query(GameTeamLink.game_id).all() for item in sublist}
current_games = {item for sublist in session.query(Game.id).all() for item in sublist}
gameTeams_to_add = current_games-current_gameTeams
gameTeams_to_add = list(gameTeams_to_add)


# def get_roster_inputs(query):   
#     roster_inputs = []
#     for instance in query.all():
#         roster_input_dict = {'date':datetime.strftime(instance.dateTime,'%Y-%m-%d'),
#                              'season':instance.season,
#                              'homeTeam':instance.homeTeam_id,
#                              'awayTeam':instance.awayTeam_id,
#                              }
#         roster_inputs.append(roster_input_dict)
        
#     return roster_inputs

# def get_roster(roster_input_dict):
#     #player_list = ['player_'+str(x) for x in range(1,41)]
#     home = mlb.get('team_roster',
#                    {'teamId':roster_input_dict['homeTeam'],
#                     'rosterType':'active',
#                     'season':roster_input_dict['season'],
#                     'date':roster_input_dict['date']
#                    })['roster']
#     home_roster_ids = [x['person']['id'] for x in home]
#     player_list = ['player_'+str(x) for x in range(1,len(home_roster_ids)+1)]
#     home_roster_dict = {x:y for x,y in zip(player_list,home_roster_ids)}
#     home_roster_dict['teamId'] = roster_input_dict['homeTeam']
    
#     away = mlb.get('team_roster',
#                    {'teamId':roster_input_dict['awayTeam'],
#                     'rosterType':'active',
#                     'season':roster_input_dict['season'],
#                     'date':roster_input_dict['date']
#                    })['roster']
#     away_roster_ids = [x['person']['id'] for x in away]
#     player_list = ['player_'+str(x) for x in range(1,len(away_roster_ids)+1)]
#     away_roster_dict = {x:y for x,y in zip(player_list,away_roster_ids)}
#     away_roster_dict['teamId']=roster_input_dict['awayTeam']
#     return home_roster_dict,away_roster_dict

# def create_GameTeamLink(game_ids):
#     records = []
#     for game_id in game_ids:
#         game_query = session.query(Game).filter_by(id=game_id)
#         roster_input_dicts = get_roster_inputs(game_query)
#         home_roster,away_roster = get_roster(roster_input_dicts[0])
#         rosters = [home_roster,away_roster]
# #       rosters.append(roster)
        
#         for roster in rosters:
#             game_team_record = GameTeamLink(game_id=game_id,
#                                             team_id=roster['teamId'],

#                                             player_1_id = roster.get('player_1','null'),
#                                             player_2_id = roster.get('player_2','null'),
#                                             player_3_id = roster.get('player_3','null'),
#                                             player_4_id = roster.get('player_4','null'),
#                                             player_5_id = roster.get('player_5','null'),
#                                             player_6_id = roster.get('player_6','null'),
#                                             player_7_id = roster.get('player_7','null'),
#                                             player_8_id = roster.get('player_8','null'),
#                                             player_9_id = roster.get('player_9','null'),
#                                             player_10_id = roster.get('player_10','null'),
#                                             player_11_id = roster.get('player_11','null'),
#                                             player_12_id = roster.get('player_12','null'),
#                                             player_13_id = roster.get('player_13','null'),
#                                             player_14_id = roster.get('player_14','null'),
#                                             player_15_id = roster.get('player_15','null'),
#                                             player_16_id = roster.get('player_16','null'),
#                                             player_17_id = roster.get('player_17','null'),
#                                             player_18_id = roster.get('player_18','null'),
#                                             player_19_id = roster.get('player_19','null'),
#                                             player_20_id = roster.get('player_20','null'),
#                                             player_21_id = roster.get('player_21','null'),
#                                             player_22_id = roster.get('player_22','null'),
#                                             player_23_id = roster.get('player_23','null'),
#                                             player_24_id = roster.get('player_24','null'),
#                                             player_25_id = roster.get('player_25','null'),
#                                             player_26_id = roster.get('player_26','null'),
#                                             player_27_id = roster.get('player_27','null'),
#                                             player_28_id = roster.get('player_28','null'),
#                                             player_29_id = roster.get('player_29','null'),
#                                             player_30_id = roster.get('player_30','null'),
#                                             player_31_id = roster.get('player_31','null'),
#                                             player_32_id = roster.get('player_32','null'),
#                                             player_33_id = roster.get('player_33','null'),
#                                             player_34_id = roster.get('player_34','null'),
#                                             player_35_id = roster.get('player_35','null'),
#                                             player_36_id = roster.get('player_36','null'),
#                                             player_37_id = roster.get('player_37','null'),
#                                             player_38_id = roster.get('player_38','null'),
#                                             player_39_id = roster.get('player_39','null'),
#                                             player_40_id = roster.get('player_40','null')
#                                            )
#             records.append(game_team_record)
#     return records

# def chunk(n,list_to_chunk):
#     """
#     takes in n, and a list to chunk. returns a list of lists with n length. The last chunk size may or may not 
#     be equal to n. 
#     """
#     return [ list_to_chunk[i:i+n] for i in range(0,len(list_to_chunk),n) ]

# def create_add_GameTeamLink(session,start=0,stop=None,chunk_size=50):   
#     # collect game_ids from the games table 
#     ids_list_test = session.query(Game.id).all()[start:stop]
#     ids_list_test=[item for sublist in ids_list_test for item in sublist]

#     # collect game_ids from the game_link table
#     # I'll naturally have duplicates so I think I'll make it a set 
#     already_added = list({item for sublist in session.query(GameTeamLink.game_id).all() for item in sublist})

#     games_to_get = [game for game in ids_list_test if game not in already_added]
    
#     list_of_chunks = chunk(chunk_size,games_to_get)
#     count = 1
    
#     for _chunk in list_of_chunks:
#         try:
#             print(f'starting chunk {count} out of {len(list_of_chunks)}')
#             games_teams_to_add = create_GameTeamLink(_chunk)

#             session.add_all(games_teams_to_add)
#             session.commit()

#             count = count+1
#         except:
#             print('chunk failed. Rolling back the session and trying the next chunk')
#             session.rollback()
#             continue 
# create_add_GameTeamLink(session)

current_people = {item for sublist in session.query(Person.id).all() for item in sublist}
new_people = {item for sublist in session.query(Play.pitcher_id).all() for item in sublist}
new_people = list(new_people-current_people)


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

create_addPerson(session,new_people)

from sqlalchemy.sql.expression import insert

def chunk_insertPeoplePlayLink(db,chunk_size=5000):
    people_plays=db.execute("""select pitcher_id,id from plays;""").fetchall()
    people_plays={tuple(x.values()) for x in people_plays}
    
    print('count down:')
    print(3)
    
    existing=db.execute("""select * from people_plays""").fetchall()
    existing={tuple(x.values()) for x in existing}
    
    print(2)
    
    people_plays=list(people_plays-existing)
    
    print(1)
    
    count=1
    chunks = sql_alch_schema.chunk(chunk_size,people_plays)
    for chunk_ in chunks:
        print(f"chunk {count} of {len(chunks)}")
        insert_stmt=insert(PersonPlayLink,chunk_)
        db.execute(insert_stmt)
        count+=1
