import sys
import keiba_lib

thresh_horse_count = None
for arg in sys.argv:
    if arg.startswith('-url='):
        url = sys.argv[1][5:]
        date = url[-11:-3]
        race_code = url[-2:]
    elif arg.startswith('-thresh_horse_count='):
        thresh_horse_count = int(arg.split('=')[1])

filepath = f'{date}/{race_code}.html'
html = keiba_lib.get_html_web(url)

all_race_result = []
race_list = keiba_lib.get_race_list(html)
for race_url in race_list:
    html = keiba_lib.get_html_web(race_url, part=True)
    (race_name, rank_list, win_yen, wide_yen, tierce_yen, tierce_ninki) = keiba_lib.get_rank_list(html)
    all_race_result.append((race_name, rank_list, win_yen, wide_yen, tierce_yen, tierce_ninki))
    print(race_name)

keiba_lib.analyze(all_race_result, thresh_horse_count=thresh_horse_count)
