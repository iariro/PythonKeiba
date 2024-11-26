import json
import sys
import keiba_lib

youbi = None
location_filter = None
for arg in sys.argv:
    if arg.startswith('-youbi='):
        youbi = arg[arg.index('=')+1:]
    elif arg.startswith('-location='):
        location_filter = arg[arg.index('=')+1:]

race_digest_list = []
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        if youbi is not None and day[11] != youbi:
            continue

        for location in race_json[day]:
            if location_filter is not None and location != location_filter:
                continue

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
