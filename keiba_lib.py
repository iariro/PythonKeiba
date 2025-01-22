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
    race_name = None
    race_title = None
    h1 = soup.select('h1 span')
    if len(h1) > 0:
        race_name = h1[0].text

    h2 = soup.select("div[class='race_title'] div div h2")
    if len(h2) > 0:
        race_title = h2[0].text.strip()
    grade = ''
    grade_img = soup.select("div[class='race_title'] div div h2 span span span img")
    if len(grade_img) >= 1:
        grade_img = grade_img[0]['src']
        if grade_img == '/JRADB/img/grade/icon_grade_g1.png':
            grade = 'GI'
        elif grade_img == '/JRADB/img/grade/icon_grade_g2.png':
            grade = 'GII'
        elif grade_img == '/JRADB/img/grade/icon_grade_g3.png':
            grade = 'GIII'
        elif grade_img == '/JRADB/img/grade/icon_grade_listed.png':
            grade = 'L'

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
            age = cell_list[9].text
            jocky = cell_list[13].text
            weight = cell_list[23].text
            ninki = int(cell_list[27].text)

            jocky = jocky.replace('☆', '').replace('▲', '').replace('△', '').replace('◇', '')

            rank_list.append((rank, horse_no, horse_name, age, jocky, weight, ninki))
            ninki_to_horse_no[ninki] = horse_no
        except:
            pass
    win_yen = None
    win_div = soup.select('li[class="win"] dl dd div div')
    if len(win_div):
        win_yen = {win_div[0].text: int(win_div[1].text.replace(',', '').replace('円', ''))}

    place_yen_list = {}
    place_div_list = soup.select("li[class='place'] dl dd div[class='line']")
    for place_div in place_div_list:
        place_yen_list[place_div.contents[1].text] = int(place_div.contents[3].text.replace(',' ,'').replace('円', ''))

    umaren_yen = {}
    umaren_div_list = soup.select('li[class="umaren"] dl dd div[class="line"]')
    for umaren_div in umaren_div_list:
        umaren_yen[umaren_div.contents[1].text] = int(umaren_div.contents[3].text.replace(',' ,'').replace('円', ''))

    umatan_yen = {}
    umatan_div_list = soup.select('li[class="umatan"] dl dd div[class="line"]')
    for umatan_div in umatan_div_list:
        umatan_yen[umatan_div.contents[1].text] = int(umatan_div.contents[3].text.replace(',' ,'').replace('円', ''))

    wide_yen_list = {}
    if True or 1 in ninki_to_horse_no and 2 in ninki_to_horse_no:
        wide_div_list = soup.select('li[class="wide"] dl dd div')
        for wide_div in wide_div_list:
            if len(wide_div.contents) == 7:
                wide_yen_list[wide_div.contents[1].text] = int(wide_div.contents[3].contents[0].replace(',', ''))
    tierce_yen = {}
    tierce_div_list = soup.select('li[class="tierce"] dl dd div')
    for tierce_div in tierce_div_list:
        if len(tierce_div.contents) == 7:
            tierce_yen[tierce_div.contents[1].text] = int(tierce_div.contents[3].text.replace(',' ,'').replace('円' ,''))

    trio_div_list = soup.select('li[class="trio"] dl dd div[class="line"]')
    trio_yen = {}
    for trio_div in trio_div_list:
        trio_div = [c.text for c in trio_div.children]
        trio_yen[trio_div[1]] = int(trio_div[3].replace(',' ,'').replace('円' ,''))

    return race_name, race_title, grade, rank_list, win_yen, place_yen_list, umaren_yen, umatan_yen, wide_yen_list, trio_yen, tierce_yen

def get_rank_record(record):
    if len(record) == 7:
        return record
    elif len(record) == 6:
        (rank, horse_no, horse_name, jocky, weight, ninki) = record
        return (rank, horse_no, horse_name, '-', jocky, weight, ninki)

def get_rank_record2(record_list):
    if len(record_list[0]) == 7:
        return record_list
    else:
        return [(rank, horse_no, horse_name, '-', jocky, weight, ninki) for (rank, horse_no, horse_name, jocky, weight, ninki) in record_list]

