
import json
import re
import sys
import keiba_lib

display_place_rank = False
day_filter = None
ninki_pattern = [1]
youbi = None
location_filter = None
race_filter = None
for arg in sys.argv:
    if arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-ninki='):
        ninki_pattern = [int(n) for n in arg[arg.index('=')+1:].split(',')]
    elif arg.startswith('-youbi='):
        youbi = arg[arg.index('=')+1:]
    elif arg.startswith('-location='):
        location_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-race_filter='):
        race_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-place_rank'):
        display_place_rank = True

total_bet = 0
total_place_yen = 0
place_rank = []
hit_list = []
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
                    elif race_filter.startswith('title:') and len([title for title in race_filter[6:].split(',') if title in result['race_title']]) == 0:
                        continue

                (rank1, horse_no1, horse_name1, age1, jocky1, weight1, ninki1) = keiba_lib.get_rank_record(result['rank_list'][0])
                (rank2, horse_no2, horse_name2, age2, jocky2, weight2, ninki2) = keiba_lib.get_rank_record(result['rank_list'][1])
                (rank3, horse_no3, horse_name3, age3, jocky3, weight3, ninki3) = keiba_lib.get_rank_record(result['rank_list'][2])

                ninki_to_horseno = {ninki1: horse_no1, ninki2: horse_no2, ninki3: horse_no3}
                horseno_to_ninki = {str(r[1]): r[4] for r in result['rank_list']}
                place_yen2 = []
                for horse_no, place_yen in result['place_yen'].items():
                    for ninki in ninki_pattern:
                        if ninki in ninki_to_horseno:
                            if str(ninki_to_horseno[ninki]) == horse_no:
                                place_yen2.append(place_yen)
                    place_rank.append({'day': day,
                                       'location': location,
                                       'race_no': race_no,
                                       'ninki': horseno_to_ninki[horse_no] if horse_no in horseno_to_ninki else '',
                                       'place_yen': place_yen})

                subtotal_place_yen.append(sum(place_yen2))
                total_bet += 100 * len(ninki_pattern)
                hit_list.append(sum(place_yen2) > 0)

            yen_list = ','.join([f'{yen}' for yen in subtotal_place_yen])
            print(f"{day} {location} {' '.join([yen if yen != '0' else '_' for yen in yen_list.split(',')])}={sum(subtotal_place_yen):,}円←{100*len(subtotal_place_yen)*len(ninki_pattern)}円")
            total_place_yen += sum(subtotal_place_yen)

print()
print(f'賭け金：{total_bet:,}円 配当：{total_place_yen:,}円 勝率：{len([hit for hit in hit_list if hit])*100/len(hit_list) if len(hit_list)>1 else 0:.2f}%')

if display_place_rank:
    place_rank = sorted(place_rank, key=lambda place: place['place_yen'])
    for place in place_rank:
        print(f"{place['day']} {place['location']} {place['race_no']:>2}R {place['ninki']:>2}番人気 {place['place_yen']:>5,}円")
