
import datetime
import json
import re
import sys
import keiba_lib

day_filter = None
red_only = False
odds_thresh = 10
ninki_list = [1]
ninki_list2 = [1, 2]
for arg in sys.argv:
    if arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]
        if len(day_filter) == 5:
            day_filter = f'{datetime.datetime.today().year}/{day_filter}'
    elif arg.startswith('-red_only'):
        red_only = True
    elif arg.startswith('-odds_thresh='):
        odds_thresh = float(arg[arg.index('=')+1:])
    elif arg.startswith('-ninki='):
        ninki_list = [int(n) for n in arg[arg.index('=')+1:].split(',')]

with open('odds.json') as odds_json_file:
    odds_json = json.load(odds_json_file)
    for day in odds_json:
        if day_filter is not None and re.match(day_filter, day) is None:
            continue

        result_list = []
        for location in odds_json[day]:

            for race_no in odds_json[day][location]:
                horse_list = []
                race_time = '--時--分'
                if 'race_time' in odds_json[day][location][race_no]:
                    race_time = odds_json[day][location][race_no]['race_time']
                if len(race_time) == 5:
                    race_time = '0' + race_time
                race_title = '-'
                if 'race_title' in odds_json[day][location][race_no]:
                    race_title = odds_json[day][location][race_no]['race_title']
                race_title = keiba_lib.extract_race_name(race_title)
                if 'horse_list' in odds_json[day][location][race_no]:
                    odds_list = sorted(odds_json[day][location][race_no]['horse_list'], key=lambda x: x['odds'])
                else:
                    odds_list = sorted(odds_json[day][location][race_no], key=lambda x: x['odds'])
                result_list.append({'day': day, 'location': location, 'race_no': race_no, 'race_title': race_title, 'race_time': race_time, 'horse_list': horse_list, 'horse_num': len(odds_list)})

                ninki_list2 = []
                for i, horse in enumerate(odds_list):
                    if (i + 1) in ninki_list:
                        ninki_list2.append(horse['rank'])
                for horse in odds_list:
                    if horse['rank'] in ninki_list2:
                        name_width = keiba_lib.get_char_count(horse['name'], 18)
                        jocky_width = keiba_lib.get_char_count(horse['jocky'], 12)
                        horse_list.append(f"{horse['rank']:>2} {horse['horse_no']:>2} {horse['odds']:>5} {horse['name']:{name_width}s} {horse['jocky']:{jocky_width}s} {horse['weight'] if 'weight' in horse else '-'}")

        sep = False
        now = datetime.datetime.now().strftime('%H時%M分')
        print(now)
        for result in sorted(result_list, key=lambda result: result['race_time']):
            if sep == False and result['race_time'] > now:
                print('-' * 60)
                sep = True
            print(f"{result['day']} {result['location']} {result['race_no']}R {result['race_title']} {result['horse_num']}頭 {result['race_time']}")
            for horse in result['horse_list']:
                print(f'    {horse}')
