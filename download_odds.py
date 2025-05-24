
import datetime
import json
import os
import re
import sys
import keiba_lib

def compare_last_history(history_list, new_history):
    if len(history_list) == 0:
        return False
    eq = True
    for horse1, horse2 in zip(history_list[-1]['list'], new_history):
        if horse1['odds'] != horse2['odds']:
            eq = False
    return eq

url = None
race_no_filter = None
for opt in sys.argv:
    if opt.startswith('-url='):
        url = opt[5:]
    elif opt.startswith('-race_no='):
        race_no_filter = opt[9:]

if os.path.exists('odds.json'):
    with open('odds.json') as odds_file:
        odds_json = json.load(odds_file)
else:
    odds_json = {}

html = keiba_lib.get_html_web(url)

race_list = keiba_lib.get_race_list(html)
for i, race in enumerate(race_list):
    if race_no_filter is not None and i + 1 != int(race_no_filter):
        continue

    html = keiba_lib.get_html_web(race, part=True)

    race_code = race[-2:]

    odds_list = keiba_lib.get_odds_list(html)
    race_title1 = odds_list['race_title1']
    race_title2 = odds_list['race_title2']
    grade = odds_list['grade']
    race_time = odds_list['race_time']
    horse_list = odds_list['horse_list']

    history_up = ''
    history = []
    for horse in horse_list:
        if 'horse_no' in horse and horse['rank'] > 0:
            history.append({'horse_no': horse['horse_no'], 'odds': horse['odds'], 'rank': horse['rank']})
    m = re.match('(.*)年(.*)月(.*)日（(.)曜）.*回(..)[0-9]*日 (.*)レース', race_title1)
    if m:
        date = f'{m.group(1)}/{int(m.group(2)):02}/{int(m.group(3)):02} {m.group(4)}'
        m2 = re.match('(.*)時(.*)分', race_time)
        race_datetime = f'{m.group(1)}/{int(m.group(2)):02}/{int(m.group(3)):02} {int(m2.group(1)):02}:{m2.group(2)}:00'
        location = m.group(5)
        race_no = m.group(6)

        history_list = []
        if date in odds_json and location in odds_json[date] and race_no in odds_json[date][location] and 'history_list' in odds_json[date][location][race_no]:
            history_list = odds_json[date][location][race_no]['history_list']
        now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        history_time = now if race_datetime > now else race_datetime
        if history_time.split()[0] == date.split()[0]:
            if compare_last_history(history_list, history) == False and len(history) > 0:
                history_list.append({'datetime': history_time, 'list': history})
                history_up = '*'
        if date not in odds_json:
            odds_json[date] = {}
        if location not in odds_json[date]:
            odds_json[date][location] = {}
        odds_json[date][location][race_no] = {'race_time': race_time,
                                              'race_title': race_title2,
                                              'grade': grade,
                                              'horse_list': horse_list,
                                              'history_list': history_list}
    print(race_title1, race_time, history_up)

with open('odds.json', 'w') as odds_file:
    json.dump(odds_json, odds_file)
