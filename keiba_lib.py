import re
import unicodedata
import urllib.request
from bs4 import BeautifulSoup

def get_html_web(url, part=False):
    if part:
        url = 'https://www.jra.go.jp/' + url
    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
    headers = {"User-Agent": user_agent}
    request = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(request)
    return html.read()

def get_html_file(filepath):
    with open(filepath, encoding='cp932') as file:
        return '\n'.join([line for line in file])

def get_race_list(html):
    soup = BeautifulSoup(html, "html.parser")
    div_list = soup.select("li a")
    race_list = []
    for link in div_list:
        img = [c for c in link.children][0]
        if img.name == 'img' and img['src'].startswith('/JRADB/img/race_number/race_num_'):
            if link['href'] not in race_list:
                race_list.append(link['href'])
    return race_list

def get_rank_list(html):
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.select('h1 span')
    race_name = h1[0].text
    row_list = soup.select('table[class="basic narrow-xy striped"] tr')
    rank_list = []
    ninki_to_horse_no = {}
    for i, row in enumerate(row_list):
        if i == 0:
            continue
        cell_list = [cell for cell in row.children]
        try:
            rank = int(cell_list[1].text)
            horse_no = int(cell_list[5].text)
            horse_name = ''.join(cell_list[7].text.split())
            jocky = cell_list[13].text
            ninki = int(cell_list[27].text)
            rank_list.append((rank, horse_no, horse_name, jocky, ninki))
            ninki_to_horse_no[ninki] = horse_no
        except:
            pass
    win_yen = soup.select('li[class="win"] dl dd div div[class="yen"]')
    win_yen = int(win_yen[0].contents[0].replace(',', ''))

    umaren_yen = soup.select('li[class="umaren"] dl dd div div[class="yen"]')
    umaren_yen = int(umaren_yen[0].contents[0].replace(',', ''))

    wide_yen = 0
    wide_horse_no_list = sorted((ninki_to_horse_no[1], ninki_to_horse_no[2]))
    wide_div_list = soup.select('li[class="wide"] dl dd div')
    for wide_div in wide_div_list:
        if len(wide_div.contents) == 7:
            if wide_div.contents[1].text == f"{wide_horse_no_list[0]}-{wide_horse_no_list[1]}":
                wide_yen = int(wide_div.contents[3].contents[0].replace(',', ''))
    tierce_div_list = soup.select('li[class="tierce"] dl dd div')
    tierce_yen = int(tierce_div_list[0].contents[3].text.replace(',' ,'').replace('円' ,''))
    tierce_ninki = tierce_div_list[0].contents[5].text

    trio_yen = soup.select('li[class="trio"] dl dd div[class="yen"]')
    trio_yen = int(trio_yen[0].text.replace(',' ,'').replace('円' ,''))

    return race_name, rank_list, win_yen, umaren_yen, wide_yen, trio_yen, tierce_yen, tierce_ninki

def analyze_tierce(all_race_result, thresh_horse_count=None, tansho_target=None, tierce12_nagashi=None):
    tierce_list = []
    for race_result in all_race_result:
        race_name = race_result['race_name']
        rank_list = race_result['rank_list']
        tierce_yen = race_result['tierce_yen']
        tierce_ninki = race_result['tierce_ninki']

        (rank1, horse_no1, horse_name1, ninki1) = rank_list[0]
        (rank2, horse_no2, horse_name2, ninki2) = rank_list[1]
        (rank3, horse_no3, horse_name3, ninki3) = rank_list[2]

        tierce_list.append((race_name, len(rank_list), tierce_yen, tierce_ninki, (ninki1, ninki2, ninki3)))

    tierce_list = sorted(tierce_list, key=lambda race: race[2])
    print('|レース|頭数|配当金|人気|着順|馬券代|回収|')
    print('|-|-|-|-|-|-|-|')
    for race in tierce_list:
        m = re.match('レース結果....年(.*月.*日)（(..)）.*回(..).日 (.*)レース', race[0])
        race_name = ' '.join((m.group(i) for i in (1, 2, 3, 4))) + 'R'
        race_no = m.group(4)
        max_ninki = max(race[4])
        box_cost = max_ninki * (max_ninki - 1) * (max_ninki - 2) * 100
        box_pay = '○' if box_cost < race[2] else '×'
        chakujun = ','.join((str(n) for n in race[4]))
        print(f"|{race_name:20}|{race[1]:>4}頭|{race[2]:10,}円|{race[3].replace('人気',''):>8} | {chakujun:8}|{box_cost:10,}円|{box_pay}|")

