select 
	id,dayNight,
    temp,wind,
    `condition`,
    venue_id,
    home_probablePitcher,
    away_probablePitcher,
    gameNumber,doubleHeader,
    season,homeTeam_id,
    awayTeam_id
from 
	MLB_Stats.games g
where
	g.`type`='R';