cat all.csv | sed 1d | awk -f 1_parse_print.awk
