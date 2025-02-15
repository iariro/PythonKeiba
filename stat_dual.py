
import json
import re
import sys
import keiba_lib

day_filter = None
youbi = None
sort = 'umaren_yen'
location_filter = None
race_filter = None
width = 4
exclude_big = True
for arg in sys.argv[1:]:
    if arg.startswith('-youbi='):
        youbi = arg[arg.index('=')+1:]
    elif arg.startswith('-sort='):
        sort = arg[arg.index('=')+1:]
    elif arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-location='):
        location_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-race_filter='):
        race_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-width='):
        width = int(arg[arg.index('=')+1:])
    elif arg.startswith('-exclude_big='):
        exclude_big = True if arg[arg.index('=')+1:] == 'True' else False
    else:
        print('err', arg)
        sys.exit()

jun_stat = {}
for n in keiba_lib.make_combination(1, 18, width):
    jun_stat[tuple(n)] = {'umaren_yen': [], 'umaren_cnt': 0, 'umatan_yen': [], 'umatan_cnt': 0, 'wide_yen': [], 'wide_cnt': 0}
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
                    elif race_filter.startswith('horse_cnt:') and len(result['rank_list']) != int(race_filter[10:]):
                        continue

                (rank1, horse_no1, horse_name1, age1, jocky1, weight1, ninki1) = keiba_lib.get_rank_record(result['rank_list'][0])
                (rank2, horse_no2, horse_name2, age2, jocky2, weight2, ninki2) = keiba_lib.get_rank_record(result['rank_list'][1])

                cnt += 1
                for k, v in jun_stat.items():
                    if ninki1 in k and ninki2 in k:
                        v['umaren_yen'].append(sum([yen for horse_no, yen in result['umaren_yen'].items() if exclude_big == False or yen < 50000]))
                        v['umatan_yen'].append(sum([yen for horse_no, yen in result['umatan_yen'].items() if exclude_big == False or yen < 50000]))
                        v['wide_yen'].append(sum([yen for horse_no, yen in result['wide_yen_list'].items() if exclude_big == False or yen < 50000]))
                        v['umaren_cnt'] += 1
                        v['umatan_cnt'] += 1
                        v['wide_cnt'] += 1

for jun, yen in sorted(jun_stat.items(), key=lambda yen: yen[1][sort] if 'cnt' in sort else sum(yen[1][sort])):
    umaren_yen = yen['umaren_yen']
    umatan_yen = yen['umatan_yen']
    wide_yen = yen['wide_yen']
    umaren_cnt = yen['umaren_cnt']
    umatan_cnt = yen['umatan_cnt']
    wide_cnt = yen['wide_cnt']
    print(f"{'-'.join([f'{j:>2}' for j in jun])} {umaren_cnt:>3}:{sum(umaren_yen):>7,}円 {umatan_cnt:>3}:{sum(umatan_yen):>9,}円 {wide_cnt:>3}:{sum(wide_yen):>9,}円")
print(f"{len(jun_stat)}パターン")
print(f"レース数 {cnt}")
