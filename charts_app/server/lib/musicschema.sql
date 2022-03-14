SET @@global.sql_mode= '';
-- creation of database
CREATE DATABASE IF NOT EXISTS musicproject;
-- using database
USE musicproject; 
DROP TABLE IF EXISTS rollingstonechartentries;
DROP TABLE IF EXISTS billboardchartentries;
DROP TABLE IF EXISTS spotifychartentries;
DROP TABLE IF EXISTS chartentries;
DROP TABLE IF EXISTS songs;
DROP PROCEDURE IF EXISTS create_billboard_entries;
DROP PROCEDURE IF EXISTS create_spotify_entries;
DROP PROCEDURE IF EXISTS create_chart_entry;
DROP PROCEDURE IF EXISTS create_chart_entries;
DROP PROCEDURE IF EXISTS create_song_entry;
DROP FUNCTION IF EXISTS return_song_id;
DROP FUNCTION IF EXISTS return_chart_entry_id;
DROP PROCEDURE IF EXISTS view_all_chart_entries;
DROP PROCEDURE IF EXISTS view_spotify_entries;
DROP PROCEDURE IF EXISTS view_billboard_entries;
DROP PROCEDURE IF EXISTS view_songs_on_both_charts;
DROP PROCEDURE IF EXISTS view_spotify_only_songs;
DROP PROCEDURE IF EXISTS view_billboard_only_songs;
DROP PROCEDURE IF EXISTS search_by_song;
DROP PROCEDURE IF EXISTS search_by_artist;

# DESIGN DECISION: gonna get rid of the artists and genre entities because
# they don't really serve a purpose for the purposes of this database. 
# Functionally, all I imagine the user using this database for is searching
# "rnb" or maybe "one direction" and seeing what songs pop up. Nothing too involved.
# they don't need to know the genre description. I guess an argument can be made for
# artists having their own entities like maybe having record label attached to them
# but that's not the databse I wanna create. They can just be attributes in the songs table.
CREATE TABLE IF NOT EXISTS songs
(
  song_id		INT 			PRIMARY KEY AUTO_INCREMENT,
  title 		VARCHAR(255)    NOT NULL,
  artist		VARCHAR(255)    NOT NULL  
);

