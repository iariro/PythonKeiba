#!/opt/anaconda3/bin/python3

import json
import re
import sys
import keiba_lib

youbi = None
day_filter = None
race_filter = None
ninki_pattern = None
location_filter = None
bet_type = None
for arg in sys.argv:
    if arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-youbi='):
        youbi = arg[arg.index('=')+1:]
    elif arg.startswith('-race_filter='):
        race_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-ninki='):
        ninki_pattern = [int(n) for n in arg[arg.index('=')+1:].split(',')]
    elif arg.startswith('-location='):
        location_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-type='):
        bet_type = arg[arg.index('=')+1:]

if ninki_pattern is None:
    ninki_pattern = [1, 2]

bet_yen = 0
total_umaren = 0
total_umatan = 0
total_wide = 0
total_umaren_bet = 0
total_umatan_bet = 0
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        if day_filter is not None and re.match(day_filter, day) is None:
            continue

        if youbi is not None and day[11] != youbi:
            continue

        for location in race_json[day]:
            if location_filter is not None and location != location_filter:
                continue

            subtotal_umaren = []
            subtotal_umatan = []
            subtotal_wide = []
            race_cnt = 0

            subtotal_umaren_bet = 0
            subtotal_umatan_bet = 0
            for race_no in race_json[day][location]:
                result = race_json[day][location][race_no]

                if race_filter is not None:
                    if race_filter == 'heavy' and len(race_no) < 2:
                        continue
                    elif race_filter == 'light' and len(race_no) >= 2:
                        continue
                    elif race_filter.startswith('horse_cnt_'):
                        if len(result['rank_list']) > int(race_filter[10:]):
                            continue
                    elif race_filter.startswith('title:') and len([title for title in race_filter[6:].split(',') if title in result['race_title']]) == 0:
                        continue

                (rank1, horse_no1, horse_name1, jocky1, ninki1) = result['rank_list'][0]
                (rank2, horse_no2, horse_name2, jocky2, ninki2) = result['rank_list'][1]
                (rank3, horse_no3, horse_name3, jocky3, ninki3) = result['rank_list'][2]

                race_cnt += 1
                bet_yen += 100
                if ninki1 in ninki_pattern and ninki2 in ninki_pattern:
                    for horse_no, yen in result['umaren_yen'].items():
                        subtotal_umaren.append(yen)
                        total_umaren += yen
                    for horse_no, yen in result['umatan_yen'].items():
                        subtotal_umatan.append(yen)
                        total_umatan += yen
                else:
                    subtotal_umaren.append(0)
                    subtotal_umatan.append(0)

                ninki_to_horseno = {ninki1: horse_no1, ninki2: horse_no2, ninki3: horse_no3}
                for n1 in ninki_pattern:
                    for n2 in ninki_pattern:
                        if n1 >= n2:
                            continue
                        if n1 not in ninki_to_horseno or n2 not in ninki_to_horseno:
                            continue
                        horse_no12 = '-'.join([str(ninki_to_horseno[n]) for n in sorted((n1, n2))])
                        if horse_no12 in result['wide_yen_list']:
                            #print(f"{day} {location} {race_no}R {horse_no12} {result['wide_yen_list'][horse_no12]}")
                            subtotal_wide.append(result['wide_yen_list'][horse_no12])
                            total_wide += result['wide_yen_list'][horse_no12]
                        else:
                            pass#print(f"{day} {location} {race_no} {horse_no12} {result['wide_yen_list']}")
                subtotal_umaren_bet += 100 * len(ninki_pattern) * (len(ninki_pattern) - 1) // 2
                subtotal_umatan_bet += 100 * len(ninki_pattern) * (len(ninki_pattern) - 1)
            total_umaren_bet += subtotal_umaren_bet
            total_umatan_bet += subtotal_umatan_bet

            if bet_type is None or bet_type == 'umaren':
                print(f"{day} {location} 馬連：{subtotal_umaren_bet:,}円→{subtotal_umaren}={sum(subtotal_umaren):,}円 ワイド：{subtotal_wide}={sum(subtotal_wide):,}円")
            if bet_type is None or bet_type == 'umatan':
                print(f"{day} {location} 馬単：{subtotal_umatan_bet:,}円→{subtotal_umatan}={sum(subtotal_umatan):,}円")

print()
print(f'馬連={total_umaren_bet:,}円→{total_umaren:,}円 ワイド={total_wide:,}円 馬単={total_umatan_bet:,}→{total_umatan:,}円')
