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

    h2 = soup.select("div[class='race_title'] div div h2")
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
            jocky = cell_list[13].text
            ninki = int(cell_list[27].text)
            rank_list.append((rank, horse_no, horse_name, jocky, ninki))
            ninki_to_horse_no[ninki] = horse_no
        except:
            pass
    win_yen = soup.select('li[class="win"] dl dd div div[class="yen"]')
    win_yen = int(win_yen[0].contents[0].replace(',', ''))

    place_yen_list = {}
    place_div_list = soup.select("li[class='place'] dl dd div[class='line']")
    for place_div in place_div_list:
        place_yen_list[place_div.contents[1].text] = int(place_div.contents[3].text.replace(',' ,'').replace('円', ''))

    umaren_yen = soup.select('li[class="umaren"] dl dd div div[class="yen"]')
    umaren_yen = int(umaren_yen[0].contents[0].replace(',', ''))

    umatan_yen = soup.select('li[class="umatan"] dl dd div div[class="yen"]')
    umatan_yen = int(umatan_yen[0].contents[0].replace(',', ''))

    wide_yen_list = {}
    if 1 in ninki_to_horse_no and 2 in ninki_to_horse_no:
        wide_horse_no_list = sorted((ninki_to_horse_no[1], ninki_to_horse_no[2]))
        wide_div_list = soup.select('li[class="wide"] dl dd div')
        for wide_div in wide_div_list:
            if len(wide_div.contents) == 7:
                wide_yen_list[wide_div.contents[1].text] = int(wide_div.contents[3].contents[0].replace(',', ''))
    tierce_div_list = soup.select('li[class="tierce"] dl dd div')
    tierce_yen = int(tierce_div_list[0].contents[3].text.replace(',' ,'').replace('円' ,''))
    tierce_ninki = tierce_div_list[0].contents[5].text

    trio_yen = soup.select('li[class="trio"] dl dd div[class="yen"]')
    trio_yen = int(trio_yen[0].text.replace(',' ,'').replace('円' ,''))

    return race_name, race_title, grade, rank_list, win_yen, place_yen_list, umaren_yen, umatan_yen, wide_yen_list, trio_yen, tierce_yen, tierce_ninki

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

    print(h1[0].text, ' '.join([span.text for span in h2]))
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
