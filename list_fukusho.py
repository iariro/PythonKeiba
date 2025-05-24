
import json
import sys
import keiba_lib

sort = False
day_filter = None
location_filter = None
for arg in sys.argv[1:]:
    if arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-location='):
        location_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-sort'):
        sort = True

win_list = []
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        if day_filter is not None and day.startswith(day_filter) == False:
            continue

        for location in race_json[day]:
            if location_filter is not None and location_filter != location:
                continue

            for race_no in race_json[day][location]:
                result = race_json[day][location][race_no]

                horse_ninki_dict = {}
                for rank_list in result['rank_list']:
                    (rank1, horse_no1, horse_name1, age1, jocky1, wight1, ninki1) = keiba_lib.get_rank_record(rank_list)
                    horse_ninki_dict[horse_no1] = ninki1

                place_ninki_yen = sorted([(horse_ninki_dict[int(horse_no)], yen) for horse_no, yen in result['place_yen'].items()])
                win_list.append({'day': day,
                                 'location': location,
                                 'race_no': race_no,
                                 'race_title': result['race_title'],
                                 'grade': result['grade'],
                                 'horse_cnt': len(result['rank_list']),
                                 'ninki': place_ninki_yen[-1][0],
                                 'place_yen': place_ninki_yen[-1][1]})

if sort:
    win_list = sorted(win_list, key=lambda race: race['place_yen'])

for race in win_list:
    print(f"{race['day']} {race['location']} {race['race_no']:>2}R {race['horse_cnt']:>2}頭 {race['ninki']:2}番人気 {race['place_yen']:,}円 {race['race_title']} {race['grade']}")
