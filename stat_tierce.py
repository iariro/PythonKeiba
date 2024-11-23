import json
import sys
import keiba_lib

tierce_no = None
youbi = None
race_filter = None
for arg in sys.argv[1:]:
    if arg.startswith('-tierce_no='):
        tierce_no = [int(n) for n in arg[arg.index('=')+1:].split(',')]
    elif arg.startswith('-youbi='):
        youbi = arg[arg.index('=')+1:]
    elif arg.startswith('-race_filter='):
        race_filter = arg[arg.index('=')+1:]
    else:
        print('err', arg)
        sys.exit()

if tierce_no is None:
    tierce_no = [1, 2, 3]

with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    total_tierce_yen = []
    total_tiercebox_yen = []
    total_bet = 0
    for day in race_json:
        if youbi is not None and day[11] != youbi:
            continue

        for location in race_json[day]:
            subtotal_tierce_yen = []
            subtotal_tiercebox_yen = []
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
                if tierce_no[0] == ninki1 and tierce_no[1] == ninki2 and tierce_no[2] == ninki3:
                    total_tierce_yen.append(result['tierce_yen'])
                    subtotal_tierce_yen.append(result['tierce_yen'])
                ninki_list = (ninki1, ninki2, ninki3)
                if tierce_no[0] in ninki_list and tierce_no[1] in ninki_list and tierce_no[2] in ninki_list:
                    total_tiercebox_yen.append(result['tierce_yen'])
                    subtotal_tiercebox_yen.append(result['tierce_yen'])
                subtotal_bet += 100
                total_bet += 100
            print(f"{day} {location} {subtotal_bet:,}円 {subtotal_tierce_yen}={sum(subtotal_tierce_yen):,}円 {subtotal_tiercebox_yen}={sum(subtotal_tiercebox_yen):,}円")

print()
print(f"1-3番人気三連単    賭け金：{total_bet:,}円 配当金：{sum(total_tierce_yen):,}円")
print(f"1-3番人気三連単box 賭け金：{total_bet*6:,}円 配当金：{sum(total_tiercebox_yen):,}円")
