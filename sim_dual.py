#!/opt/anaconda3/bin/python3

import json
import sys
import keiba_lib

youbi = None
race_filter = None
ninki_pattern = None
location_filter = None
for arg in sys.argv:
    if arg.startswith('-youbi='):
        youbi = arg[arg.index('=')+1:]
    elif arg.startswith('-race_filter='):
        race_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-ninki='):
        ninki_pattern = [int(n) for n in arg[arg.index('=')+1:].split(',')]
    elif arg.startswith('-location='):
        location_filter = arg[arg.index('=')+1:]

if ninki_pattern is None:
    ninki_pattern = [1, 2]

bet_yen = 0
total_umaren = 0
total_umatan = 0
total_wide = 0
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        if youbi is not None and day[11] != youbi:
            continue

        for location in race_json[day]:
            if location_filter is not None and location != location_filter:
                continue

            subtotal_umaren = []
            subtotal_umatan = []
            subtotal_wide = []
            race_cnt = 0

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

                (rank1, horse_no1, horse_name1, jocky1, ninki1) = result['rank_list'][0]
                (rank2, horse_no2, horse_name2, jocky2, ninki2) = result['rank_list'][1]
                (rank3, horse_no3, horse_name3, jocky3, ninki3) = result['rank_list'][2]

                race_cnt += 1
                bet_yen += 100
                if ninki_pattern[0] in (ninki1, ninki2) and ninki_pattern[1] in (ninki1, ninki2):
                    subtotal_umaren.append(result['umaren_yen'])
                    total_umaren += result['umaren_yen']
                if ninki1 == ninki_pattern[0] and ninki2 == ninki_pattern[1]:
                    subtotal_umatan.append(result['umatan_yen'])
                    total_umatan += result['umatan_yen']
                ninki_to_horseno = {ninki1: horse_no1, ninki2: horse_no2, ninki3: horse_no3}
                if ninki_pattern[0] in ninki_to_horseno and ninki_pattern[1] in ninki_to_horseno:
                    horse_no12 = '-'.join([str(n) for n in sorted((ninki_to_horseno[ninki_pattern[0]], ninki_to_horseno[ninki_pattern[1]]))])
                    subtotal_wide.append(result['wide_yen_list'][horse_no12])
                    total_wide += result['wide_yen_list'][horse_no12]

            print(f"{day} {location} {race_cnt*100:>6,}円 馬連：{subtotal_umaren}={sum(subtotal_umaren):,}円 馬単：{subtotal_umatan}={sum(subtotal_umatan):,}円 ワイド：{subtotal_wide}={sum(subtotal_wide):,}円")

print()
print(f'賭け金={bet_yen:,}円 馬連={total_umaren:,}円 馬単={total_umatan:,}円 ワイド={total_wide:,}円')
