import json
import keiba_lib

with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        for location in race_json[day]:
            for race_no in race_json[day][location]:
                result = race_json[day][location][race_no]
                print(result)
                break
                for rank_list in result['rank_list']:
                    (rank1, horse_no1, horse_name1, age1, jocky1, weight1, ninki1) = keiba_lib.get_rank_record(rank_list)
                    print(day, location, race_no, rank1, horse_no1, horse_name1)
