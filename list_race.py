
import datetime
import json
import re
import sys
import keiba_lib

day_filter = None
filter_jocky = None
sort_order = 'avg_past'
for arg in sys.argv:
    if arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]
    elif arg.startswith('-sort='):
        sort_order = arg[arg.index('=')+1:]
    elif arg.startswith('-jocky='):
        filter_jocky = arg[arg.index('=')+1:]

all_list = []
with open('odds.json') as odds_json_file, open('race_result.json') as race_json_file:
    odds_json = json.load(odds_json_file)
    race_json = json.load(race_json_file)

    day_location_race = []
    for day in odds_json:
        if day_filter is not None and re.match(day_filter, day) is None:
            continue
        for location in odds_json[day]:
            for race_no in odds_json[day][location]:
                time = '--:--'
                if 'race_time' in odds_json[day][location][race_no]:
                    time = odds_json[day][location][race_no]['race_time']
                if len(time) == 5:
                    time = '0' + time
                day_location_race.append({'day': day, 'location': location, 'race_no': race_no, 'time': time})
    day_location_race = sorted(day_location_race, key=lambda race: (race['day'], race['time']))

    for race in day_location_race:
        day = race['day']
        location = race['location']
        race_no = race['race_no']

        horse_list = []
        if 'horse_list' in odds_json[day][location][race_no]:
            odds_list = odds_json[day][location][race_no]['horse_list']
        else:
            odds_list = odds_json[day][location][race_no]

        # 騎手がいるか
        if filter_jocky is not None and all([filter_jocky not in horse['jocky'] for horse in odds_list]):
            continue

        time = '--:--'
        if 'race_time' in odds_json[day][location][race_no]:
            time = odds_json[day][location][race_no]['race_time']

        race_title = '-'
        if 'race_title' in odds_json[day][location][race_no]:
            race_title = odds_json[day][location][race_no]['race_title']

        grade = ''
        if 'grade' in odds_json[day][location][race_no]:
            grade = odds_json[day][location][race_no]['grade']

        race_header = f"{day} {location} {race_no}R {time} {race_title}"
        if grade:
            race_header += ' ' + grade
        print(race_header)

        result = None
        if day in race_json:
            if location in race_json[day]:
                if race_no in race_json[day][location]:
                    result = race_json[day][location][race_no]

        total_list = []
        rank = 0
        for j, horse in enumerate(odds_list):
            if result:
                for record in result['rank_list']:
                    (rank2, horse_no2, horse_name2, age2, jocky2, weight2, ninki2) = keiba_lib.get_rank_record(record)
                    if horse['horse_no'] not in ('除外', '取消') and horse_no2 == int(horse['horse_no']):
                        rank = rank2
            past_race = []
            past_time = []
            for i in range(1, 5):
                if f'past{i}' in horse:
                    if horse[f'past{i}']['rank1'].endswith('着'):
                        past_race.append(int(horse[f'past{i}']['rank1'][0:-1]))
                        m = re.match('([0-9]*).*', horse[f'past{i}']['course'])
                        if m:
                            meter = int(m.group(1))
                        if len(horse[f'past{i}']['time']) > 1:
                            past_time.append(keiba_lib.time_to_second(horse[f'past{i}']['time']) * 1000 / meter)
            total_list.append({'horse_no': horse['horse_no'] if 'horse_no' in horse else j+1,
                               'icon': horse['icon'] if 'icon' in horse else None,
                               'name': horse['name'],
                               'odds': horse['odds'],
                               'ninki': horse['rank'],
                               'weight': horse['weight'] if 'weight' in horse else '-',
                               'age': horse['age'].replace('\n', '') if 'age' in horse else '-',
                               'jocky': horse['jocky'],
                               'past_race': past_race,
                               'past_time': past_time,
                               'rank': rank})

        past_rank_list = {horse['horse_no']: 18 for horse in total_list}
        for horse in total_list:
            if len(horse['past_race']) > 0:
                past_rank_list[horse['horse_no']] = sum(horse['past_race']) / len(horse['past_race'])
        past_rank_list = {horse_no: (i+1, rank) for i, (horse_no, rank) in enumerate(sorted(past_rank_list.items(), key=lambda horse: horse[1]))}

        if sort_order == 'avg_past':
            total_list = sorted(total_list, key=lambda horse: sum(horse['past_race']) / len(horse['past_race']) if len(horse['past_race']) > 0 else 18)
        elif sort_order == 'min_past':
            total_list = sorted(total_list, key=lambda horse: min(horse['past_race']) if len(horse['past_race']) > 0 else 18)
        elif sort_order == 'rank':
            total_list = sorted(total_list, key=lambda horse: horse['rank'])
        elif sort_order == 'odds':
            total_list = sorted(total_list, key=lambda horse: horse['odds'])

        past_race_cnt = 0
        for horse in total_list:
            if len(horse['past_race']) > 0:
                past_race_cnt += 1

        for horse in total_list:
            name_width = keiba_lib.get_char_count(horse['name'], 20)
            weight_width = keiba_lib.get_char_count(horse['weight'], 15)
            age_width = keiba_lib.get_char_count(horse['age'], 12)
            jocky_width = keiba_lib.get_char_count(horse['jocky'], 12)
            past_rank = past_rank_list[horse['horse_no']]
            if len(horse['past_race']) > 0:
                past_min = f"{min(horse['past_race'])}"
            else:
                past_min = '-'
            past_race = '/'.join([str(r) for r in horse['past_race']])
            past_time = 0
            if len(horse['past_time']) > 0:
                past_time = sum(horse['past_time']) / len(horse['past_time'])
            icon = None
            if horse['icon']:
                icon = {'chi': '地', 'kaku-chi': '角地', 'gai': '外'}[horse['icon']]
            gap = None
            if past_race_cnt > 0:
                if horse['ninki'] - past_rank[0] >= 6:
                    gap = '*'
                elif past_rank[0] - horse['ninki'] >= 6:
                    gap = '-'
            print(f"{horse['horse_no']:>2} {horse['name']:{name_width}s} {horse['odds']:>5} {horse['ninki']:>2}番人気 {horse['weight']:{weight_width}s} {horse['age']:{age_width}s} {horse['jocky']:{jocky_width}s} {past_race:12} {past_rank[1]:>5.2f} {past_rank[0]:>3}位 {past_min:>2} {past_time:5.2f}秒 {horse['rank']:>2}着 {' '.join((t for t in (icon, gap) if t))}")

        yen_line = []
        if result:
            for item, yen in result.items():
                if 'yen' in item:
                    kake_type = None
                    if item == 'win_yen':
                        kake_type = '単勝'
                    elif item == 'place_yen':
                        kake_type = '複勝'
                    elif item == 'wide_yen_list':
                        kake_type = 'ワイド'
                    elif item == 'umaren_yen':
                        kake_type = '馬連'
                    elif item == 'umatan_yen':
                        kake_type = '馬単'
                    elif item == 'trio_yen':
                        kake_type = '三連複'
                    elif item == 'tierce_yen':
                        kake_type = '三連単'
                    yen_line.append(f"{kake_type}:{' '.join([f'{yen:,}円' for horse_no, yen in result[item].items()])}")
            print('／'.join(yen_line))

