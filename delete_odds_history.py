
import datetime
import japanize_matplotlib
import json
import matplotlib.pyplot as plt
import pandas as pd
import sys

day = None
location = None
race_no = None
for opt in sys.argv:
    if opt.startswith('-day='):
        day = opt.split('=')[1]
    elif opt.startswith('-location='):
        location = opt.split('=')[1]

with open('odds.json') as odds_file:
    odds_json = json.load(odds_file)

for race_no in odds_json[day][location]:
    print(f"del {day} {location} {race_no} {odds_json[day][location][race_no]['history_list'][0]['datetime']}")
    del odds_json[day][location][race_no]['history_list'][0]

with open('odds.json', 'w') as odds_file:
    json.dump(odds_json, odds_file)
