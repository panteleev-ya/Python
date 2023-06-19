import matplotlib.pyplot as plt


def to_binary_digits(s):
    """
    Переводит строку в двоичный код (список нулей и единиц)

    :param s:
    :return:
    """
    return [int(digit) for i in s for digit in f"{ord(i):b}"]


def meander(binary_digits, frequency):
    """
    Функция преобразует двоичный код в список значений функции меандра.

    :param binary_digits: двоичный код
    :param frequency: количество точек на графике для каждого бита кода (начало и конец)
    :return: список значений функции меандра
    """
    return [int(digit) for digit in binary_digits for _ in range(frequency)]


word = "physics"
word_binary_digits = to_binary_digits(word)

print(f"Word: {word}")
print(f"Binary: {word_binary_digits}")

meander_values = meander(
    binary_digits=word_binary_digits,
    frequency=2
)

x_labels = list(range(len(meander_values)))
plt.plot(x_labels, meander_values, color='green')
plt.ylabel("Значение")
plt.xlabel("Время")
plt.title(f"Слово: {word}")
plt.show()
