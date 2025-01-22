# 配当がどうやって決定されるかを推定

import datetime
import json
import re
import sys
import keiba_lib

day_filter = None
for arg in sys.argv:
    if arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]
        if len(day_filter) == 5:
            day_filter = f'{datetime.datetime.today().year}/{day_filter}'

all_list = []
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

                horse_no_odds = {}
                for horse in odds_list:
                    horse_no_odds[horse['horse_no']] = horse['odds']
                    if result:
                        for record in result['rank_list']:
                            (rank2, horse_no2, horse_name2, age2, jocky2, weight2, ninki2) = keiba_lib.get_rank_record(record)
                            if horse_no2 == int(horse['horse_no']):
                                rank = rank2
                for no, yen in result['umaren_yen'].items():
                    no1, no2 = no.split('-')
                    ratio = yen / (horse_no_odds[no1] * (horse_no_odds[no2]))
                    all_list.append({'day': day,
                                     'location': location,
                                     'race_no': race_no,
                                     'no': no,
                                     'horse_cnt': len(result['rank_list']),
                                     'umaren_yen': yen,
                                     'odds1': horse_no_odds[no1],
                                     'odds2': horse_no_odds[no2]})
for race in sorted(all_list, key=lambda race: race['odds1']):
    if False and race['odds1'] != 12:
        continue
    ratio = race['umaren_yen'] / (race['odds1'] * race['odds2'] * race['horse_cnt'])
    print(f"{race['day']} {race['location']} {race['race_no']:>2}R {race['no']:5} {race['horse_cnt']:>2}頭 {race['umaren_yen']:7,} {race['odds1']:5} {race['odds2']:5} {ratio}")
