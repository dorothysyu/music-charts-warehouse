# Web scrapes the content of the Spotify's Top 200 songs in the US in the past week.
# TODO: Probably need to use Selenium or an additional framework in order to scrape fully loaded page
# Used these sites to help me write this code:
# https://www.freecodecamp.org/news/web-scraping-python-tutorial-how-to-scrape-data-from-a-website/
# https://medium.com/the-innovation/how-to-scrape-the-most-popular-songs-on-spotify-using-python-8a8979fa6b06
import requests
import pandas
from bs4 import BeautifulSoup

# Latest weekly charts URL for Spotify.
rollingstones_url = 'https://www.rollingstone.com/charts/songs/'
rollingstones_page = requests.get(rollingstones_url)
rollingstones_soup = BeautifulSoup(rollingstones_page.content, 'html.parser')

songs = rollingstones_soup.find("div", class_="c-content")  # Gets the contents of the chart.
rollingstones_chart_entries = []                                      # Creates an empty list containing all chart entries.


# Scrapes information for each track.
def scrape_song():
    # date = billboard_soup.find("div", {"data-type": "date"}).find("div", class_="responsive-select-value").text
    for track in songs.find_all("div", class_="c-chart__table--top"):
        position = track.find("div", class_="c-chart__table--rank").text
        artist = track.find("div", class_="c-chart__table--caption").text
        title = track.find("div", class_="c-chart__table--title").text
        # streams = track.find("span", class_="chart-element__information").find("span", class_="chart-element__metas").find("span", class_="chart_element__meta")
        # last_week
        # peak_pos
        rollingstones_chart_entries.append([position, title, artist])


def rollingstones_to_csv():
    scrape_song()
    final_df = pandas.DataFrame(rollingstones_chart_entries, columns=["Position", "Title", "Artist"])
    with open('rollingstones.csv', 'w') as f:
        final_df.to_csv(f, header=True, index=False)


rollingstones_to_csv()
