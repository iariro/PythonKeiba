#!/opt/anaconda3/bin/python3

import json
import re
import sys
import keiba_lib

race_title_list = {}
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        for location in race_json[day]:
            variance_list = []
            for race_no in race_json[day][location]:
                result = race_json[day][location][race_no]
                ninki_to_horse_no = {ninki: horse_no for (rank, horse_no, horse_name, jocky, ninki) in result['rank_list']}
                for i in range(1, len(result['rank_list']) + 1):
                    if i in ninki_to_horse_no:
                        variance_list.append((i - ninki_to_horse_no[i]) ** 2)

                race_title = race_json[day][location][race_no]['race_title']
                race_title = re.sub('第[0-9]*回', '第xx回', race_title)
                race_title = re.sub('メイクデビュー.*', 'メイクデビュー', race_title)
                grade = race_json[day][location][race_no]['grade']
                if grade:
                    race_title = grade
                if race_title not in race_title_list:
                    race_title_list[race_title] = []
                race_title_list[race_title].append(sum(variance_list))

for race_title, variance in sorted(race_title_list.items(), key=lambda title: sum(title[1]) / len(title[1])):
    if len(variance) > 1:
        title_width = keiba_lib.get_char_count(race_title, 50)
        print(f"{race_title:{title_width}s} {len(variance):>3}回 {sum(variance) / len(variance):>7.2f}")
