import sys
import keiba_lib

url = None
thresh_horse_count = None
tansho_target = None
for arg in sys.argv:
    if arg.startswith('-url='):
        url = arg[5:]
    elif arg.startswith('-thresh_horse_count='):
        thresh_horse_count = int(arg.split('=')[1])
    elif arg.startswith('-tansho_target='):
        tansho_target = [int(n) for n in arg.split('=')[1].split(',')]

if url is None:
    url = input('url=')
if thresh_horse_count is None:
    thresh_horse_count = int(input('thresh_horse_count='))
if tansho_target is None:
    tansho_target = [int(n) for n in input('tansho_target=').split(',')]

date = url[-11:-3]
race_code = url[-2:]

filepath = f'{date}/{race_code}.html'
html = keiba_lib.get_html_web(url)

all_race_result = []
race_list = keiba_lib.get_race_list(html)
for race_url in race_list:
    html = keiba_lib.get_html_web(race_url, part=True)
    result = keiba_lib.get_rank_list(html)
    all_race_result.append(result)
    print(result[0])

keiba_lib.analyze(all_race_result, thresh_horse_count=thresh_horse_count, tansho_target=tansho_target)
