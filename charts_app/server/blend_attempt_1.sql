use musicproject;


SELECT * FROM chartentries;
SELECT * FROM allentries;

SELECT 
	billboard.chart_name,
    spotify.chart_name,
	billboard.chart_week, 
    spotify.chart_week,
    billboard.title,
    billboard.artist,
    spotify.streams,
    billboard.weeks_on_chart,
    billboard.peak_pos,
    billboard.last_pos
FROM
	(SELECT * FROM allentries WHERE chart_name='Spotify') spotify
LEFT OUTER JOIN
	(SELECT * FROM allentries WHERE chart_name='Billboard') billboard
ON billboard.song_id = spotify.song_id AND datediff(billboard.chart_week, spotify.chart_week) = 9
UNION
SELECT 
	spotify.chart_name,
    billboard.chart_name,
	billboard.chart_week, 
    spotify.chart_week,
    spotify.title,
    spotify.artist,
    spotify.streams,
    billboard.weeks_on_chart,
    billboard.peak_pos,
    billboard.last_pos
FROM
	(SELECT * FROM allentries WHERE chart_name='Spotify') spotify
RIGHT OUTER JOIN
	(SELECT * FROM allentries WHERE chart_name='Billboard') billboard
ON billboard.song_id = spotify.song_id;

SELECT   
	billboard.chart_name,     
    spotify.chart_name,  
    billboard.chart_week,      
    spotify.chart_week,     
    billboard.title,     
    billboard.artist,     
    spotify.streams,     
    billboard.weeks_on_chart,     
    billboard.peak_pos,     
    billboard.last_pos 
FROM  
	(SELECT * FROM allentries WHERE chart_name='Spotify') spotify 
LEFT OUTER JOIN  
	(SELECT * FROM allentries WHERE chart_name='Billboard') billboard 
	ON billboard.song_id = spotify.song_id AND datediff(billboard.chart_week, spotify.chart_week) = 9 
UNION  
SELECT   
	billboard.chart_name,     
    spotify.chart_name,  
    billboard.chart_week,      
    spotify.chart_week,     
    billboard.title,     
    billboard.artist,     
    spotify.streams,     
    billboard.weeks_on_chart,     
    billboard.peak_pos,     
    billboard.last_pos 
FROM  
	(SELECT * FROM allentries WHERE chart_name='Spotify') spotify 
RIGHT OUTER  JOIN  
	(SELECT * FROM allentries WHERE chart_name='Billboard') billboard 
    ON billboard.song_id = spotify.song_id AND datediff(billboard.chart_week, spotify.chart_week) = 9
