import sys
import keiba_lib

date = sys.argv[1][-11:-3]
url = sys.argv[1]
race_code = url[-2:]

html = keiba_lib.get_html_web(url)

filepath = f'{date}/{race_code}.html'
race_list = keiba_lib.get_race_list(html)
for race in race_list:
    html = keiba_lib.get_html_web(race, part=True)

    date = race[-11:-3]
    race_code = race[-2:]

    filepath = f'{date}/{race_code}.html'
    keiba_lib.get_odds_list(html)
