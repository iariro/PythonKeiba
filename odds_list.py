#!/opt/anaconda3/bin/python3

import datetime
import sys
import keiba_lib

url = None
count_display = False
for opt in sys.argv:
    if opt.startswith('-url='):
        url = opt[5:]
    elif opt == '-count_display':
        count_display = True

date = url
race_code = url[-2:]

html = keiba_lib.get_html_web(url)

print(datetime.datetime.now())
print()

filepath = f'{date}/{race_code}.html'
race_list = keiba_lib.get_race_list(html)
top_odds_list = []
count_list = []
horse_count = {}
rider_count = {}
odds_ratio_list = []
for race in race_list:
    html = keiba_lib.get_html_web(race, part=True)

    date = race[-11:-3]
    race_code = race[-2:]

    filepath = f'{date}/{race_code}.html'
    race_name, horse_list = keiba_lib.get_odds_list(html)
    top_odds_list.append({'race_name': race_name, 'horse_list': horse_list[0]})
    count_list.append({'race_name': race_name, 'horse_count': len(horse_list)})
    odds123 = 0
    odds456 = 0
    for i, horse in enumerate(horse_list):
        if horse['name'] not in horse_count:
            horse_count[horse['name']] = 0
        horse_count[horse['name']] += 1
        if horse['rider'] not in rider_count:
            rider_count[horse['rider']] = 0
        rider_count[horse['rider']] += 1
        if i in (0, 1, 2):
            odds123 += float(horse['odds'])
        if i in (3, 4, 5):
            odds456 += float(horse['odds'])
    odds_ratio_list.append((race_name, odds123, odds456))

top_odds_list = sorted(top_odds_list, key=lambda horse: horse['horse_list']['odds'], reverse=True)
count_list = sorted(count_list, key=lambda horse: horse['horse_count'])
odds_ratio_list = sorted(odds_ratio_list, key=lambda race: race[1] / race[2])
print('１番人気のオッズが高いレース')
for i in range(5):
    print(top_odds_list[i]['race_name'], top_odds_list[i]['horse_list']['odds'])
print()
print('頭数の少ないレース')
for i in range(5):
    print(count_list[i]['race_name'], count_list[i]['horse_count'])
print()
print('１−３番人気が際立ったレース')
for i in range(5):
    print(f'{odds_ratio_list[i][0]} {odds_ratio_list[i][1]:.2f} / {odds_ratio_list[i][2]:.2f} = {odds_ratio_list[i][1] / odds_ratio_list[i][2]:.2f}')

if count_display:
    horse_count = sorted(horse_count.items(), key=lambda x:x[1], reverse=True)
    print(horse_count)

    rider_count = sorted(rider_count.items(), key=lambda x:x[1], reverse=True)
    print(rider_count)
