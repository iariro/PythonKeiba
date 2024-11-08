import sys
import keiba_lib

date = sys.argv[1][-11:-3]
url = sys.argv[1]
race_code = url[-2:]

filepath = f'{date}/{race_code}.html'
html = keiba_lib.get_html_web(url)

all_race_result = []
race_list = keiba_lib.get_race_list(html)
for race_url in race_list:
    html = keiba_lib.get_html_web(race_url, part=True)
    (race_name, rank_list, win_yen, wide_yen) = keiba_lib.get_rank_list(html)
    all_race_result.append((race_name, rank_list, win_yen, wide_yen))
    print(race_name)

keiba_lib.analyze(all_race_result)
