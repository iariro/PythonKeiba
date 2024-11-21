import json
import sys
import keiba_lib

thresh_horse_count = None
tansho_target = None
tierce12_nagashi = None
for arg in sys.argv:
    if arg.startswith('-thresh_horse_count='):
        thresh_horse_count = int(arg.split('=')[1])
    elif arg.startswith('-tansho_target='):
        tansho_target = [int(n) for n in arg.split('=')[1].split(',')]
    elif arg.startswith('-tierce12_nagashi='):
        tierce12_nagashi = [int(n) for n in arg.split('=')[1].split(',')]

if thresh_horse_count is None:
    thresh_horse_count = int(input('thresh_horse_count='))
if tansho_target is None:
    tansho_target = [int(n) for n in input('tansho_target=').split(',')]

with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        for location in race_json[day]:
            all_race_result = []
            for race_no in race_json[day][location]:
                result = race_json[day][location][race_no]
                all_race_result.append(result)

            keiba_lib.analyze_tierce(all_race_result,
                thresh_horse_count=thresh_horse_count,
                tansho_target=tansho_target,
                tierce12_nagashi=tierce12_nagashi)
