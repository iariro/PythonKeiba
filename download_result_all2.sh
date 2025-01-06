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
START_TIME=$(date)
for url in `cat << EOF
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1006202501010120250105/6B
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1007202501010120250105/B5
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0106202501020120250106/BC
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde0107202501020120250106/06
EOF`
do
  python3 download_result.py -url=$url
done
echo $START_TIME
date