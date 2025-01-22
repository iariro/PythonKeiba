#!/opt/anaconda3/bin/python3

import json
import re
import sys
import keiba_lib

day_filter = None
youbi = None
sort = False
location_filter = None
race_filter = None
for arg in sys.argv[1:]:
    if arg.startswith('-youbi='):
        youbi = arg[arg.index('=')+1:]
    elif arg.startswith('-sort'):
        sort = True
    elif arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-location='):
        location_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-race_filter='):
        race_filter = arg[arg.index('=')+1:]
    else:
        print('err', arg)
        sys.exit()

ninki_and_yen = []
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        if day_filter is not None:
            m = re.match(day_filter, day)
            if m is None:
                continue
        if youbi is not None and day[11] != youbi:
            continue

        for location in race_json[day]:
            if location_filter is not None and location != location_filter:
                continue

            for race_no in race_json[day][location]:
                result = race_json[day][location][race_no]

                if race_filter is not None:
                    if race_filter == 'heavy' and len(race_no) < 2:
                        continue
                    elif race_filter == 'light' and len(race_no) >= 2:
                        continue
                    elif race_filter.startswith('horse_cnt_') and len(result['rank_list']) > int(race_filter[10:]):
                        continue

                (rank1, horse_no1, horse_name1, age1, jocky1, weight1, ninki1) = keiba_lib.get_rank_record(result['rank_list'][0])
                (rank2, horse_no2, horse_name2, age2, jocky2, weight2, ninki2) = keiba_lib.get_rank_record(result['rank_list'][1])
                (rank3, horse_no3, horse_name3, age3, jocky3, weight3, ninki3) = keiba_lib.get_rank_record(result['rank_list'][2])

                
                for horse_no, yen in result['tierce_yen'].items():
                    ninki_and_yen.append((max(ninki1, ninki2, ninki3), yen))

histo = {n: {'cnt': 0, 'yen': []} for n in range(1, 19)}
for ninki, yen in ninki_and_yen:
    histo[ninki]['cnt'] += 1
    histo[ninki]['yen'].append(yen)
total = 0
for ninki, cnt in histo.items():
    if len(cnt['yen']) > 0:
        total += cnt['cnt']
        print(f"{ninki:>2} : {total*100/len(ninki_and_yen):>5.1f}% {min(cnt['yen']):>9,}-{max(cnt['yen']):>9,} ", '*' * cnt['cnt'])
