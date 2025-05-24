
import json
import sys

with open('odds.json') as odds_json_file:
    odds_json = json.load(odds_json_file)

    horse_name_list = set()
    for day in odds_json:
        for location in odds_json[day]:
            for race_no in odds_json[day][location]:
                if 'horse_list' in odds_json[day][location][race_no]:
                    horse_list = odds_json[day][location][race_no]['horse_list']
                else:
                    horse_list = odds_json[day][location][race_no]

                for horse in horse_list:
                    horse_name_list.add(horse['name'])

    for horse in horse_name_list:
        if len(horse) == 2:
            print(horse)