def analyze(all_race_result, thresh_horse_count=None, tansho_target=None, tierce12_nagashi=None):
    tansho_list = []
    niren_list = []
    sanren_list = []
    tierce_list = []
    win_yen_sum = 0
    win_yen_sum345 = 0
    umaren_yen_sum = 0
    tierce12_yen_list = []
    tierce12_kake_sum = 0
    trio12_345_yen_list = []
    tierce12_345_yen_list = []
    tierce12_345_kake_sum = 0
    if tansho_target is None:
        tansho_target = (3, 4, 5)
    if tierce12_nagashi is None:
        tierce12_nagashi = (3, 4, 5)
    wide_yen_sum = 0
    for race_result in all_race_result:
        race_name = race_result['race_name']
        rank_list = race_result['rank_list']
        win_yen = race_result['win_yen']
        umaren_yen = race_result['umaren_yen']
        wide_yen = race_result['wide_yen']
        trio_yen = race_result['trio_yen']
        tierce_yen = race_result['tierce_yen']
        tierce_ninki = race_result['tierce_ninki']

        (rank1, horse_no1, horse_name1, ninki1) = rank_list[0]
        (rank2, horse_no2, horse_name2, ninki2) = rank_list[1]
        (rank3, horse_no3, horse_name3, ninki3) = rank_list[2]
        if thresh_horse_count is None or len(rank_list) <= thresh_horse_count:
            tansho_list.append(ninki1)
            niren_list.append((ninki1, ninki2))
            sanren_list.append((ninki1, ninki2, ninki3))

            if ninki1 == 1:
                win_yen_sum += win_yen
            if ninki1 in tansho_target:
                win_yen_sum345 += win_yen

            if (ninki1 + ninki2) in (3, 4):
                umaren_yen_sum += umaren_yen

            if ninki1 == 1 and ninki2 == 2:
                wide_yen_sum += wide_yen
                tierce12_yen_list.append(tierce_yen)
            tierce12_kake_sum += len(rank_list) - 2

            if (ninki1 + ninki2 == 3 and ninki3 in tierce12_nagashi) or \
               (ninki1 + ninki3 == 3 and ninki2 in tierce12_nagashi) or \
               (ninki2 + ninki3 == 3 and ninki1 in tierce12_nagashi):
                trio12_345_yen_list.append(trio_yen)
                tierce12_345_yen_list.append(tierce_yen)

        tierce_list.append((race_name, len(rank_list), tierce_yen, tierce_ninki, (ninki1, ninki2, ninki3)))

    print(f'単勝を賭け続けて当たる額={win_yen_sum}円 {tansho_target}番人気={win_yen_sum345}円')

    print(tansho_list)
    total = len(tansho_list)
    atari = len([n for n in tansho_list if n == 1])
    print(f'１番人気が単勝で勝つ確率={atari * 100 / total if total > 0 else 0:.2f}%')

    print()

    print(f'馬連を賭け続けて当たる額={umaren_yen_sum}円')
    print(niren_list)
    atari = len([(n1, n2) for n1, n2 in niren_list if n1 + n2 == 1+2])
    atari13 = len([(n1, n2) for n1, n2 in niren_list if n1 + n2 == 1+3])
    print(f'１番人気・２番人気が馬連で勝つ確率={atari * 100 / total if total > 0 else 0:.2f}% + {atari13 * 100 / total if total > 0 else 0:.2f}%')
    print()
    atari = len([(n1, n2) for n1, n2 in niren_list if n1 == 1 and n2 == 2])
    print(f'１番人気・２番人気が馬単で勝つ確率={atari * 100 / total if total > 0 else 0:.2f}%')
    print()

    print(f'ワイドを賭け続けて当たる額={wide_yen_sum}円')

    print(sanren_list)
    atari = len([(n1, n2, n3) for n1, n2, n3 in sanren_list if 1 in (n1, n2, n3) and 2 in (n1, n2, n3)])
    print(f'１番人気・２番人気がワイドで勝つ確率={atari * 100 / total if total > 0 else 0:.2f}%')
    print()
    atari = len([(n1, n2, n3) for n1, n2, n3 in sanren_list if n1 + n2 + n3 == 1+2+3])
    print(f'１番人気・２番人気・３番人気が３連複で勝つ確率={atari * 100 / total if total > 0 else 0:.2f}%')
    print()
    atari = len([(n1, n2, n3) for n1, n2, n3 in sanren_list if n1 == 1 and n2 == 2 and n3 == 3])
    print(f'１番人気・２番人気・３番人気が３連単で勝つ確率={atari * 100 / total if total > 0 else 0:.2f}%')

    tierce_list = sorted(tierce_list, key=lambda race: race[2])
    box600_win = []
    box2400_win = []
    box6000_win = []
    min_race_cnt = 0
    print('三連単の配当金')
    print('|レース|頭数|配当金|人気|着順|馬券代|回収|')
    print('|-|-|-|-|-|-|-|')
    for race in tierce_list:
        m = re.match('レース結果....年(.*月.*日)（(..)）.*回(..).日 (.*)レース', race[0])
        race_name = ' '.join((m.group(i) for i in (1, 2, 3, 4))) + 'R'
        race_no = m.group(4)
        max_ninki = max(race[4])
        box_cost = max_ninki * (max_ninki - 1) * (max_ninki - 2) * 100
        box_pay = '○' if box_cost < race[2] else '×'
        chakujun = ','.join((str(n) for n in race[4]))
        if thresh_horse_count is None or race[1] <= thresh_horse_count:
            min_race_cnt += 1
            if max_ninki <= 3:
                box600_win.append(race[2])
            if max_ninki <= 4:
                box2400_win.append(race[2])
            if max_ninki <= 5:
                box6000_win.append(race[2])
        print(f"|{race_name:20}|{race[1]:>4}頭|{race[2]:10,}円|{race[3].replace('人気',''):>8} | {chakujun:8}|{box_cost:10,}円|{box_pay}|")

    print()
    box600_win_join = '+'.join((str(n) for n in box600_win))
    print(f"1-3番人気をボックス買いして得られる額：{box600_win_join}={sum(box600_win):,}円 馬券代：{600*min_race_cnt:,}円")
    box2400_win_join = '+'.join((str(n) for n in box2400_win))
    print(f"1-4番人気をボックス買いして得られる額：{box2400_win_join}={sum(box2400_win):,}円 馬券代：{2400*min_race_cnt:,}円")
    box6000_win_join = '+'.join((str(n) for n in box6000_win))
    print(f"1-5番人気をボックス買いして得られる額：{box6000_win_join}={sum(box6000_win):,}円 馬券代：{6000*min_race_cnt:,}円")
    print(f"1-2番人気流しで得られる額：{tierce12_yen_list}={sum(tierce12_yen_list):,}円 馬券代：{tierce12_kake_sum*600:,}円")
    tierce12_345_bakendai = 100 * len(tierce12_nagashi) * 3 * len(all_race_result)
    print(f"1-2番人気+3-5番人気で得られる額：{tierce12_345_yen_list}={sum(tierce12_345_yen_list):,}円 馬券代：{tierce12_345_bakendai:,}円")
    trio12_345_bakendai = 100 * len(tierce12_nagashi) * len(all_race_result)
    print(f"1-2番人気+3-5番人気の三連複で得られる額：{trio12_345_yen_list}={sum(trio12_345_yen_list):,}円 馬券代：{trio12_345_bakendai:,}円")

    return tansho_list, niren_list, sanren_list

