
import json
import re
import sys
import keiba_lib

def age_sort(age):
    # せん9   牝3   牝4   牝5   牝6   牝7   牝8  牡10
    if age.startswith('せん'):
        return 300 + int(age[2:])
    elif age.startswith('牝'):
        return 200 + int(age[1:])
    elif age.startswith('牡'):
        return 100 + int(age[1:])

day_filter = None
for arg in sys.argv:
    if arg.startswith('-day='):
        day_filter = arg[arg.index('=')+1:]

age_stat = {'2024': {}, '2025': {}}
all_age = set()
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    sum_age = {'牡': 0, '牝': 0, 'せん': 0}
    for day in race_json:
        if day_filter is not None and re.match(day_filter, day) is None:
            continue
        year = day[0:4]

        for location in race_json[day]:
            print(day, location)

            for race_no in race_json[day][location]:
                result = race_json[day][location][race_no]
                for (rank, horse_no, horse_name, age, jocky, weight, ninki) in keiba_lib.get_rank_record2(result['rank_list']):
                    if age == '-':
                        continue
                    if rank not in age_stat[year]:
                        age_stat[year][rank] = {}
                    if age not in age_stat[year][rank]:
                        age_stat[year][rank][age] = 0
                    age_stat[year][rank][age] += 1
                    all_age.add(age)

                    if age.startswith('せん'):
                        sum_age['せん'] += 1
                    elif age.startswith('牝'):
                        sum_age['牝'] += 1
                    elif age.startswith('牡'):
                        sum_age['牡'] += 1

all_age = sorted(all_age, key=age_sort)
print('  ', ' '.join([f"{age:>{keiba_lib.get_char_count(age, 5)}s}" for age in all_age]))
for year in age_stat:
    for rank, cnt in age_stat[year].items():
        print(f"{rank:>2}", ' '.join([f'{cnt[age]:5}' if age in cnt else ' ' * 5 for age in all_age]))
    print()
for s, cnt in sum_age.items():
    print(s, cnt)
