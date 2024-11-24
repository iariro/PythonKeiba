import json
import sys
import keiba_lib

ninki_pattern = None
youbi = None
race_filter = None
for arg in sys.argv:
    if arg.startswith('-ninki='):
        ninki_pattern = [int(n) for n in arg[arg.index('=')+1:].split(',')]
    elif arg.startswith('-youbi='):
        youbi = arg[arg.index('=')+1:]
    elif arg.startswith('-race_filter='):
        race_filter = arg[arg.index('=')+1:]

if ninki_pattern is None:
    ninki_pattern = [1, 2, 3]

with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    trio_yen_sum = []
    total_bet = 0
    for day in race_json:
        if youbi is not None and day[11] != youbi:
            continue

        for location in race_json[day]:
            subtrio_yen_sum = []
            subtotal_bet = 0
            for race_no in race_json[day][location]:
                result = race_json[day][location][race_no]

                if race_filter is not None:
                    if race_filter == 'heavy' and len(race_no) < 2:
                        continue
                    elif race_filter == 'light' and len(race_no) >= 2:
                        continue
                    elif race_filter.startswith('horse_cnt_') and len(result['rank_list']) > int(race_filter[10:]):
                        continue

                (rank1, horse_no1, horse_name1, jocky1, ninki1) = result['rank_list'][0]
                (rank2, horse_no2, horse_name2, jocky2, ninki2) = result['rank_list'][1]
                (rank3, horse_no3, horse_name3, jocky3, ninki3) = result['rank_list'][2]
                ninki_list = (ninki1, ninki2, ninki3)
                if ninki_pattern[0] in ninki_list and ninki_pattern[1] in ninki_list and ninki_pattern[2] in ninki_list:
                    trio_yen_sum.append(result['trio_yen'])
                    subtrio_yen_sum.append(result['trio_yen'])
                subtotal_bet += 100
                total_bet += 100
            print(f"{day} {location} {subtotal_bet} {subtrio_yen_sum}={sum(subtrio_yen_sum):,}")

print()
print(f"賭け金：{total_bet:,}円 配当金：{sum(trio_yen_sum):,}円")
