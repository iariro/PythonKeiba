import json
import sys
import keiba_lib

ninki_limit = None
for arg in sys.argv:
    if arg.startswith('-ninki_limit='):
        ninki_limit = int(arg.split('=')[1])

with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    total_bet = 0
    total_total_win_yen_sum = []
    ninki_histo = {i: 0 for i in range(1, 19)}
    for day in race_json:
        for location in race_json[day]:
            top_ninki_list = []
            top_win_yen_sum = []
            total_win_yen_sum = 0
            max_win_yen = 0
            total_horse_cnt = 0
            for race_no in race_json[day][location]:
                result = race_json[day][location][race_no]
                total_horse_cnt += len(result['rank_list'])
                (rank, horse_no, horse_name, jocky, ninki) = result['rank_list'][0]
                if ninki == 1:
                    top_win_yen_sum.append(result['win_yen'])
                total_win_yen_sum += result['win_yen']
                if max_win_yen < result['win_yen']:
                    max_win_yen = result['win_yen']
                top_ninki_list.append(ninki)
                ninki_histo[ninki] += 1

                if race_no in ('10', '11', '12'):
                    total_bet += 100 * ninki_limit
                    if ninki_limit is None or ninki <= ninki_limit:
                        total_total_win_yen_sum.append(result['win_yen'])
            print(f"{day} {location} トップの人気：{' '.join([str(n) for n in top_ninki_list])} トップの配当：{top_win_yen_sum} 最高配当：{max_win_yen} 全掛け金：{100 * total_horse_cnt} 全配当：{total_win_yen_sum}")

print(f'賭け金：{total_bet:,}円 配当：{sum(total_total_win_yen_sum):,}円')

for i, count in ninki_histo.items():
    print(f"{i:2} {'*' * count}")
