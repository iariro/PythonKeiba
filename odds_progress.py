
import datetime
import japanize_matplotlib
import json
import matplotlib.pyplot as plt
import pandas as pd
import sys

day = None
location = None
race_no = None
odds_thresh = 100
for opt in sys.argv:
    if opt.startswith('-day='):
        day = opt.split('=')[1]
    elif opt.startswith('-location='):
        location = opt.split('=')[1]
    elif opt.startswith('-race_no='):
        race_no = opt.split('=')[1]
    elif opt.startswith('-odds_thresh='):
        odds_thresh = int(opt.split('=')[1])

with open('odds.json') as odds_file:
    odds_json = json.load(odds_file)

dts = []
for history in odds_json[day][location][race_no]['history_list']:
    dts.append(datetime.datetime.strptime(history['datetime'], '%Y/%m/%d %H:%M:%S'))

# 補完用に全番号を求める
horse_no_list = set()
for history in odds_json[day][location][race_no]['history_list']:
    for horse in history['list']:
        horse_no_list.add(horse['horse_no'])

y_list = {horse_no: [] for horse_no in sorted(horse_no_list, key=lambda n: int(n))}
for history in odds_json[day][location][race_no]['history_list']:
    for horse_no in horse_no_list:
        for horse in history['list']:
            if horse_no == horse['horse_no']:
                y_list[horse_no].append(horse['odds'])
                break
        else:
            # 補完
            y_list[horse_no].append(None)

# 閾値判定
y_list2 = {horse_no: odds_list for horse_no, odds_list in y_list.items() if all([odds < odds_thresh if odds else True for odds in odds_list])}

race_time = odds_json[day][location][race_no]['race_time']

horse_name = {}
odds_list = odds_json[day][location][race_no]['horse_list']
for horse in odds_list:
    horse_name[horse['horse_no']] = horse['name']

fig, ax = plt.subplots()
ax.set_facecolor('lightgray')
plt.title(f"{day} {location} {race_no}R {race_time}")
for horse_no in y_list2:
    df = pd.DataFrame({'x': dts, 'y': y_list2[horse_no]})
    ax.plot(df['x'], df['y'], marker='.')
plt.legend([f"{horse_no} {horse_name[horse_no]}" for horse_no in y_list2])
plt.show()
