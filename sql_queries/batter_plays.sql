select
	plays.batter_id,
    people.primaryPosition_type,
    plays.game_id,
    plays.startTime
from 
	MLB_Stats.plays
inner join
	MLB_Stats.people
	on 
    plays.batter_id=people.id
order by 
	plays.startTime desc;