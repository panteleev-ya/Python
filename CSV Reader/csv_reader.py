from resources import unique, read_csv, get_check, print_check

# Не забыть, что в дата у нас добавляются только первые 10 строк из Data.csv
tags, data = read_csv("Data.csv")
check = get_check(tags, data)
print_check(check)
