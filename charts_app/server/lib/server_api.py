from flask import render_template, Flask
from flask_bootstrap import Bootstrap
from chart_connection import *
import pandas as pd

app = Flask(__name__, template_folder="../static/public")
Bootstrap(app)
charts = ChartsConnection()


@app.route("/")
def index():
    data = charts.return_all_chart_entries()
    # data = charts.table_from_curweek()
    df = pd.DataFrame(data, columns=['Chart Name', 'Chart Week', 'Title', 'Artist', 'Song ID', 'Position', 'Streams',
                                  'Weeks on Chart', 'Peak Position', 'Last Position'])
    df["Chart Week"] = pd.to_datetime(df["Chart Week"], format="%Y/%m/%d")
    df["Chart Week"] = df["Chart Week"].dt.strftime('%Y-%m-%d')
    return df.to_json(orient='records')


@app.route('/tables')
def show_tables():
    data = charts.return_all_chart_entries()
    data = charts.table_from_curweek()
    df = pd.DataFrame(data, columns=['Chart Name', 'Chart Week', 'Title', 'Artist', 'Song ID', 'Position', 'Streams',
                                  'Weeks on Chart', 'Peak Position', 'Last Position'])
    df.set_index('Position', inplace=True)
    spotify = df.loc[df['Chart Name'] == 'Spotify'].sort_index(inplace=False)
    billboard = df.loc[df['Chart Name'] ==
                       'Billboard'].sort_index(inplace=False)
    print(billboard.to_string())
    print(billboard.to_html(classes='billboard'))
    return render_template('view2.html', tables=[spotify.to_html(classes='spotify'),
                                                 billboard.to_html(classes='billboard')],
                           titles=['na', 'Spotify', 'Billboard'])


@app.route('/common')
def show_common_songs():
    data = charts.common_songs_in('Spotify', 'Billboard')
    df = pd.DataFrame(data, columns=['Chart Name', 'Chart Week', 'Title', 'Artist', 'Song ID', 'Position', 'Streams',
                                  'Weeks on Chart', 'Peak Position', 'Last Position'])
    df.set_index('Position', inplace=True)
    return render_template('view2.html', tables=[df.to_html()])


if __name__ == '__main__':
    app.run(debug=True)
