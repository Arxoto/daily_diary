cat all.csv | sed 1d | awk -F'","' '{ print $1," - ",$2}' | tr -d '"' | grep -v 'Landing Guy'
echo 'Landing Guy  -  刘昊霖'