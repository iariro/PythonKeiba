
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
    elif arg.startswith('-red_only'):
        red_only = True
    elif arg.startswith('-odds_thresh='):
        odds_thresh = float(arg[arg.index('=')+1:])
    elif arg.startswith('-ninki='):
        ninki_list = [int(n) for n in arg[arg.index('=')+1:].split(',')]

odds_and_rank = {odds: [] for odds in range(10, 60)}
with open('odds.json') as odds_json_file, open('race_result.json') as race_json_file:
    odds_json = json.load(odds_json_file)
    race_json = json.load(race_json_file)
    for day in odds_json:
        if day_filter is not None and re.match(day_filter, day) is None:
            continue

        for location in odds_json[day]:
            print(day, location)

            for race_no in odds_json[day][location]:
                if 'horse_list' in odds_json[day][location][race_no]:
                    odds_list = sorted(odds_json[day][location][race_no]['horse_list'], key=lambda x: x['odds'])
                else:
                    odds_list = sorted(odds_json[day][location][race_no], key=lambda x: x['odds'])

                if day in race_json:
                    for rank, horse_no, name, jocky, wegit, ninki in race_json[day][location][race_no]['rank_list']:
                        if horse_no == int(odds_list[0]['horse_no']):
                            odds_and_rank[odds_list[0]['odds']*10].append(rank)

for odds, rank in odds_and_rank.items():
    print(f"オッズ{odds/10}", ' '.join([f"{len([r for r in rank if r == i])*100/len(rank):6.2f}" if len([r for r in rank if r == i])>0 else '      ' for i in range(1, 19)]))