def analyze_tierce(all_race_result, thresh_horse_count=None, tansho_target=None, tierce12_nagashi=None):
    tierce_list = []
    for race_result in all_race_result:
        race_name = race_result['race_name']
        rank_list = race_result['rank_list']
        tierce_yen = race_result['tierce_yen']
        tierce_ninki = race_result['tierce_ninki']

        (rank1, horse_no1, horse_name1, jocky1, ninki1) = rank_list[0]
        (rank2, horse_no2, horse_name2, jocky2, ninki2) = rank_list[1]
        (rank3, horse_no3, horse_name3, jocky3, ninki3) = rank_list[2]

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

    h2 = soup.select("div[class='race_title'] div div h2 span span")

    race_title1 = h1[0].text
    race_title2 = ' '.join([span.text for span in h2])
    date = date_line[0].contents[1].contents[3].text.strip()

    race_header_div = soup.select("div[class='race_header'] div[class='left'] div[class='date_line'] div[class='inner'] div[class='cell time']")
    race_time = race_header_div[0].text.strip()[5:]

    rows = soup.find_all('tr')
    horse_list = []
    for i, row in enumerate(rows):
        if i == 0:
            continue
        horse = {}
        for j, column in enumerate(row.children):
            if j == 3:
                t = column.text.split()
                if len(t) > 0:
                    horse['horse_no'] = t[0]
            elif j == 5:
                lines = column.text.split()
                m1 = re.match('([^0-9\.]*)([0-9\.]*)\(([0-9]*)番人気\)', lines[0])
                if m1:
                    horse['name'] = m1.group(1)
                    horse['odds'] = float(m1.group(2))
                    horse['rank'] = int(m1.group(3))
                if len(lines) >= 2:
                    m2 = re.match('([0-9]*kg\([^\)]*\))', lines[1])
                    if m2:
                        horse['weight'] = m2.group(1)
            elif j == 7:
                if len(column.contents) >= 6:
                    horse['age'] = column.contents[1].text
                    horse['jocky'] = column.contents[5].text.strip().replace('☆', '').replace('▲', '').replace('△', '').replace('◇', '').replace('★', '')
        if 'jocky' in horse and 'rank' in horse:
            horse_list.append(horse)

    #horse_list = sorted(horse_list, key=lambda x: x['rank'])
    if False:
        for horse in horse_list:
            name_width = get_char_count(horse['name'], 20)
            jocky_width = get_char_count(horse['jocky'], 15)
            print(f"{horse['horse_no']:>2} {horse['name']:{name_width}s} {horse['jocky']:{jocky_width}s} {horse['odds']:>5} {horse['rank']:>2}")
        print()
    return {'race_title1': race_title1, 'race_title2': race_title2, 'race_time': race_time, 'horse_list': horse_list}

def get_start_end(pattern):
    if '-' in pattern:
        (s, e) = pattern.split('-')
    else:
        s = e = pattern
    return int(s), int(e)

def nagashi_pattern(n, pattern, ninki):
    cnt = 0
    atari_tierce = False
    atari_trio = False
    if pattern[0] != '*':
        s1, e1 = get_start_end(pattern[0])
    if pattern[1] != '*':
        s2, e2 = get_start_end(pattern[1])
    if pattern[2] != '*':
        s3, e3 = get_start_end(pattern[2])
    for i in range(1, n+1):
        if pattern[0] == '*' or s1 <= i <= e1:
            for j in range(1, n+1):
                if i == j:
                    continue
                if pattern[1] == '*' or s2 <= j <= e2:
                    for k in range(1, n+1):
                        if i == k or j == k:
                            continue
                        if pattern[2] == '*' or s3 <= k <= e3:
                            cnt += 1
                            if i == ninki[0] and j == ninki[1] and k == ninki[2]:
                                atari_tierce = True
                            if i in ninki and j in ninki and k in ninki:
                                atari_trio = True
    return cnt, atari_tierce, atari_trio

def extract_race_name(race_name):
    while True:
        extract = False
        m = re.match('第[0-9]*回(.*)', race_name)
        if m:
            race_name = m.group(1).strip()
            extract = True
        m = re.match('JRA(.*)', race_name)
        if m:
            race_name = m.group(1).strip()
            extract = True
        m = re.match('2024(.*)', race_name)
        if m:
            race_name = m.group(1).strip()
            extract = True
        if extract == False:
            return race_name

def make_exp_histo(yen_list, histo_class):
    histo = {hc: 0 for hc in histo_class}
    for yen in yen_list:
        for hc in histo_class:
            if yen < hc:
                break
            hc2 = hc
        histo[hc2] += 1
    return histo

# 12 13 14 15 23 24 25 34 35 45
def make_combination(s, n, d):
    for i in range(s, n+1):
        if d > 1:
            for j in make_combination(i+1, n, d-1):
                yield [i] + j
        else:
            yield [i]

if __name__ == '__main__':
    for i, n in enumerate(make_combination(1, 18, 5)):
        print(i+1, n)
    print(nagashi_pattern(10, ('1','2-3','2-3'), (1,2,3)))
    print(nagashi_pattern(10, ('1','2-3','2-3'), (3,2,1)))
    print(nagashi_pattern(10, ('1','2-3','2-3'), (4,2,1)))
    print(extract_race_name('第69回 第69回 有馬記念'))
