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

tierse_yen_list = []
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

                for horse_no, yen in result['tierce_yen'].items():
                    tierse_yen_list.append(yen)

histo_class = [100 * i for i in range(1, 10)]
histo_class += [1000 * i for i in range(1, 10)]
histo_class += [10000 * i for i in range(1, 10)]
histo_class += [100000 * i for i in range(1, 10)]
histo_class += [1000000 * i for i in range(1, 10)]

histo = keiba_lib.make_exp_histo(tierse_yen_list, histo_class)

for hc, cnt in histo.items():
    print(f"{hc:>9,} : {'*' * cnt}")
