import json
import sys
import keiba_lib

youbi = None
race_filter = None
for arg in sys.argv:
    if arg.startswith('-youbi='):
        youbi = arg[arg.index('=')+1:]
    elif arg.startswith('-race_filter='):
        race_filter = arg[arg.index('=')+1:]

horse_list = {}
jocky_list = {}
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        if youbi is not None and day[11] != youbi:
            continue

        for location in race_json[day]:
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

                for i, (rank, horse_no, horse_name, jocky, ninki) in enumerate(result['rank_list']):
                    if i == 0:
                        if horse_name not in horse_list:
                            horse_list[horse_name] = 0
                        horse_list[horse_name] += 1
                        if jocky not in jocky_list:
                            jocky_list[jocky] = 0
                        jocky_list[jocky] += 1

horse_list = sorted(horse_list.items(), key=lambda horse: horse[1], reverse=True)
jocky_list = sorted(jocky_list.items(), key=lambda jocky: jocky[1], reverse=True)

#print(horse_list)
for jocky, cnt in jocky_list[0:20]:
    print(f'{jocky:{keiba_lib.get_char_count(jocky, 16)}s} {cnt}')
