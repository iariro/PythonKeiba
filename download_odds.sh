#!/bin/sh

# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202405030120241207/80
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0108202407030120241207/76
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0107202404030120241207/99
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202405040120241208/B0
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0108202407040120241208/A6
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0107202404040120241208/C9
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202405050120241214/89
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0108202407050120241214/7F
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0107202404050120241214/A2
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202405060120241215/B9
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0108202407060120241215/AF
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0107202404060120241215/D2
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202405070120241221/92
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0108202407070120241221/88
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202405080120241222/C2
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0108202407080120241222/B8
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202405090120241228/A3
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0108202407090120241228/99
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202501010120250105/D0
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0107202501010120250105/1A
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202501020120250106/00
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0107202501020120250106/4A
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202501030120250111/1C
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0107202501030120250111/66
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202501040120250112/4C
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0107202501040120250112/96
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202501050120250113/7C
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0107202501050120250113/C6
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202501060120250118/A0
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0107202501060120250118/EA
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202501070120250119/D0
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0107202501070120250119/1A

for url in `cat << EOF
https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202501080120250125/A9
https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0107202501080120250125/F3
https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0110202501010120250125/F1
EOF`
do
  ./download_odds.py -url=$url $*
done

date
