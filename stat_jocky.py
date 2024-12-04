#!/opt/anaconda3/bin/python3

import json
import re
import sys
import keiba_lib

jocky_filter = None
for arg in sys.argv:
    if arg.startswith('-jocky='):
        jocky_filter = arg[arg.index('=')+1:]

jocky_list = {}
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        for location in race_json[day]:
            for race_no in race_json[day][location]:
                result = race_json[day][location][race_no]

                for (rank, horse_no, horse_name, jocky, ninki) in result['rank_list']:
                    target = True
                    if jocky_filter is not None:
                        m = re.match(jocky_filter, jocky)
                        if m is None:
                            target = False
                    if target:
                        #print(f"{day} {location} {race_no:>2} {jocky} {rank:>2}着/{len(result['rank_list']):>2}頭 {ninki:>2}番人気 {horse_name}")
                        if jocky not in jocky_list:
                            jocky_list[jocky] = []
                        jocky_list[jocky].append(rank)

jocky_list2 = sorted(jocky_list.items(), key=lambda jocky: sum(jocky[1]) / len(jocky[1]))
for jocky, rank in [(jocky, rank) for jocky, rank in jocky_list2 if len(jocky_list[jocky]) >= 20 or True][0:20]:
    print(f"{jocky:{keiba_lib.get_char_count(jocky, 16)}s} {len(jocky_list[jocky]):>3}回 平均{sum(rank) / len(rank):.2f}着")

if jocky_filter is not None:
    if jocky in jocky_list:
        for i in range(1, 19):
            print(f"{i:>2}着", '*' * len([n for n in jocky_list[jocky] if n == i]) if jocky in jocky_list else '-')