def get_char_count(value, width):
    count = 0
    for c in value:
        if unicodedata.east_asian_width(c) in "FWA":
            count += 1
    return width-count

def get_odds_list(html):
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.select("h1 span span[class='txt'] span[class='opt']")
    date_line = soup.select("div[class='date_line']")
    print(h1[0].text)
    print(date_line[0].contents[1].contents[3].text.strip())
    rows = soup.find_all('tr')
    horse_list = []
    for i, row in enumerate(rows):
        if i == 0:
            continue
        horse = {}
        for j, column in enumerate(row.children):
            if j == 3:
                horse['horse_no'] = column.text.split()[0]
            elif j == 5:
                lines = column.text.split()
                m = re.match('([^0-9\.]*)([0-9\.]*)\(([0-9]*)番人気\)', lines[0])
                if m:
                    horse['name'] = m.group(1)
                    horse['odds'] = m.group(2)
                    horse['rank'] = int(m.group(3))
            elif j == 7:
                if len(column.contents) >= 6:
                    horse['rider'] = column.contents[5].text.strip().replace('☆', '').replace('▲', '')
        if 'rider' in horse and 'rank'in horse:
            horse_list.append(horse)

    horse_list = sorted(horse_list, key=lambda x: x['rank'])
    for horse in horse_list:
        name_width = get_char_count(horse['name'], 20)
        rider_width = get_char_count(horse['rider'], 15)
        print(f"{horse['horse_no']:>2} {horse['name']:{name_width}s} {horse['rider']:{rider_width}s} {horse['odds']:>5} {horse['rank']:>2}")
    print()
    return h1[0].text, horse_list
