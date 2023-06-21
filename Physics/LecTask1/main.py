import matplotlib.pyplot as plt


def to_binary_str(s):
    return " ".join(f"{ord(i):08b}" for i in s)


def calculate_delta_t_dispersion(c, b, lambda_0, L, delta_lambda):
    D = b ** 2 * lambda_0 / (c ** 2 + b ** 2 * lambda_0 ** 2) * 0.5
    delta_t_dispersion = (D * L * delta_lambda) / lambda_0 ** 2
    return delta_t_dispersion


c = 3e8
L = 1  # предполагаемая длина среды в метрах
lambda_0 = 1.5e-6
delta_t = 1e-5
delta_lambda = 1 / delta_t
for b in [1, 10, 100]:
    delta_t_dispersion = calculate_delta_t_dispersion(c, b, lambda_0, L, delta_lambda)
    print(f"Характерное время расплывания пакета для b = {b}: {delta_t_dispersion} с")

word = "qubit"
binary_code_str = to_binary_str(word)
print(f"Слово: {word}")
print(f"Двоичный код: {binary_code_str}")

binary_code = binary_code_str.replace(" ", "")

time_points = []
current_time = 0

L = 1
b = 1000
delta_t_dispersion = calculate_delta_t_dispersion(c, b, lambda_0, L, delta_lambda)
bit_time = delta_t_dispersion / len(binary_code)  # время для прохождения одного бита
for bit in binary_code:
    time_points.append(current_time)
    time_points.append(current_time + bit_time)
    current_time += bit_time

values = []
for bit in binary_code:
    if bit == "0":
        values.extend([0, 0])
    elif bit == "1":
        values.extend([1, 1])

plt.plot(time_points, values)
plt.title(f"Слово: {word}\nКод: {binary_code}")
plt.xlabel("Время")
plt.ylabel("Амплитуда")
plt.ylim(-0.5, 1.5)
plt.show()
