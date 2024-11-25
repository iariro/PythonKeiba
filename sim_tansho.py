import json
import sys
import keiba_lib

ninki_pattern = [1]
youbi = None
race_filter = None
histo = False
for arg in sys.argv:
    if arg.startswith('-ninki='):
        ninki_pattern = [int(n) for n in arg[arg.index('=')+1:].split(',')]
    elif arg.startswith('-youbi='):
        youbi = arg[arg.index('=')+1:]
    elif arg.startswith('-race_filter='):
        race_filter = arg[arg.index('=')+1:]

print('１番人気だけ買い続けた場合')

with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    total_bet = 0
    total_total_win_yen_sum = []
    ninki_histo = {i: 0 for i in range(1, 19)}
    for day in race_json:
        if youbi is not None and day[11] != youbi:
            continue

        for location in race_json[day]:
            top_ninki_list = []
            top_win_yen_sum = []
            total_win_yen_sum = 0
            max_win_yen = 0
            subtotal_bet = 0
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

                (rank, horse_no, horse_name, jocky, ninki) = result['rank_list'][0]
                if ninki in ninki_pattern:
                    top_win_yen_sum.append(result['win_yen'])
                    total_win_yen_sum += result['win_yen']
                if max_win_yen < result['win_yen']:
                    max_win_yen = result['win_yen']
                top_ninki_list.append(ninki)
                ninki_histo[ninki] += 1

                subtotal_bet += 100 * len(ninki_pattern)
                total_bet += 100 * len(ninki_pattern)
                if ninki in ninki_pattern:
                    total_total_win_yen_sum.append(result['win_yen'])
            print(f"{day} {location} 掛け金={subtotal_bet:5,}円 配当={total_win_yen_sum:5,}円 トップの人気：{' '.join([str(n) for n in top_ninki_list])}")

print(f'賭け金：{total_bet:,}円 配当：{sum(total_total_win_yen_sum):,}円')

if histo:
    for i, count in ninki_histo.items():
        print(f"{i:2} {'*' * count}")