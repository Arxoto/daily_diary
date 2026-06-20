# visit https://www.tunemymusic.com/zh-CN/home
cat all.csv | sed 1d | awk -f 1_parse_print.awk -v output_split=' - '
