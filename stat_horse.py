#!/opt/anaconda3/bin/python3

import json
import sys
import keiba_lib

youbi = None
race_filter = None
location_filter = None
for arg in sys.argv:
    if arg.startswith('-youbi='):
        youbi = arg[arg.index('=')+1:]
    elif arg.startswith('-race_filter='):
        race_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-location='):
        location_filter = arg[arg.index('=')+1:]

location_list = ('東京', '京都', '福島', '新潟', '中山', '中京')

horse_list = {}
jocky_list = {}
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
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
                    elif race_filter.startswith('horse_cnt_'):
                        if len(result['rank_list']) > int(race_filter[10:]):
                            continue

                for i, (rank, horse_no, horse_name, age, jocky, weight, ninki) in enumerate(keiba_lib.get_rank_record(result['rank_list'])):
                    if i == 0:
                        jocky = jocky.replace('☆', '').replace('▲', '').replace('△', '')
                        if horse_name not in horse_list:
                            horse_list[horse_name] = {loc: 0 for loc in location_list}
                        horse_list[horse_name][location] += 1
                        if jocky not in jocky_list:
                            jocky_list[jocky] = {loc: 0 for loc in location_list}
                        jocky_list[jocky][location] += 1

horse_list = sorted(horse_list.items(), key=lambda horse: sum([cnt for loc, cnt in horse[1].items()]), reverse=True)
jocky_list = sorted(jocky_list.items(), key=lambda jocky: sum([cnt for loc, cnt in jocky[1].items()]), reverse=True)

print(' ' * 15, ' '.join(location_list))
for horse, cnt in horse_list[0:20]:
    print(f"{horse:{keiba_lib.get_char_count(horse, 18)}s} {'   '.join([f'{yen:>2}' for loc, yen in cnt.items()])}")
for jocky, cnt in jocky_list[0:20]:
    print(f"{jocky:{keiba_lib.get_char_count(jocky, 16)}s} {'   '.join([f'{yen:>2}' for loc, yen in cnt.items()])}")
