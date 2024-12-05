
import json
import re
import os
import sys
import keiba_lib

url = None
for arg in sys.argv:
    if arg.startswith('-url='):
        url = arg[arg.index('=')+1:]

if url is None:
    url = input('url=')

date = url[-11:-3]
race_code = url[-2:]

filepath = f'{date}/{race_code}.html'
html = keiba_lib.get_html_web(url)

if os.path.exists('race_result.json'):
    with open('race_result.json') as race_json_file:
        race_json = json.load(race_json_file)
else:
    race_json = {}

race_list = keiba_lib.get_race_list(html)
for race_url in race_list:
    html = keiba_lib.get_html_web(race_url, part=True)
    (race_name, race_title, grade, rank_list, win_yen, place_yen_list, umaren_yen, umatan_yen, wide_yen_list, trio_yen, tierce_yen) = keiba_lib.get_rank_list(html)
    m = re.match('レース結果(.*)年(.*)月(.*)日（(.)曜）.回(.*)[0-9]日 (.*)レース', race_name)
    if m:
        location = m.group(5)
        if False:
            if m.group(5) == '東京':
                location = 'tokyo'
            elif m.group(5) == '京都':
                location = 'kyoto'
            elif m.group(5) == '中山':
                location = 'nakayama'
        day = f'{int(m.group(1)):04}/{int(m.group(2)):02}/{int(m.group(3)):02} {m.group(4)}'
        if day not in race_json:
            race_json[day] = {}
        if location not in race_json[day]:
            race_json[day][location] = {}
        race_json[day][location][m.group(6)] = {
            'race_name': race_name,
            'race_title': race_title,
            'grade': grade,
            'rank_list': rank_list,
            'win_yen': win_yen,
            'place_yen': place_yen_list,
            'umaren_yen': umaren_yen,
            'umatan_yen': umatan_yen,
            'wide_yen_list': wide_yen_list,
            'trio_yen': trio_yen,
            'tierce_yen': tierce_yen}
        print(race_name, race_title)

with open('race_result.json', 'w') as race_json_file:
    race_json = json.dump(race_json, race_json_file)
