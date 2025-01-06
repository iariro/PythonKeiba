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
width = 4
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
    elif arg.startswith('-width='):
        width = int(arg[arg.index('=')+1:])
    else:
        print('err', arg)
        sys.exit()

jun_stat = {}
for n in keiba_lib.make_combination(1, 18, width):
    jun_stat[tuple(n)] = {'umaren_yen': [], 'umatan_yen': [], 'wide_yen': []}
cnt = 0
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

                (rank1, horse_no1, horse_name1, jocky1, weight1, ninki1) = result['rank_list'][0]
                (rank2, horse_no2, horse_name2, jocky2, weight2, ninki2) = result['rank_list'][1]

                cnt += 1
                for k, v in jun_stat.items():
                    if ninki1 in k and ninki2 in k:
                        v['umaren_yen'].append(sum([yen for horse_no, yen in result['umaren_yen'].items()]))
                        v['umatan_yen'].append(sum([yen for horse_no, yen in result['umatan_yen'].items()]))
                        v['wide_yen'].append(sum([yen for horse_no, yen in result['wide_yen_list'].items()]))

for jun, yen in sorted(jun_stat.items(), key=lambda yen: sum(yen[1]['umaren_yen'])):
    umaren_yen = yen['umaren_yen']
    umatan_yen = yen['umatan_yen']
    wide_yen = yen['wide_yen']
    print(f"{'-'.join([f'{j:>2}' for j in jun])} {sum(umaren_yen):>7,}円 {sum(umatan_yen):>7,}円 {sum(wide_yen):>7,}円")
print(cnt)
