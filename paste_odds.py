
import json
import os
import sys

def input_macos():
    n = 1
    race_list = []
    while True:
        line = input()
        if line == 'end':
            break
        if n >= 2:
            if n % 3 == 1:
                race.append(line)
            if n % 3 == 2:
                race = []
                race_list.append(race)
                race.append(line)
        n += 1

    horse_list = []
    for race in race_list:
        fields1 = race[0].split()
        if fields1[0].startswith('枠'):
            fields1 = fields1[1:]
        fields2 = race[1].split()
        jocky = f"{fields2[3]} {fields2[4]}"
        jocky = jocky.replace('☆', '').replace('▲', '').replace('△', '').replace('◇', '')
        if fields1[2] != '取消':
            horse = {'horse_no': fields1[0], 'name': fields1[1], 'odds': float(fields1[2]), 'jocky': jocky}
        horse_list.append(horse)

    return horse_list

def input_windows():
    n = 0
    horse_list = []
    while True:
        line = input()
        n += 1
        if line == 'end':
            break
        if n == 1:
             continue

        fields1 = line.split()
        if fields1[0].startswith('枠'):
            fields1 = fields1[1:]
        jocky = f"{fields1[7]} {fields1[8]}"
        jocky = jocky.replace('☆', '').replace('▲', '').replace('△', '').replace('◇', '')
        if fields1[2] != '取消':
            horse_list.append({'horse_no': fields1[0], 'name': fields1[1], 'odds': float(fields1[2]), 'jocky': jocky})

    return horse_list

if sys.argv[1] not in ('-macos', '-windows'):
    sys.exit()

day = input('day:')
location = input('location:')
race_no_start = input('race_no_start:')
for race_no in range(int(race_no_start), 13):
    print(f"paste {race_no}R and type 'end'")
    if sys.argv[1] == '-macos':
        horse_list = input_macos()
    elif sys.argv[1] == '-windows':
        horse_list = input_windows()

    horse_list = sorted(horse_list, key=lambda horse: horse['odds'])
    for i, horse in enumerate(horse_list):
        horse['rank'] = i + 1
        print(horse)

    if input('ok? ') == 'ok':
        if os.path.exists('odds.json'):
            with open('odds.json') as odds_file:
                odds_json = json.load(odds_file)
        else:
            odds_json = {}

        if day not in odds_json:
            odds_json[day] = {}
        if location not in odds_json[day]:
            odds_json[day][location] = {}
        odds_json[day][location][race_no] = horse_list

        with open('odds.json', 'w') as odds_file:
            json.dump(odds_json, odds_file)
