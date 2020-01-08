-- home runs grouped by player
select batter_id, count(*) as home_runs from MLB_Stats.plays where eventType='home_run' group by batter_id