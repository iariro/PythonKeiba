#!/opt/anaconda3/bin/python3

import json
import re
import sys
import keiba_lib

day_filter = None
youbi = None
location_filter = None
for arg in sys.argv[1:]:
    if arg.startswith('-youbi='):
        youbi = arg[arg.index('=')+1:]
    elif arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-location='):
        location_filter = arg[arg.index('=')+1:]
    else:
        print('err', arg)
        sys.exit()

horse_num_stat = {n: {'umaren': [], 'wide': [], 'umatan': []} for n in range(5, 19)}
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

                for horse_no, yen in result['umaren_yen'].items():
                    horse_num_stat[len(result['rank_list'])]['umaren'].append(yen)
                for horse_no, yen in result['umatan_yen'].items():
                    horse_num_stat[len(result['rank_list'])]['umatan'].append(yen)
                for horse_no, wide_yen in result['wide_yen_list'].items():
                    horse_num_stat[len(result['rank_list'])]['wide'].append(wide_yen)

for horse_no, stat in horse_num_stat.items():
    print(f"{horse_no:>2}頭 馬連：{sum(stat['umaren'])//len(stat['umaren']):>5,}円 馬単：{sum(stat['umatan'])//len(stat['umatan']):>6,}円 ワイド：{sum(stat['wide'])//len(stat['wide']):>6,}円")
