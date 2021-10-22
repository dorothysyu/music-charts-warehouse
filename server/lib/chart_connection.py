import pymysql
import scrape_billboard
import scrape_spotify
import csv
import re
from fuzzywuzzy import process
from python_sql_dbconfig import read_db_config


class ChartsConnection:
    def __init__(self, is_test=False):
        self.is_test = is_test
        self.cnx = None
        self.connect()
        self.populate_billboard()
        self.populate_spotify()

    def connect(self):
        """ Connect to MySQL database """
        if self.is_test:
            db_config = read_db_config('tests/testchartsconfig.ini')
        else:
            db_config = read_db_config('lib/chartsconfig.ini')
        try:
            print('Connecting to MySQL database...')
            self.cnx = pymysql.Connection(**db_config)
            if self.cnx.open:
                print('Connection established.')
            else:
                print('Connection failed.')
        except Exception as error:
            print(error)

    def view_all_chart_entries(self):
        cur = self.cnx.cursor()
        cur.callproc('view_all_chart_entries')
        for row in cur.fetchall():
            print(row)
        print("\n")
        cur.close()

    def return_all_chart_entries(self):
        cur = self.cnx.cursor()
        cur.callproc('view_all_chart_entries')
        chart_entries = []
        for row in cur.fetchall():
            chart_entries.append(row)
        cur.close()
        return chart_entries

    def view_spotify(self):
        cur = self.cnx.cursor()
        cur.callproc('view_spotify_entries')
        for row in cur.fetchall():
            print(row)
        print("\n")
        cur.close()

    def view_billboard(self):
        cur = self.cnx.cursor()
        cur.callproc('view_billboard_entries')
        for row in cur.fetchall():
            print(row)
        print("\n")
        cur.close()

    def search_by_song(self):
        cur = self.cnx.cursor()
        song = [input("Enter a song title: ")]
        cur.callproc('search_by_song', song)
        for row in cur.fetchall():
            print(row)
        print("\n")
        cur.close()

    def search_by_artist(self):
        cur = self.cnx.cursor()
        artist = [input("Enter an artist name: ")]
        cur.callproc('search_by_artist', artist)
        for row in cur.fetchall():
            print(row)
        print("\n")
        cur.close()

    # Returns a positive number if the same song, -1 if not.
    def is_same_song(self, song1, artist1, song2, artist2):
        """
        In songs that feature more than one artist in the credits, Billboard and Spotify list it very differently,
        leading to discrepancies. For example, Billboard may list a song entry as 'Richer, Rod Wave Featuring Polo G'
        while Spotify may list it as 'Richer (feat. Polo G), Rod Wave'. This aims to parse two different songs and determine
        if the two songs are the same song.
        Performance concern: Is it better to have SQL do a first pass on determining one-chart-only songs, having it
        output a table with results containing songs that are truly only exclusive to one chart combined with false positives
        and then passing those results through tis function OR should I just skip SQL entirely and have all chart entries
        passed through this function to determine songs that only made one chart?
        """
        # print('is_same_song (%s // %s),\n (%s // %s)' % (song1, artist1, song2, artist2))
        artists_in_track1 = []
        artists_in_track2 = []
        delim = 'feat. | Featuring |, '
        if len(re.split(delim, song1)) > 1:
            song1_no_artist = re.split(delim, song1)[0].strip(" (")
            artists_in_track1.append(re.split(delim, song1)[1].strip(")"))
        else:
            song1_no_artist = song1

        if len(re.split(delim, artist1)) > 1:
            artists_in_track1.append(re.split(delim, artist1)[0].strip(")"))
            artists_in_track1.append(re.split(delim, artist1)[1].strip(")"))
        else:
            artists_in_track1.append(artist1)

        if len(re.split(delim, song2)) > 1:
            song2_no_artist = re.split(delim, song2)[0].strip(" (")
            artists_in_track2.append(re.split(delim, song2)[1].strip(")"))
        else:
            song2_no_artist = song2.strip(" (")
        if len(re.split(delim, artist2)) > 1:
            artists_in_track2.append(re.split(delim, artist2)[0].strip(")"))
            artists_in_track2.append(re.split(delim, artist2)[1].strip(")"))
        else:
            artists_in_track2.append(artist2)

        # print('Looking for "%s" in "%s" and (%s in %s)' % (song2_no_artist, song1_no_artist, artists_in_track2, artists_in_track1))
        return song2_no_artist in song1_no_artist and set(artists_in_track2).issubset(artists_in_track1)

    def has_same_song(self, title, artist):
        """
        Really almost didn't wanna write this because the performance of this is guaranteed horrible
        (O(n(n-C))???)..basically O(n^2)) but will think of a better way to do this. in the future lol
        :param title: Title of the song
        :param artist:
        :param table: List that represents SQL table containing columns song_id, title, artist.
        :return:
        """
        found_same = False
        cur = self.cnx.cursor()
        cur.callproc('same_songs_billboard')
        for row in cur.fetchall():
            # print(row)
            title2 = row[1]
            artist2 = row[2]
            print(title2 + ' , ' + artist2)
            print(self.is_same_song(title, artist, title2, artist2))
        #        if is_same_song(title, artist, title2, artist2):
        #            return True
        print("\n")
        cur.close()
        return found_same

    def fuzzy_is_same_song(self, str1, str2):
        str1 = "4 Da Gang 42 Dugg & Roddy Ricch"
        str1 = "4 Da Gang (with Roddy Ricch) 42 Dugg"
        Ratio = fuzz.ratio(Str1.lower(), Str2.lower())
        Partial_Ratio = fuzz.partial_ratio(Str1.lower(), Str2.lower())
        Token_Sort_Ratio = fuzz.token_sort_ratio(Str1, Str2)
        Token_Set_Ratio = fuzz.token_set_ratio(Str1, Str2)
        print(Ratio)
        print(Partial_Ratio)
        print(Token_Sort_Ratio)
        print(Token_Set_Ratio)

    def create_song_entry(self, title, artist):
        cur = self.cnx.cursor()
        cur.execute('SELECT title, artist from songs')
        for song in cur.fetchall():  # https://stackoverflow.com/questions/12142133/how-to-get-first-element-in-a-list-of-tuples
            if not self.is_same_song():
                return

    def songs_in_helper(self, *chart_name):
        """
        Returns a table that contains song entries that are in all of the given charts.
        :param chart1:
        :return:
        """
        songs_only_found_on_chart1 = """SELECT songs.song_id, songs.title, songs.artist, chartentries.chart_name
        FROM chartentries JOIN songs ON chartentries.song_id = songs.song_id
        GROUP BY songs.song_id HAVING COUNT(*) = 1 AND chartentries.chart_name = '""" + chart_name[0] + "';"
        chart2_songs_query = """SELECT songs.song_id, songs.title, songs.artist, chartentries.chart_name
        FROM chartentries JOIN songs ON chartentries.song_id = songs.song_id
        WHERE chartentries.chart_name = '""" + chart_name[1] + "';"""
        cur = self.cnx.cursor()
        cur.execute(chart2_songs_query)
        chart2_songs = []
        for row in cur.fetchall():
            chart2_songs.append(row)
        cur.close()

        cur = self.cnx.cursor()
        cur.execute(songs_only_found_on_chart1)
        songs_on_both = []
        for row in cur.fetchall():
            for row_b in chart2_songs:
                if self.is_same_song(row[1], row[2], row_b[1], row_b[2]):
                    entry = (row[1], row[2])
                    songs_on_both.append(entry)

        return songs_on_both

    def populate_spotify(self):
        if not self.is_test:
            scrape_spotify.spotify_to_csv()
            cur = self.cnx.cursor()
            with open('music_data/billboard.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line_count = 0
                for row in csv_reader:
                    if line_count == 100:
                        break
                    cur.callproc('create_chart_entries', ('Spotify', row["Chart Week"], row["Position"], row["Title"],
                                                          row["Artist"], row['Streams'], 'null', 'null',
                                                          'null'))  # fix date # testing to see if streams formatting is the problem
                    line_count += 1
            self.cnx.commit()
            cur.close()

    def populate_billboard(self):
        if not self.is_test:
            scrape_billboard.billboard_to_csv()
            cur = self.cnx.cursor()
            with open('music_data/billboard.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        # print(f'Column names are {", ".join(row)}') # TODO: clean, debug line
                        line_count += 1
                    # if line_count == 101:
                    #     break # TODO: FIX THIS
                    cur.callproc('create_chart_entries', ('Billboard', row["Chart Week"], row["Position"], row["Title"],
                                                          row["Artist"], 'NULL', row["Weeks on Chart"],
                                                          row["Peak Position"],
                                                          row["Last Position"]))
                    line_count += 1
            self.cnx.commit()
            cur.close()

    def common_songs_in(self, *charts):
        songs_in_all_charts = []
        chart_number = len(charts)
        query = """SELECT songs.title, songs.artist, songs.song_id
        FROM chartentries JOIN songs ON chartentries.song_id = songs.song_id
        GROUP BY songs.song_id HAVING COUNT(*) = """ + str(chart_number) + ";"""
        cur = self.cnx.cursor()
        cur.execute(query)
        for row in cur.fetchall():
            songs_in_all_charts.append(row)
        songs_in_all_charts.extend(self.songs_in_helper(*charts))
        return songs_in_all_charts

    def table_from_curweek(self):
        cur = self.cnx.cursor()
        cur.execute("""
        SELECT chartentries.chart_name, chartentries.chart_week, songs.title, songs.artist, songs.song_id, 
        chartentries.position, chartentries.streams, chartentries.weeks_on_chart, chartentries.peak_pos, 
        chartentries.last_pos
        FROM chartentries JOIN songs ON chartentries.song_id = songs.song_id
        WHERE chart_week >= DATE(NOW()) - INTERVAL 7 DAY;
        """)
        cur_chart_entries = []
        for row in cur.fetchall():
            cur_chart_entries.append(row)
        cur.close()
        return cur_chart_entries
