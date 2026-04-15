cat all.csv | sed 1d | awk -F'","' '{ print $1}' | tr -d '"' | termux-clipboard-set
