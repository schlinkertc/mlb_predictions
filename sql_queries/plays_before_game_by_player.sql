select
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
	p.pitcher_id=477132
    and 
    date(g.`dateTime`)<date(20190612)
order by 
	p.startTime desc;