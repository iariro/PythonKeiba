
import datetime
import json
import re
import sys
import keiba_lib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import japanize_matplotlib

day_filter = None
location_filter = None
for arg in sys.argv:
    if arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]
        if len(day_filter) == 5:
            day_filter = f'{datetime.datetime.today().year}/{day_filter}'
    elif arg.startswith('-location='):
        location_filter = arg[arg.index('=')+1:]

all_odds_list = []
with open('odds.json') as odds_json_file:
    odds_json = json.load(odds_json_file)
    for day in odds_json:
        if day_filter is not None and re.match(day_filter, day) is None:
            continue

        for location in odds_json[day]:
            if location_filter is not None and location != location_filter:
                continue

            for race_no in odds_json[day][location]:
                horse_list = []
                if 'horse_list' in odds_json[day][location][race_no]:
                    odds_list = odds_json[day][location][race_no]['horse_list']
                else:
                    odds_list = odds_json[day][location][race_no]
                odds_list = sorted([odds['odds'] for odds in odds_list])

                if max(odds_list) < 100:
                    continue

                all_odds_list.append({'odds_list': odds_list, 'location': location, 'race_no': race_no})

fig, ax = plt.subplots()
ax.set_facecolor((0.9, 0.9, 0.9, 1))
ax.set_title(f'{day_filter}')
ax.xaxis.set_major_locator(MaxNLocator(integer=True))

for i, odds_list in enumerate(sorted(all_odds_list, key=lambda odds_list: max(odds_list['odds_list']), reverse=True)):
    x_axis = [n for n in range(1, len(odds_list['odds_list'])+1)]
    if i < 10:
        ax.plot(x_axis, odds_list['odds_list'], label=f"{odds_list['location']} {odds_list['race_no']}R")
    else:
        ax.plot(x_axis, odds_list['odds_list'], label=f"{odds_list['location']} {odds_list['race_no']}R", linestyle='--')

ax.legend(loc='upper left')
ax.set_xlabel('人気順')
ax.set_ylabel('オッズ')
ax.grid(True, alpha=0.5)
plt.show()
