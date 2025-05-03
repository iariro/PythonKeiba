
import json
import re
import os
import sys
import keiba_lib

day = None
location = None
for arg in sys.argv:
    if arg.startswith('-day='):
        day = arg[arg.index('=')+1:]
    elif arg.startswith('-location='):
        location = arg[arg.index('=')+1:]

with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)

for day2 in race_json:
    print(day2, [location2 for location2 in race_json[day2]])
#del race_json[day][location]

#with open('race_result.json', 'w') as race_json_file:
#    race_json = json.dump(race_json, race_json_file)
