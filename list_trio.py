
import json
import re
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

trio_list = []
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        if day_filter is not None and re.match(day_filter, day) is None:
            continue

        for location in race_json[day]:
            if location_filter is not None and location_filter != location:
                continue

            for race_no in race_json[day][location]:
                result = race_json[day][location][race_no]

                (rank1, horse_no1, horse_name1, age1, jocky1, wight1, ninki1) = keiba_lib.get_rank_record(result['rank_list'][0])
                (rank2, horse_no2, horse_name2, age2, jocky2, wight2, ninki2) = keiba_lib.get_rank_record(result['rank_list'][1])
                (rank3, horse_no3, horse_name3, age3, jocky3, wight3, ninki3) = keiba_lib.get_rank_record(result['rank_list'][2])

                ninki_list = (ninki1, ninki2, ninki3)
                if ninki_pattern is None or (ninki_pattern[0] in ninki_list and ninki_pattern[1] in ninki_list and ninki_pattern[2] in ninki_list):
                    trio_list.append({'day': day,
                                        'location': location,
                                        'race_no': race_no,
                                        'race_title': result['race_title'],
                                        'grade': result['grade'],
                                        'horse_cnt': len(result['rank_list']),
                                        'ninki': (ninki1, ninki2, ninki3),
                                        'horse_no': (horse_no1, horse_no2, horse_no3),
                                        'trio_yen': result['trio_yen']})

if sort:
    trio_list = sorted(trio_list, key=lambda race: max([yen for horse_no, yen in race['trio_yen'].items()]))

for race in trio_list:
    print(f"{race['day']} {race['location']} {race['race_no']:>2}R {race['horse_cnt']:>2}頭 {','.join([str(n) for n in race['ninki']])+'番人気':8} {'-'.join([str(n) for n in race['horse_no']])+'番':8} {' '.join([f'{yen:,}円' for hn, yen in race['trio_yen'].items()]):>10} {race['race_title']} {race['grade']}")
