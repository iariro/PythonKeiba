import json
import sys
import keiba_lib

race_digest_list = []
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        for location in race_json[day]:
            total_variance = 0
            for race_no, result in race_json[day][location].items():
                variance = 0
                for (rank1, horse_no1, horse_name1, jocky1, ninki1) in result['rank_list']:
                    variance += (rank1 - ninki1) ** 2
                    total_variance += (rank1 - ninki1) ** 2
                #print(race_no, result['race_name'], result['grade'] if result['grade'] else '', variance)
            race_digest_list.append({'day': day, 'location': location, 'total_variance': total_variance})

#race_digest_list = sorted(race_digest_list, key=lambda digest: digest['total_variance'])
for digest in race_digest_list:
    print(f"{digest['day']} {digest['location']} {digest['total_variance']:,}", '*' * (digest['total_variance']//100))
