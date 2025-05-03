
import datetime
import json
import re
import sys
import keiba_lib

race_filter = None
for arg in sys.argv[1:]:
    if arg.startswith('-race_filter='):
        race_filter = arg[arg.index('=')+1:]
    else:
        print('err', arg)
        sys.exit()

all_list = []
with open('odds.json') as odds_json_file:
    odds_json = json.load(odds_json_file)

    day_location_race = []
    for day in odds_json:
        for location in odds_json[day]:
            for race_no in odds_json[day][location]:
                if race_filter is not None:
                    if race_filter.startswith('race_no:') and race_no != race_filter[8:]:
                        continue

                race_title = odds_json[day][location][race_no]['race_title'] if 'race_title' in odds_json[day][location][race_no] else '-'
                print(f"{day} {location} {race_no}R {race_title}")

