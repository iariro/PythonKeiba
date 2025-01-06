#!/bin/sh

rm race_result.json

START_TIME=$(date)
for url in `cat << EOF
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1006202404080120240928/DF
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1007202403080120240928/F8

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1006202404090120240929/0F
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1007202403090120240929/28

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202404010120241005/4A
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202405010120241005/59
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1004202404010120241005/00
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202404020120241006/7A
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202405020120241006/89
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1004202404020120241006/30

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202405030120241012/62
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1004202404030120241012/09
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202404030120241013/10
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202405040120241013/92
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202404040120241014/40
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1004202404040120241014/F6

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202404050120241019/64
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202405050120241019/73
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1004202404050120241019/1A
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202404060120241020/8C
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202405060120241020/9B
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1004202404060120241020/42

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202404070120241026/6D
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202405070120241026/7C
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1004202404070120241026/23
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202404080120241027/9D
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202405080120241027/AC
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1004202404080120241027/53

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202405010120241102/BF
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202406010120241102/CE
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1003202403010120241102/C9
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202405020120241103/EF
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202406020120241103/FE
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1003202403020120241103/F9

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202405030120241109/D0
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202406030120241109/DF
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1003202403030120241109/DA
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202405040120241110/F8
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202406040120241110/07
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1003202403040120241110/02

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202405050120241116/D9
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202406050120241116/E8
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1003202403050120241116/E3
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202405060120241117/09
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202406060120241117/18
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1003202403060120241117/13

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0105202405070120241123/03
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0108202406070120241123/12
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0105202405080120241124/33
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0108202406080120241124/42

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1006202405010120241130/9D
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202407010120241130/93
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1007202404010120241130/B6
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202405020120241201/5B
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0108202407020120241201/51
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0107202404020120241201/74

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202405030120241207/3C
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0108202407030120241207/32
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0107202404030120241207/55
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1006202405040120241208/4B
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202407040120241208/41
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1007202404040120241208/64

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202405050120241214/45
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0108202407050120241214/3B
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0107202404050120241214/5E
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202405060120241215/75
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0108202407060120241215/6B
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0107202404060120241215/8E
EOF`
do
  python3 download_result.py -url=$url
done
echo $START_TIME
date
