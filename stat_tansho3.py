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

cnt = 0
win_yen_list = {i: [] for i in range(1, 18+1)}
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

                for (rank, horse_no, name, age, jocky, weight, ninki) in keiba_lib.get_rank_record(result['rank_list']):
                    if str(horse_no) in result['win_yen']:
                        win_yen_list[ninki].append(result['win_yen'][str(horse_no)])
                cnt += 1

for ninki, win_yen in win_yen_list.items():
    print(f"{ninki:>2}番人気 {len(win_yen):>3}回 {sum(win_yen):>7,}円", '*' * (sum(win_yen) // 1000))
print()
for ninki, win_yen in win_yen_list.items():
    print(f"{ninki:>2}番人気 {len(win_yen):>3}回 {sum(win_yen):>7,}円", '*' * (len(win_yen) // 5))
print(cnt)
