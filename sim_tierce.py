#!/opt/anaconda3/bin/python3

import json
import sys
import keiba_lib

ninki_pattern = None
day_filter = None
youbi = None
location_filter = None
race_filter = None
box_width = 3
nagashi = None
for arg in sys.argv[1:]:
    if arg.startswith('-ninki='):
        ninki_pattern = [int(n) for n in arg[arg.index('=')+1:].split(',')]
    elif arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-youbi='):
        youbi = arg[arg.index('=')+1:]
    elif arg.startswith('-location='):
        location_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-race_filter='):
        race_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-box_width='):
        box_width = int(arg[arg.index('=')+1:])
    elif arg.startswith('-nagashi='):
        nagashi = arg[arg.index('=')+1:].split(',')
    else:
        print('err', arg)
        sys.exit()

if ninki_pattern is None:
    ninki_pattern = [1, 2, 3]

total_nagashi_bet = []
total_box_bet = 0
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    total_tierce_yen = []
    total_tiercebox_yen = []
    total_nagashi_yen = []
    total_bet = 0
    for day in race_json:
        if day_filter is not None and day.startswith(day_filter) == False:
            continue
        if youbi is not None and day[11] != youbi:
            continue
        for location in race_json[day]:
            if location_filter is not None and location != location_filter:
                continue

            subtotal_tierce_yen = []
            subtotal_tiercebox_yen = []
            subtotal_nagashi_yen = []
            subtotal_bet = 0
            subtotal_box_bet = 0
            subtotal_nagashi_bet = 0
            horse_cnt = []
            for race_no in race_json[day][location]:
                result = race_json[day][location][race_no]

                if race_filter is not None:
                    if race_filter == 'heavy' and len(race_no) < 2:
                        continue
                    elif race_filter == 'light' and len(race_no) >= 2:
                        continue
                    elif race_filter.startswith('horse_cnt_') and len(result['rank_list']) > int(race_filter[10:]):
                        continue
                    elif race_filter.startswith('title:') and race_filter[6:] not in result['race_title']:
                        continue

                (rank1, horse_no1, horse_name1, jocky1, weight1, ninki1) = result['rank_list'][0]
                (rank2, horse_no2, horse_name2, jocky2, weight2, ninki2) = result['rank_list'][1]
                (rank3, horse_no3, horse_name3, jocky3, weight3, ninki3) = result['rank_list'][2]
                tierce_yen = result['tierce_yen'][f'{horse_no1}-{horse_no2}-{horse_no3}']
                if ninki_pattern[0] == ninki1 and ninki_pattern[1] == ninki2 and ninki_pattern[2] == ninki3:
                    total_tierce_yen.append(tierce_yen)
                    subtotal_tierce_yen.append(tierce_yen)
                    #print(day, location, race_no, tierce_yen)
                if nagashi:
                    nagashi_bet, atari_tierce, atari_trio = keiba_lib.nagashi_pattern(len(result['rank_list']), nagashi, (ninki1, ninki2, ninki3))
                    subtotal_nagashi_bet += nagashi_bet * 100
                    if atari_tierce:
                        #print(race_no, nagashi, (ninki1, ninki2, ninki3), result['tierce_yen'])
                        total_nagashi_yen.append(tierce_yen)
                        subtotal_nagashi_yen.append(tierce_yen)
                    total_nagashi_bet.append(nagashi_bet * 100)
                elif all(ninki <= box_width for ninki in (ninki1, ninki2, ninki3)):
                    if nagashi is None or ninki1 == nagashi:
                        total_tiercebox_yen.append(tierce_yen)
                        subtotal_tiercebox_yen.append(tierce_yen)

                subtotal_bet += 100
                total_bet += 100
                if nagashi is not None:
                    subtotal_box_bet += subtotal_bet * (box_width - 1) * (box_width - 2)
                else:
                    horse_cnt.append(len(result['rank_list']))
                    box_width2 = box_width if box_width <= len(result['rank_list']) else len(result['rank_list'])
                    subtotal_box_bet += 100 * box_width2 * (box_width2 - 1) * (box_width2 - 2)
                total_box_bet += subtotal_box_bet
            print(f"{day} {location} {subtotal_bet:,}円→{subtotal_tierce_yen}={sum(subtotal_tierce_yen):,}円 {subtotal_box_bet:,}円→{subtotal_tiercebox_yen}={sum(subtotal_tiercebox_yen):,}円 {subtotal_nagashi_bet:,}円→{subtotal_nagashi_yen}={sum(subtotal_nagashi_yen):,}円")

print()
print(f"1-3番人気三連単    賭け金：{total_bet:,}円 配当金：{sum(total_tierce_yen):,}円")
if nagashi is not None:
    total_box_bet = total_bet * (box_width - 1) * (box_width - 2)
print(f"1-{box_width}番人気三連単box 賭け金：{total_box_bet:,}円 配当金：{sum(total_tiercebox_yen):,}円")
if nagashi:
    print(f"{','.join(nagashi)}番人気三連単流し 賭け金：{sum(total_nagashi_bet):,}円 配当金：{sum(total_nagashi_yen):,}円")
