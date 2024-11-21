import json
import sys
import keiba_lib

main_race_list = []
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        for location in race_json[day]:
            result = race_json[day][location]['11']
            main_race_list.append({'race_day': day,
                'race_no': 11,
                'location': location,
                'tierce_yen': result['tierce_yen'],
                'tierce_ninki': result['tierce_ninki']})

main_race_list = sorted(main_race_list, key=lambda race: race['tierce_yen'])
for race in main_race_list:
    print(f"{race['race_day']} {race['location']} {race['race_no']:>2} {race['tierce_yen']:>10,} {race['tierce_ninki']}")
