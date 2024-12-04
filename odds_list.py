#!/opt/anaconda3/bin/python3

import json
import sys
import keiba_lib

ninki_list = [1]
ninki_list2 = [1, 2]
for arg in sys.argv:
    if arg.startswith('-ninki='):
        ninki_list = [int(n) for n in arg[arg.index('=')+1:].split(',')]

with open('odds.json') as odds_json_file, open('race_result.json') as race_json_file:
    odds_json = json.load(odds_json_file)
    race_json = json.load(race_json_file)
    for day in odds_json:
        for location in odds_json[day]:
            print(day, location)

            win_yen_list = []
            place_yen_list = []
            umaren_yen_list = []
            for race_no in odds_json[day][location]:
                odds_list = sorted(odds_json[day][location][race_no], key=lambda x: x['odds'])
                odds_list = [float(horse['odds']) for horse in odds_list]

                target2 = False
                target34 = False
                high_odds = [odds for odds in odds_list if odds < 10]
                if len(high_odds) <= 2:
                    target2 = True
                elif len(high_odds) <= 3:
                    if min([odds for odds in high_odds]) < 2.5:
                        if high_odds[1] >= 3:
                            target34 = True
                elif len(high_odds) <= 4:
                    if min([odds for odds in high_odds]) < 2:
                        if high_odds[1] >= 3:
                            target34 = True

                horse_list = sorted(odds_json[day][location][race_no], key=lambda horse: horse['rank'])
                if target2 or target34:
                    for ninki in ninki_list:
                        if horse_list[ninki - 1]['horse_no'] in race_json[day][location][race_no]['win_yen']:
                            win_yen_list.append(race_json[day][location][race_no]['win_yen'][horse_list[ninki - 1]['horse_no']])
                        else:
                            win_yen_list.append(None)

                        if horse_list[ninki - 1]['horse_no'] in race_json[day][location][race_no]['place_yen']:
                            place_yen_list.append(race_json[day][location][race_no]['place_yen'][horse_list[ninki - 1]['horse_no']])
                        else:
                            place_yen_list.append(None)

                if target2:
                    (ninki1, ninki2) = ninki_list2
                    horse_nos = sorted((int(n) for n in (horse_list[ninki1 - 1]['horse_no'], horse_list[ninki2 - 1]['horse_no'])))
                    horse_nos = [str(n) for n in horse_nos]
                    if '-'.join(horse_nos) in race_json[day][location][race_no]['umaren_yen']:
                        umaren_yen_list.append(race_json[day][location][race_no]['umaren_yen']['-'.join(horse_nos)])
                    else:
                        umaren_yen_list.append(None)

                print('\t', day, location, race_no, target2, target34, [horse['odds'] for horse in horse_list[0:6]])
                if False:
                    for horse in horse_list:
                        name_width = keiba_lib.get_char_count(horse['name'], 20)
                        jocky_width = keiba_lib.get_char_count(horse['jocky'], 15)
                        print(f"\t{horse['horse_no']:>2} {horse['name']:{name_width}s} {horse['jocky']:{jocky_width}s} {horse['odds']:>5} {horse['rank']:>2}")
            print('\t単勝', win_yen_list)
            print(f"\t複勝 賭け金={100*len(place_yen_list)}円 配当={place_yen_list}={sum(place_yen_list)}円")

            print('\t馬連', umaren_yen_list)
            print()
