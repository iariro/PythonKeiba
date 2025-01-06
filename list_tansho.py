#!/opt/anaconda3/bin/python3

import json
import sys
import keiba_lib

sort = False
day_filter = None
ninki_pattern = None
location_filter = None
for arg in sys.argv[1:]:
    if arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-ninki='):
        ninki_pattern = [int(n) for n in arg[arg.index('=')+1:].split(',')]
    elif arg.startswith('-location='):
        location_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-sort'):
        sort = True

win_list = []
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        if day_filter is not None and day.startswith(day_filter) == False:
            continue

        for location in race_json[day]:
            if location_filter is not None and location_filter != location:
                continue

            for race_no in race_json[day][location]:
                result = race_json[day][location][race_no]

                (rank1, horse_no1, horse_name1, jocky1, wight1, ninki1) = result['rank_list'][0]

                if ninki_pattern is None or (ninki_pattern[0] == ninki1):
                    win_list.append({'day': day,
                                        'location': location,
                                        'race_no': race_no,
                                        'race_title': result['race_title'],
                                        'grade': result['grade'],
                                        'horse_cnt': len(result['rank_list']),
                                        'ninki': ninki1,
                                        'win_yen': result['win_yen']})

if sort:
    win_list = sorted(win_list, key=lambda race: max([yen for horse_no, yen in race['win_yen'].items()]))

for race in win_list:
    print(f"{race['day']} {race['location']} {race['race_no']:>2}R {race['horse_cnt']:>2}頭 {race['ninki']:2}番人気 {' '.join([f'{yen:,}円' for hn, yen in race['win_yen'].items()]):>8} {race['race_title']} {race['grade']}")
