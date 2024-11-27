#!/opt/anaconda3/bin/python3

import json
import sys
import keiba_lib

day_filter = None
location_filter = None
for arg in sys.argv[1:]:
    if arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-location='):
        location_filter = arg[arg.index('=')+1:]

tierce_list = []
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

                (rank1, horse_no1, horse_name1, jocky1, ninki1) = result['rank_list'][0]
                (rank2, horse_no2, horse_name2, jocky2, ninki2) = result['rank_list'][1]
                (rank3, horse_no3, horse_name3, jocky3, ninki3) = result['rank_list'][2]
                tierce_list.append({'day': day, 'location': location, 'race_no': race_no, 'race_title': result['race_title'], 'grade': result['grade'], 'horse_cnt': len(result['rank_list']), 'ninki': (ninki1, ninki2, ninki3), 'tierce_yen': result['tierce_yen']})

#tierce_list = sorted(tierce_list, key=lambda race: race['tierce_yen'])
for race in tierce_list:
    print(f"{race['day']} {race['location']} {race['race_no']:>2}R {race['horse_cnt']:>2}頭 {','.join([str(n) for n in race['ninki']]):8} {race['tierce_yen']:>9,}円 {race['race_title']} {race['grade']}")
