
import datetime
import json
import re
import sys
import keiba_lib

day_filter = None
for arg in sys.argv:
    if arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]

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
                    odds_list = odds_json[day][location][race_no]['horse_list']
                else:
                    odds_list = odds_json[day][location][race_no]

                print(day, location, race_no, odds_json[day][location][race_no]['race_title'])

                result = None
                if day in race_json:
                    if location in race_json[day]:
                        if race_no in race_json[day][location]:
                            result = race_json[day][location][race_no]

                total_list = []
                for horse in odds_list:
                    if result:
                        for record in result['rank_list']:
                            (rank2, horse_no2, horse_name2, age2, jocky2, weight2, ninki2) = keiba_lib.get_rank_record(record)
                            if horse_no2 == int(horse['horse_no']):
                                rank = rank2
                    past_race = []
                    for i in range(1, 5):
                        if f'past{i}' in horse:
                            if horse[f'past{i}']['rank1'].endswith('着'):
                                past_race.append(int(horse[f'past{i}']['rank1'][0:-1]))
                    total_list.append({'horse_no': horse['horse_no'],
                                       'name': horse['name'], 
                                       'odds': horse['odds'], 
                                       'ninki': horse['rank'], 
                                       'weight': horse['weight'], 
                                       'age': horse['age'], 
                                       'jocky': horse['jocky'], 
                                       'past_race': past_race, 
                                       'rank': rank})
                total_list = sorted(total_list, key=lambda horse: sum(horse['past_race']) / len(horse['past_race']) if len(horse['past_race']) > 0 else 0)
                total_list = sorted(total_list, key=lambda horse: min(horse['past_race']) if len(horse['past_race']) > 0 else 18)
                #total_list = sorted(total_list, key=lambda horse: horse['rank'])
                for horse in total_list:
                    name_width = keiba_lib.get_char_count(horse['name'], 20)
                    weight_width = keiba_lib.get_char_count(horse['weight'], 15)
                    age_width = keiba_lib.get_char_count(horse['age'], 12)
                    jocky_width = keiba_lib.get_char_count(horse['jocky'], 12)
                    if len(horse['past_race']) > 0:
                        past_avg = f"{sum(horse['past_race']) / len(horse['past_race']):.2f}"
                    else:
                        past_avg = '-'
                    if len(horse['past_race']) > 0:
                        past_min = f"{min(horse['past_race'])}"
                    else:
                        past_min = '-'
                    past_race = '/'.join([str(r) for r in horse['past_race']])
                    print(f"{horse['horse_no']:>2} {horse['name']:{name_width}s} {horse['odds']:>5} {horse['ninki']:>2}番人気 {horse['weight']:{weight_width}s} {horse['age']:{age_width}s} {horse['jocky']:{jocky_width}s} {past_race:12} {past_avg:>5} {past_min:>2} {horse['rank']:>2}着")
