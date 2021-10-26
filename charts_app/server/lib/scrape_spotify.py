# Web scrapes the content of the Spotify's Top 200 songs in the US in the past week.
# Used these sites to help me write this code:
# https://www.freecodecamp.org/news/web-scraping-python-tutorial-how-to-scrape-data-from-a-website/
# https://medium.com/the-innovation/how-to-scrape-the-most-popular-songs-on-spotify-using-python-8a8979fa6b06
import requests
import pandas
from bs4 import BeautifulSoup
import cfscrape

scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance.
# Latest weekly charts URL for Spotify.
spotify_url = 'https://spotifycharts.com/regional/us/weekly/latest'
spotify_page = scraper.get(spotify_url)
spotify_soup = BeautifulSoup(spotify_page.content, 'html.parser')

# Gets the contents of the chart.
songs = spotify_soup.find("table", class_="chart-table")
# Creates an empty list containing all chart entries.
spotify_charts_entries = []


# Scrapes information for each track.
def scrape_song():
    date = spotify_soup.find("div", attrs={
                             "data-type": "date"}).find("div", class_="responsive-select-value").text
    for track in songs.find("tbody").find_all("tr"):
        position = track.find("td", class_="chart-table-position").text
        artist = track.find("td", class_="chart-table-track").find("span").text
        artist = artist.replace("by ", "").strip()
        title = track.find(
            "td", class_="chart-table-track").find("strong").text
        streams = track.find("td", class_="chart-table-streams").text
        streams = streams.replace(',', '')
        spotify_charts_entries.append([date, position, artist, title, streams])


def spotify_to_csv():
    scrape_song()
    df = pandas.DataFrame(spotify_charts_entries, columns=[
                          "Chart Week", "Position", "Artist", "Title", "Streams"])
    df["Chart Week"] = pandas.to_datetime(df["Chart Week"], format="%m/%d/%Y")
    df["Chart Week"] = df["Chart Week"].dt.strftime('%Y-%m-%d')
    with open('charts_app/server/music_data/spotify.csv', 'w') as f:
        df.to_csv(f, header=True, index=False)


if __name__ == "__main__":
    spotify_to_csv()
