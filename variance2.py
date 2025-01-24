
import datetime
import json
import re
import sys
import keiba_lib

location_filter = None
day_filter = None
for arg in sys.argv:
    if arg.startswith('-location='):
        location_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]
        if len(day_filter) == 5:
            day_filter = f'{datetime.datetime.today().year}/{day_filter}'

title_list = {}
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        if day[11] == '月':
            continue
        if day_filter is not None and re.match(day_filter, day) is None:
            continue

        for location in race_json[day]:
            if location_filter is not None and location != location_filter:
                continue

            for race_no, result in race_json[day][location].items():
                title = result['race_title']
                if int(race_no) >= 8:
                    title = race_no + 'R'
                if 'メイクデビュー' in title:
                    title = 'メイクデビュー'

                title = day[11] + ':' + title
                if title not in title_list:
                    title_list[title] = []
                variance = 0
                for (rank1, horse_no1, horse_name1, age1, jocky1, weight1, ninki1) in keiba_lib.get_rank_record2(result['rank_list']):
                    if rank1 > 6:
                        continue
                    variance += (rank1 - ninki1) ** 2 / len(result['rank_list'])
                title_list[title].append(variance)

for title, variance_list in sorted(title_list.items(), key=lambda title: sum(title[1]) / len(title[1]), reverse=True):
    if len(variance_list) < 10:
        pass#continue
    print(f"{title:{keiba_lib.get_char_count(title, 25)}s} {sum(variance_list) / len(variance_list):6.2f} {len(variance_list)}")
