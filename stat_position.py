#!/opt/anaconda3/bin/python3

import json
import sys
import keiba_lib

top_horse_no = {}
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        for location in race_json[day]:
            for race_no, result in race_json[day][location].items():
                (rank1, horse_no1, horse_name1, age1, jocky1, weight1, ninki1) = keiba_lib.get_rank_record(result['rank_list'][0])
                (rank2, horse_no2, horse_name2, age2, jocky2, weight2, ninki2) = keiba_lib.get_rank_record(result['rank_list'][1])
                horse_cnt = max(rank[1] for rank in result['rank_list'])
                if horse_cnt not in top_horse_no:
                    top_horse_no[horse_cnt] = {n: 0 for n in range(1, horse_cnt+1)}
                top_horse_no[horse_cnt][horse_no1] += 1
                top_horse_no[horse_cnt][horse_no2] += 1

for horse_cnt in sorted(top_horse_no):
    print(horse_cnt)
    for no, cnt in top_horse_no[horse_cnt].items():
        print(f"\t {no:>2} {cnt:>2}", '*' * cnt)
