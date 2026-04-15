cat all.csv | sed 1d | awk -F'","' '{ print $1," - ",$2}' | tr -d '"' \
| grep -v 'Landing Guy' \
| grep -v '女儿情' \
| grep -v '女兒情'

echo 'Landing Guy  -  刘昊霖'
echo '女儿情  -  吴静'
