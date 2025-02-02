#!/bin/sh

# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202405030120241207/3C
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0108202407030120241207/32
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0107202404030120241207/55
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202405050120241214/45
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0108202407050120241214/3B
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0107202404050120241214/5E
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202405060120241215/75
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0108202407060120241215/6B
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0107202404060120241215/8E
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1006202405070120241221/2D
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202407070120241221/23
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202405080120241222/7E
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0108202407080120241222/74
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1006202405090120241228/3E
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202407090120241228/34
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1006202501010120250105/6B
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1007202501010120250105/B5
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202501020120250106/BC
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0107202501020120250106/06
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202501030120250111/D8
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0107202501030120250111/22
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0107202501040120250112/52
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202501040120250112/08
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202501050120250113/38
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0107202501050120250113/82
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202501060120250118/5C
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0107202501060120250118/A6
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202501070120250119/8C
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0107202501070120250119/D6
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202501080120250125/65
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0107202501080120250125/AF
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0110202501010120250125/AD
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0110202501021220250126/E4
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0107202501091220250126/E6
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202501091220250126/9C
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0105202501011220250201/D0
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0108202501011220250201/AE
# https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0110202501031220250201/6D
START_TIME=$(date)
for url in `cat << EOF
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0105202501020120250202/F9
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0108202501020120250202/D7
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0110202501040120250202/96
EOF`
do
  python3 download_result.py -url=$url
done
echo $START_TIME
date
