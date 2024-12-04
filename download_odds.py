#!/opt/anaconda3/bin/python3

import json
import os
import re
import sys
import keiba_lib

url = None
for opt in sys.argv:
    if opt.startswith('-url='):
        url = opt[5:]

if os.path.exists('odds.json'):
    with open('odds.json') as odds_file:
        odds_json = json.load(odds_file)
else:
    odds_json = {}

html = keiba_lib.get_html_web(url)

race_list = keiba_lib.get_race_list(html)
for race in race_list:
    html = keiba_lib.get_html_web(race, part=True)

    race_code = race[-2:]

    odds_list = keiba_lib.get_odds_list(html)
    race_title1 = odds_list['race_title1']
    race_title2 = odds_list['race_title2']
    horse_list = odds_list['horse_list']
    print(race_title1)
    m = re.match('(.*)年(.*)月(.*)日（(.)曜）.*回(..)[0-9]日 (.*)レース', race_title1)
    if m:
        date = f'{m.group(1)}/{int(m.group(2)):02}/{int(m.group(3)):02} {m.group(4)}'
        location = m.group(5)
        race_no = m.group(6)

        if date not in odds_json:
            odds_json[date] = {}
        if location not in odds_json[date]:
            odds_json[date][location] = {}
        odds_json[date][location][race_no] = horse_list

with open('odds.json', 'w') as odds_file:
    json.dump(odds_json, odds_file)
