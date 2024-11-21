#!/bin/sh

rm race_result.json

for url in `cat << EOF
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202404010120241005/4A
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202405010120241005/59
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202404020120241006/7A
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202405020120241006/89

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202405030120241012/62
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202404030120241013/10
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202405040120241013/92
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202404040120241014/40

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202404050120241019/64
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202405050120241019/73
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202404060120241020/8C
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202405060120241020/9B

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202404070120241026/6D
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202405070120241026/7C
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202404080120241027/9D
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202405080120241027/AC

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202405010120241102/BF
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202406010120241102/CE
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202405020120241103/EF
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202406020120241103/FE

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202405030120241109/D0
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202406030120241109/DF
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202405040120241110/F8
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202406040120241110/07

https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202405050120241116/D9
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202406050120241116/E8
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1005202405060120241117/09
https://www.jra.go.jp/JRADB/accessS.html?CNAME=pw01sde1008202406060120241117/18
EOF`
do
  python3 download_result.py -url=$url
done