# DESIGN DECISION: https://stackoverflow.com/questions/20864054/implement-specialization-in-er-diagram
# Another design decision: Added week attribute bc had the thought of what happens to the old charts when re-run the Python script
# to have the latest charts? Don't wanna overwwrite old songs and chart entries, so better to have a weekly record hehe.
# NEW DESIGN DECISION: getting rid of superclass bc it's too much overhead. It's useful for things like employee where it's 
# useful to have an overall employee chart without the specializations... but for a jumbled up giant chart with chart entries
# belonging to different music charts, it doesn't make sense. I considered, maybe it's useful for enforcing that each
# chart entry MUST have chart_week, song_id, position, but... having to create a chart entry so i can have something
# to reference in each individual chart is too much overhead i think? PLUS, if for some reason i wanna combine 
# charts together, it's just a matter of a select/union statement. If by some mistake they dont have one of the "required"
# fields, it's not gonna make the code not run. hmmmm. VERY open to going back to this though if someone suggests it.
# ACTUALLY JUST KIDDING. IM KEEPING THE HIERARCHY. https://www.cs.uct.ac.za/mit_notes/database/htmls/chp07.html#mapping-specializationgeneralization-to-relational-tables
# the locaiton->province/country/etc example convinved me. each chart entry is still a chart entry.
# http://www.agiledata.org/essays/mappingObjects.html#ComparingTheStrategies
-- table creation
CREATE TABLE chartentries
(
  chart_entry_id	INT			PRIMARY KEY AUTO_INCREMENT,
  chart_name		VARCHAR(50) NOT NULL,
  position			INT			NOT NULL,
  chart_week		DATE		NOT NULL,
  standard_week     DATE		NOT NULL,
  song_id			INT			NOT NULL,
  streams			INT,
  weeks_on_chart	INT,
  peak_pos			INT,
  last_pos 			INT			DEFAULT NULL,
  FOREIGN KEY (song_id) REFERENCES songs(song_id)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

DELIMITER //

# TODO: each chart has more attributes of their own. decide how u wanna show that.
# also i dont think this logic is right. i need to access the song table first and then the chart tbale ? and also handle weekly records 
# sooo TODO: FIX THIS
-- search procedures (read operation)
CREATE PROCEDURE search_by_artist (
	IN artist_param	VARCHAR(75)
)
	BEGIN
		SELECT * FROM chartentries JOIN songs ON songs.song_id = chartentries.song_id WHERE songs.artist = artist_param;
	END // 

# TODO: again, decide how to show info from each chart.
CREATE PROCEDURE search_by_song (
	IN song_param	VARCHAR(100)
)
	BEGIN
		SELECT * FROM chartentries JOIN songs ON songs.song_id = chartentries.song_id WHERE songs.title = song_param;
	END // 

CREATE FUNCTION return_song_id (
	song_name_param			VARCHAR(100),
    artist_param			VARCHAR(100)
 )
RETURNS INT 
DETERMINISTIC READS SQL DATA
	BEGIN
		DECLARE id_value INT;
		SELECT song_id INTO id_value
			FROM songs
			WHERE title = song_name_param AND artist=artist_param;
		RETURN (id_value);
	END //

CREATE FUNCTION return_chart_entry_id (
	chart_week_param		DATE,
	song_id_param			INT,
    position_param			INT
 )
RETURNS INT 
DETERMINISTIC READS SQL DATA
	BEGIN
		DECLARE id_value INT;
		
		SELECT chart_entry_id INTO id_value
			FROM chartentries
			WHERE chart_week = chart_week_param AND song_id=song_id_param AND position=position_param;
		RETURN (id_value);
	END //

CREATE PROCEDURE create_song_entry (
	IN title_param	VARCHAR(100),
    IN artist_param	VARCHAR(100)
)
	BEGIN	
		IF NOT EXISTS (SELECT * FROM songs WHERE title=title_param AND artist=artist_param) 
			THEN INSERT IGNORE INTO songs(title, artist) VALUES (title_param, artist_param);
            END IF;
	END //

# Creates a new song entry into the songs table if the song doesn't already exist. 
# An existing song is determined by comparing both song title and artist name.
# Note: This doesn't indicate if the procedure fails to create a new entry when the song already exists.
CREATE PROCEDURE create_chart_entries (
	IN chart_name_param VARCHAR(50),
    IN chart_week_param DATE,
    IN position_param INT,		
	IN title_param VARCHAR(100),
    IN artist_param VARCHAR(100),	
  	IN streams_param			INT,
  	IN weeks_on_chart_param	INT,
  	IN peak_pos_param			INT,
  	IN last_pos_param 			INT
)
	BEGIN 
		DECLARE song_id_val INT;
        DECLARE standard_week_val DATE;
        
 		CALL create_song_entry(title_param, artist_param);
        SET song_id_val =  return_song_id(title_param, artist_param);
        #https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_week
        #https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_date-format
        SET standard_week_val = str_to_date(concat(yearweek('2022-02-19'), ' Monday'), '%X%V %W');
        
		IF NOT EXISTS (SELECT * FROM chartentries WHERE chart_name = chart_name_param AND song_id=song_id_val AND chart_week=chart_week_param AND position=position_param) 
			THEN INSERT IGNORE INTO chartentries(chart_name, chart_week, standard_week, song_id, position, streams, weeks_on_chart, peak_pos, last_pos) 
            VALUES (chart_name_param, chart_week_param, standard_week_val, song_id_val, position_param, streams_param, weeks_on_chart_param, peak_pos_param, last_pos_param);
            END IF;
	END //

CREATE PROCEDURE view_all_chart_entries(
)
DETERMINISTIC READS SQL DATA
	BEGIN 
		SELECT chartentries.chart_name, chartentries.standard_week, songs.title, songs.artist, songs.song_id, chartentries.position, chartentries.streams, chartentries.weeks_on_chart, chartentries.peak_pos, chartentries.last_pos
        FROM chartentries JOIN songs ON chartentries.song_id = songs.song_id;
	END //
    
CREATE PROCEDURE view_spotify_entries(
)
DETERMINISTIC READS SQL DATA
	BEGIN 
		SELECT chartentries.chart_name, chartentries.chart_week, songs.title, songs.artist, chartentries.position, chartentries.streams 
        FROM chartentries JOIN songs ON chartentries.song_id = songs.song_id WHERE chart_name = 'Spotify';   
	END //
    
CREATE PROCEDURE view_billboard_entries(
)
DETERMINISTIC READS SQL DATA
	BEGIN 
		SELECT chartentries.chart_name, chartentries.chart_week, songs.title, songs.artist, chartentries.position, chartentries.weeks_on_chart, chartentries.peak_pos, chartentries.last_pos
        FROM chartentries JOIN songs ON chartentries.song_id = songs.song_id WHERE chart_name = 'Billboard';   
	END //

CREATE PROCEDURE view_songs_on_both_charts(
)
DETERMINISTIC READS SQL DATA
	BEGIN 
		SELECT songs.title, songs.artist, songs.song_id
		FROM chartentries JOIN songs ON chartentries.song_id = songs.song_id 
        GROUP BY songs.song_id HAVING COUNT(*) > 1;   
	END //

CREATE PROCEDURE view_spotify_only_songs(
)
	BEGIN
		SELECT chartentries.chart_name, chartentries.chart_week, songs.title, songs.artist, songs.song_id, chartentries.position, chartentries.streams
		FROM chartentries JOIN songs ON chartentries.song_id = songs.song_id
        GROUP BY songs.song_id HAVING COUNT(*) = 1 AND chartentries.chart_name = 'Spotify';
    END //
    
CREATE PROCEDURE view_billboard_only_songs(
)
	BEGIN
		SELECT chartentries.chart_name, chartentries.chart_week, songs.title, songs.artist,  songs.song_id, chartentries.position, chartentries.weeks_on_chart, chartentries.peak_pos, chartentries.last_pos
		FROM chartentries JOIN songs ON chartentries.song_id = songs.song_id
        GROUP BY songs.song_id HAVING COUNT(*) = 1 AND chartentries.chart_name = 'Billboard';
    END //
    
DELIMITER // 
DROP PROCEDURE IF EXISTS same_songs_billboard;
CREATE PROCEDURE same_songs_billboard(
)
	BEGIN
		SELECT songs.song_id, songs.title, songs.artist, chartentries.chart_name
		FROM chartentries JOIN songs ON chartentries.song_id = songs.song_id
        GROUP BY songs.song_id HAVING COUNT(*) = 1 AND chartentries.chart_name = 'Billboard';
    END //
    
    
    /*
    	SELECT sp.chart_name, bb.chart_name, sp.chart_week, sp.position, bb.position, sp.streams, bb.weeks_on_chart, bb.peak_pos, bb.last_pos FROM 
		(SELECT * FROM chartentries WHERE chart_name = 'Spotify') as sp
	left  JOIN 
		(SELECT * FROM chartentries WHERE chart_name = 'Billboard') as bb
	ON sp.song_id = bb.song_id
	UNION
	SELECT sp.chart_name, bb.chart_name, sp.chart_week, sp.position, bb.position, sp.streams, bb.weeks_on_chart, bb.peak_pos, bb.last_pos FROM 
		(SELECT * FROM chartentries WHERE chart_name = 'Spotify') as sp
	RIGHT  JOIN 
		(SELECT * FROM chartentries WHERE chart_name = 'Billboard') as bb
	ON sp.song_id = bb.song_id)
    */