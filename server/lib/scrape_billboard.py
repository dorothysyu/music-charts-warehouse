# Web scrapes the content of the Spotify's Top 200 songs in the US in the past week.
# Used these sites to help me write this code:
# https://www.freecodecamp.org/news/web-scraping-python-tutorial-how-to-scrape-data-from-a-website/
# https://medium.com/the-innovation/how-to-scrape-the-most-popular-songs-on-spotify-using-python-8a8979fa6b06
import requests
import pandas
from bs4 import BeautifulSoup

# Latest weekly charts URL for Spotify.
# billboard_url = 'https://www.billboard.com/charts/billboard-200'
billboard_url = 'https://www.billboard.com/charts/hot-100'

billboard_page = requests.get(billboard_url)
billboard_soup = BeautifulSoup(billboard_page.content, 'html.parser')

# Gets the contents of the chart.
songs = billboard_soup.find("ol", class_="chart-list__elements")
# Creates an empty list containing all chart entries.
billboard_chart_entries = []


# Scrapes information for each track.
def scrape_song():
    chart_week = billboard_soup.find(
        "button", class_="date-selector__button").text.strip()
    for track in songs.find_all("button", class_="chart-element__wrapper"):
        position = track.find(
            "span", class_="chart-element__rank__number").text
        artist = track.find(
            "span", class_="chart-element__information__artist").text
        title = track.find(
            "span", class_="chart-element__information__song").text
        weeks_on_chart = track.find(
            class_="chart-element__meta text--center color--secondary text--week").text
        peak_pos = track.find(
            class_="chart-element__meta text--center color--secondary text--peak").text
        last_pos = track.find(
            class_="chart-element__meta text--center color--secondary text--last").text
        last_pos = last_pos.replace("-", "NULL").strip()
        billboard_chart_entries.append(
            [chart_week, position, artist, title, weeks_on_chart, peak_pos, last_pos])


def billboard_to_csv():
    scrape_song()
    df = pandas.DataFrame(billboard_chart_entries, columns=["Chart Week", "Position", "Artist", "Title",
                                                            "Weeks on Chart", "Peak Position", "Last Position"])
    df["Chart Week"] = pandas.to_datetime(df["Chart Week"], format='%B %d, %Y')
    df["Chart Week"] = df["Chart Week"].dt.strftime('%Y-%m-%d')
    with open('server/music_data/billboard.csv', 'w') as f:
        df.to_csv(f, header=True, index=False)


if __name__ == "__main__":
    billboard_to_csv()
