import json
import sys
import keiba_lib

jocky_rank = {}

main_race_list = []
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        for location in race_json[day]:
            result = race_json[day][location]['11']

            (rank1, horse_no1, horse_name1, jocky1, ninki1) = result['rank_list'][0]
            (rank2, horse_no2, horse_name2, jocky2, ninki2) = result['rank_list'][1]
            (rank3, horse_no3, horse_name3, jocky3, ninki3) = result['rank_list'][2]

            main_race_list.append({'race_day': day,
                'race_no': 11,
                'location': location,
                'tierce_yen': result['tierce_yen'],
                'tierce_ninki': result['tierce_ninki'],
                'ninki_list': f'{ninki1}-{ninki2}-{ninki3} {jocky1}-{jocky2}-{jocky3}'})
            for jocky in (jocky1, jocky2, jocky3):
                if jocky not in jocky_rank:
                    jocky_rank[jocky] = 0
                jocky_rank[jocky] += 1

main_race_list = sorted(main_race_list, key=lambda race: race['tierce_yen'])
for race in main_race_list:
    print(f"{race['race_day']} {race['location']} {race['race_no']:>2} {race['tierce_yen']:>10,} {race['tierce_ninki']} {race['ninki_list']}")

for jocky in sorted(jocky_rank.items(), key=lambda jocky: jocky[1], reverse=True):
    print(jocky)
