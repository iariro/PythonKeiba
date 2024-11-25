import json
import sys
import keiba_lib

display_place_rank = False
ninki_pattern = [1]
youbi = None
race_filter = None
for arg in sys.argv:
    if arg.startswith('-ninki='):
        ninki_pattern = [int(n) for n in arg[arg.index('=')+1:].split(',')]
    elif arg.startswith('-youbi='):
        youbi = arg[arg.index('=')+1:]
    elif arg.startswith('-race_filter='):
        race_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-place_rank'):
        display_place_rank = True

total_bet = 0
total_place_yen = 0
place_rank = []
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        if youbi is not None and day[11] != youbi:
            continue

        for location in race_json[day]:
            subtotal_place_yen = []
            for race_no in race_json[day][location]:
                result = race_json[day][location][race_no]

                if race_filter is not None:
                    if race_filter == 'heavy' and len(race_no) < 2:
                        continue
                    elif race_filter == 'light' and len(race_no) >= 2:
                        continue
                    elif race_filter.startswith('horse_cnt_'):
                        if len(result['rank_list']) not in [int(n) for n in race_filter[10:].split(',')]:
                            continue

                (rank1, horse_no1, horse_name1, jocky1, ninki1) = result['rank_list'][0]
                (rank2, horse_no2, horse_name2, jocky2, ninki2) = result['rank_list'][1]
                (rank3, horse_no3, horse_name3, jocky3, ninki3) = result['rank_list'][2]

                ninki_to_horseno = {ninki1: horse_no1, ninki2: horse_no2, ninki3: horse_no3}
                horseno_to_ninki = {str(r[1]): r[4] for r in result['rank_list']}
                place_yen2 = 0
                for horse_no, place_yen in result['place_yen'].items():
                    for ninki in ninki_pattern:
                        if ninki in ninki_to_horseno:
                            if str(ninki_to_horseno[ninki]) == horse_no:
                                place_yen2 = place_yen
                    place_rank.append({'day': day, 'location': location, 'race_no': race_no, 'ninki': horseno_to_ninki[horse_no] if horse_no in horseno_to_ninki else '', 'place_yen': place_yen})
                subtotal_place_yen.append(place_yen2)
                total_bet += 100 * len(ninki_pattern)

            yen_list = ','.join([f'{yen}' for yen in subtotal_place_yen])
            print(f'{day} {location} {yen_list}={sum(subtotal_place_yen):,}円')
            total_place_yen += sum(subtotal_place_yen)

print()
print(f'賭け金：{total_bet:,}円 配当：{total_place_yen:,}円')

if display_place_rank:
    place_rank = sorted(place_rank, key=lambda place: place['place_yen'])
    for place in place_rank:
        print(f"{place['day']} {place['location']} {place['race_no']:>2}R {place['ninki']:>2}番人気 {place['place_yen']:>5,}円")
