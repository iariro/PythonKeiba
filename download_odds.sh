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
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202501080120250125/A9
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0107202501080120250125/F3
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0110202501010120250125/F1
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0106202501090120250126/D9
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0107202501090120250126/23
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0110202501020120250126/21
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0105202501010120250201/0D
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0108202501010120250201/EB
# https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0110202501030120250201/AA

for url in `cat << EOF
https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0110202501040120250202/DA
https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0108202501020120250202/1B
https://www.jra.go.jp/JRADB/accessD.html?CNAME=pw01dde0105202501020120250202/3D
EOF`
do
  python3 download_odds.py -url=$url $*
done

date
