#!/opt/anaconda3/bin/python3

import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import sys
import keiba_lib

location_filter = None
for arg in sys.argv:
    if arg.startswith('-location='):
        location_filter = arg[arg.index('=')+1:]

weight_list = []
rank_weight = {n: [] for n in range(1, 19)}
rank_weight_diff = {n: [] for n in range(1, 19)}
with open('race_result.json') as race_json_file:
    race_json = json.load(race_json_file)
    for day in race_json:
        for location in race_json[day]:
            if location_filter is not None and location != location_filter:
                continue

            for race_no, result in race_json[day][location].items():
                for (rank, horse_no, horse_name, age, jocky, weight, ninki) in keiba_lib.get_rank_record2(result['rank_list']):
                    m = re.match('([0-9]*)\((.*)\)', weight)
                    rank_weight[rank].append(int(m.group(1)))
                    weight_list.append(int(m.group(1)))
                    if m.group(2) not in ('初出走', '前計不'):
                        rank_weight_diff[rank].append(int(m.group(2)))

s1 = []
s2 = []
for i in range(1, 19):
    s1.append(i)
    s2.append(sum(rank_weight[i]) / len(rank_weight[i]))
    print(f"{i:>2}着 : {sum(rank_weight[i]) / len(rank_weight[i]):.2f}kg")
s1 = pd.Series(s1)
s2 = pd.Series(s2)
print(s1.corr(s2))

points = [rank_weight[i] for i in range(1, 19)]
fig, ax = plt.subplots()
bp = ax.boxplot(points)
ax.set_xticklabels([i for i in range(1, 19)])
#ax.set_facecolor('lightgray')
plt.title('rank-weight')
plt.grid()
plt.show()

fig, ax = plt.subplots(5, sharey=True)
for i in range(0, 5):
    ax[i].hist(rank_weight[i*2+1], range=(400, 550), bins=40)
fig.tight_layout()
plt.show()
