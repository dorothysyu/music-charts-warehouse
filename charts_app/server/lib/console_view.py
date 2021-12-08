from charts_app.server.lib.chart_connection import ChartsConnection

if __name__ == "__main__":
    charts = ChartsConnection()
    menu = {'0': 'View all charts.',
            '1': "Search for songs by title.",
            '2': "Search for songs by artist.",
            '3': "View Spotify charts.",
            '4': "View Billboard charts."}
    '''
    menu['3'] = "Populate Spotify chart."
    menu['4'] = "Populate Billboard chart."
    '''
    menu['5'] = "Exit"

    while True:
        options = menu.keys()
        for entry in options:
            print(entry + ": " + menu[entry])

        selection = input("Please select an action:")
        if selection == '0':
            charts.view_all_chart_entries()
        elif selection == '1':
            charts.search_by_song()
        elif selection == '2':
            charts.search_by_artist()
        elif selection == '3':
            charts.view_spotify()
        elif selection == '4':
            charts.view_billboard()

        elif selection == '5':
            charts.populate_spotify()
        elif selection == '6':
            charts.populate_billboard()
        elif selection == '7':
            print(*charts.common_songs_in('Billboard', 'Spotify'), sep='\n')

        else:
            print("Unknown Option Selected! Please enter a valid command\n")
