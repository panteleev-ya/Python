def unique(a):
    b = []
    for i in range(len(a)):
        # Если еще нет такого элемента - добавляем
        if a[i] not in b:
            b.append(a[i])
    return b


def read_csv(_file_path):
    file = open(_file_path, encoding="utf-8")
    # Лист тегов из первой строки файла
    _tags = file.readline()
    _tags = list(_tags.split(','))
    # Костыль на первый столбец (ибо он изначально "undefined")
    _tags[0] = '\"id\"'
    # Костыль на последний столбец, ибо у него в конце "\n"
    _tags[len(_tags)-1] = _tags[len(_tags)-1][:-1]
    # Костыль на удаление лишних ебучих кавычек ибо они меня бесят
    for t in range(len(_tags)):
        if _tags[t][0] == '\"':
            _tags[t] = _tags[t][1:]
        if _tags[t][len(_tags[t])-1] == '\"':
            _tags[t] = _tags[t][:-1]
    # Двумерный массив строк csv файла
    _arr = []

# Вот тут надо бы убрать срезание до первых 10 ;)
    for line in file.readlines()[:10]:
        # Делим строку на столбцы
        _line = line.split(',')
        # Убираем "\n" из конца строки
        _line[len(_line)-1] = _line[len(_line)-1][:-1]
        # Убираем ебучие кавычки
        for l in range(len(_line)):
            _line[l] = _line[l][1:-1]
        _arr.append(_line)
    return _tags, _arr


def get_check(_tags, _data):
    # Копируем лист строк csv
    _id = list(_data)
    # Берем из каждой строки только IDПользователя
    for i in range(len(_id)):
        _id[i] = _id[i][3]
    # Из списка IDПользователя выбираем только уникальные
    _un_id = unique(_id)
    # Создаем трехмерный список чеков arr[IDПользователя][category][element]
    _arr = []
    for i in range(len(_un_id)):
        _arr.append([])
    # Обрабатываем каждую строку csv файла
    for line in _data:
        # Получаем номер данного IDПользователя в списке уникальных
        ind = _un_id.index(line[3])
        # Добавляем всю информацию о покупках пользователя по его IDПользователя в лист
        _arr[ind].append(list(line[3:]))
    return _arr


def print_check(_check):
    # Просто тупая функция красивого вывода информации о чеках
    for a in range(len(_check)):
        print(_check[a][0][0])
        print(f"    {len(_check[a])}")
        for b in _check[a]:
            print(f"    {b[1:]}")
