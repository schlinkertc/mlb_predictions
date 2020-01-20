select 
	games.id,
    max(plays.homeScore) as home_score,
    max(plays.awayScore) as home_score,
from
	MLB_Stats.games
inner join
	MLB_Stats.plays
    on
    games.id=plays.game_id
where
	games.`type`='R'
group by 
	games.id;