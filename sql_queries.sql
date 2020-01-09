-- total regular season games
select pk from MLB_Stats.games where `season`=2018;

-- home runs grouped by player
select batter_id, count(*) as home_runs froam MLB_Stats.plays where eventType='home_run' group by batter_id;

select * from MLB_Stats.games where `type`='R' limit 50;

select * from MLB_Stats.teams;