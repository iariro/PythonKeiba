
import datetime
import json
import re
import sys
import keiba_lib

day_filter = None
jocky = '武 豊'
for arg in sys.argv:
    if arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]
        if len(day_filter) == 5:
            day_filter = f'{datetime.datetime.today().year}/{day_filter}'
    elif arg.startswith('-jocky='):
        jocky = arg[arg.index('=')+1:]

with open('odds.json') as odds_json_file, open('race_result.json') as race_json_file:
    odds_json = json.load(odds_json_file)
    race_json = json.load(race_json_file)
    for day in odds_json:
        if day_filter is not None and re.match(day_filter, day) is None:
            continue

        result_list = []
        for location in odds_json[day]:

            for race_no in odds_json[day][location]:

                horse_list = []
                if 'horse_list' in odds_json[day][location][race_no]:
                    odds_list = sorted(odds_json[day][location][race_no]['horse_list'], key=lambda x: x['odds'])
                else:
                    odds_list = sorted(odds_json[day][location][race_no], key=lambda x: x['odds'])

                result = None
                if day in race_json:
                    if location in race_json[day]:
                        if race_no in race_json[day][location]:
                            result = race_json[day][location][race_no]

                for horse in odds_list:
                    if jocky in horse['jocky']:
                        rank = '-'
                        if result:
                            for record in result['rank_list']:
                                (rank2, horse_no2, horse_name2, age2, jocky2, weight2, ninki2) = keiba_lib.get_rank_record(record)
                                if horse_no2 == int(horse['horse_no']):
                                    rank = rank2
                        name_width = keiba_lib.get_char_count(horse['name'], 18)
                        jocky_width = keiba_lib.get_char_count(horse['jocky'], 12)
                        print(f"{day} {location} {race_no:>2}R {horse['rank']:>2}番人気 {horse['horse_no']:>2} {horse['odds']:>5} {horse['name']:{name_width}s} {horse['jocky']:{jocky_width}s} {rank:>2}着 {horse['weight'] if 'weight' in horse else '-'}")
