from math import cos
from math import tan
from math import pi


class Ladder:
    precision = 7  # точность округления данных
    output_precision = 3  # точность округления выводимых данных

# Заранее известные константы
    arc_a = -9.81  # Ускорение дуги по оси Y (масса плазмы отрицательна)
    air_E_min = 3 * 10 ** 6  # Электрическая прочность воздушного промежутка (В/м) 3000в/мм => 15000/х = 3000 => х = 5мм, а в Галилео было около 3см разница, но дуга все равно разрывалась
    g = 9.81  # Ускорение свободного падения (м/с^2)
    ion_y = 5 * 10 ** (-2)  # Коэффициент вторичной ионизации

    atmosphere_pressure = 10 ** 5  # Абсолютное давление (Па)
    air_temperature = 273.15  # Температура воздуха (K) (0 *С)

    arc_temperature = 9273.15  # Температура плазмы (К) (9000 *C)
    arc_p = 0.00114  # Удельное сопротивление плазмы (в Ом*мм^2/м)
    arc_S = 0.23758 * 10 ** (-7)  # Площадь поперечного сечения дуги
    stick_length = 1  # Длина проводников (м)

# Входные данные
    stick_angle = 0  # Угол между проводниками - [0; 90] (в градусах) (до целых) -> переводится в радианы при просчете косинуса
    stick_d = 0  # Расстояние между проводниками в нижней точке - [0.001; 1.000] (в метрах) (до тысячных)
    stick_p = 0  # Удельное сопротивление проводников - [0.015; 1.500] (в Ом*мм^2/м)
    stick_S = 0  # Площадь поперечного сечения провода - [0.5; 1600.0] (в мм^2) (до десятых)

    battery_U = 0  # Напряжение на выходе из источника питания - [0; 10000] (в Вольтах) (до целых)
    battery_I = 0  # Сила тока источника - [0.0, 10.0] (в Амперах) (до десятых)

    wire_length = 0  # Длина проводов между источником и проводниками - [0.1; 10.0] (в метрах) (до десятых)
    wire_p = 0  # Удельное сопротивление проводов - [0.015; 1.500] (в Ом*мм^2/м)
    wire_S = 0  # Площадь поперечного сечения провода - [0.5; 1600.0] (в мм^2) (до десятых)
    start_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # содержит все начальные параметры дуги
# Вычисленные, не изменяющиеся данные
    wire_R = 0  # (R = p*l/S) -> сопротивление каждого провода (они оба одинаковые)
    wire_Q_dt = 0  # (Q/t = I^2*R) -> выделяемое количество теплоты на каждом проводе в секунду
    wire_U = 0  # (U = I*R) -> напряжение на каждом проводе (В)

    arc_start_U = 0  # (U = Uобщ - Uп1 - Uп2 = Uобщ - 2*Uп) -> начальное напряжение эл. дуги
    arc_start_E = 0  # (E = U/d) -> начальная напряженность поля, образовавшегося между проводниками
    arc_h = 0  # (h = at^2/2, a - ускорение дуги, h0 = 0, v0 = 0) -> высота, на которую поднялась дуга
    arc_start_position = [794, 590]  # стартовая позиция дуги == [середина между проводниками, самая нижняя точка между проводниками]
    arc_length = 0  # (2*d = h * tg(a/2)) -> расстояние между проводниками на данной высоте
    arc_max_h = 0  # максимальная высота подъема дуги
    arc_R = 0  # сопротивление дуги
    ion_a = 0  # (0.2 * (E - 24.5)^2) -> Коэффициент ударной ионизации

# Обновляющиеся данные
    stick_passed_length = 0  # (length = h/cos(a/2)) -> длина проводника, которое дуга уже преодолела
    stick_passed_R = 0   # (R = p*l/S) -> сопротивление участка проводника, который теперь тоже является участком электрической цепи
    stick_passed_U = 0  # (U = I*R) -> напряжение на каждом проводнике (В)

    arc_position = 0  # стартовая позиция дуги == [середина между проводниками, самая нижняя точка между проводниками]
    delta_X = 0  # расстояние от левого проводника до центра
    arc_U = 0  # (U = Uобщ - 2*U_w - 2*U_s) -> напряжение дуги
    arc_E = 0  # (E = U/d) -> напряженность дуги
    arc_exist = 0  # 0 - нет дуги, 1 - есть дуга

    # Конструктор с заданием начальных значений величин
    def __init__(self, angle, d, U, length, wire_p, wire_S, stick_p, stick_S, y):
        self.stick_angle = angle
        self.stick_d = d
        self.arc_length = d
        self.battery_U = U
        self.wire_length = length
        self.wire_p = wire_p
        self.wire_S = wire_S
        self.stick_p = stick_p
        self.stick_S = stick_S
        self.ion_y = y
        return

    # Округление полученных данных
    def round_data(self):
        self.arc_position = [
            round(self.arc_position[0], self.precision),
            round(self.arc_position[1], self.precision)
        ]
        # добавить сюда все, что будет выводиться на экран

    # Обновить данные до начальных
    def reload_data(self):
        self.arc_h = 0
        self.make_start_calculations()
        # self.arc_h = self.start_data[0]
        # self.stick_passed_length = self.start_data[1]
        # self.stick_passed_R = self.start_data[2]
        # self.arc_length = self.start_data[3]
        # self.arc_R = self.start_data[4]
        # self.battery_I = self.start_data[5]
        # self.wire_U = self.start_data[6]
        # self.stick_passed_U = self.start_data[7]
        # self.arc_U = self.start_data[8]
        # self.arc_E = self.start_data[9]
        # self.arc_position = self.start_data[10]
        return

    # Стартовые рассчеты
    def make_start_calculations(self):

        # Вычисляем сопротивление проводов
        self.wire_R = self.wire_p * self.wire_length / self.wire_S  # R = p * l / S

        # Вычисляем напряжение между проводниками в самой нижней точке (точке с самым маленьким расстоянием между проводниками)
        self.arc_start_U = self.battery_U - 2 * self.wire_U  # (U = Uобщ - Uп1 - Uп2 = Uобщ - 2*Uп)

        # Вычисляем напряженность поля, образовавшегося между проводниками (по формуле заряженного конденсатора)
        self.arc_start_E = self.arc_start_U / self.stick_d  # (E = U/d)

        # Проверяем, больше ли получившееся напряжение, чем необходимое для "пробития" - полной потери диэлектриком (воздухом) изолирующих свойств
        if self.arc_start_E >= self.air_E_min:
            self.arc_exist = True  # дуга "зажжется"
        else:
            self.arc_exist = False  # дуга не "зажжется"

        # Записать стартовые данные для дуги
        # self.start_data = [
        #     self.arc_h,
        #     self.stick_passed_length,
        #     self.stick_passed_R,
        #     self.arc_length,
        #     self.arc_R,
        #     self.battery_I,
        #     self.wire_U,
        #     self.stick_passed_U,
        #     self.arc_U,
        #     self.arc_E,
        #     self.arc_position
        # ]
        return

    # Функция обновления позиции объекта
    def make_regular_calculations(self, t):

        if self.arc_exist:  # если дуга "зажглась", иначе - ничего не проверяем

            # Вычисляем высоту, на которую поднялась дуга
            self.arc_h = -self.arc_a * t * t / 2  # h = at^2 / 2
            if self.arc_h > self.arc_max_h:
                self.arc_max_h = self.arc_h

            # Вычисляем длину участка проводника, который теперь добавляется к компонентам цепи
            self.stick_passed_length = self.arc_h / cos((self.stick_angle * pi / 180) / 2)  # (hд / cos(a / 2))

            # Вычисляем сопротивление данного участка проводника
            self.stick_passed_R = self.stick_p * self.stick_passed_length / self.stick_S  # (Rпр = p * l / S)

            # Вычисляем длину получившейся дуги
            self.delta_X = self.arc_h * tan((self.stick_angle * pi / 180) / 2)
            L = self.stick_d + 2 * self.delta_X  # (L = L0 + 2 * delta X)
            self.arc_length = L / 2 * (1 + 1 / cos((self.stick_angle * pi / 180) / 2))  # (len = L / 2 * (1 + 1 / cos(a / 2) ))
            print(self.arc_length / L)

            # Вычисляем сопротивление получившейся дуги
            self.arc_R = self.arc_p * self.arc_length / self.arc_S  # (Rд = p * l / S)

            # Вычисляем силу тока в цепи
            self.battery_I = self.battery_U / (2 * self.wire_R + 2 * self.stick_passed_R + self.arc_R)  # Iобщ = Uобщ / Rобщ

            # Вычисляем напряжения на проводах
            self.wire_U = self.battery_I * self.wire_R  # (Uп = Iобщ * Rп)

            # Вычисляем напряжения на участках проводников
            self.stick_passed_U = self.battery_I * self.stick_passed_R   # (Uпр = Iобщ * Rпр)

            # Вычисляем напряжения на получившейся дуге
            self.arc_U = self.battery_U - 2 * (self.wire_U + self.stick_passed_U)  # (U = Uобщ - 2*Uп - 2*Uпр)

            # Вычисляем напряженность на дуге (нужна для коэффициента ударной ионизации)
            self.arc_E = self.arc_U / self.arc_length  # (E = U/d)

            # Вычисляем выделяемое количество теплоты на каждом проводе в секунду
            self.wire_Q_dt = (self.battery_I ** 2) * self.wire_R  # (Q/t = I^2*R)

            # Вычисляем позицию центра дуги
            self.arc_position = [
                self.arc_start_position[0],               # позиция по оси X не меняется
                self.arc_start_position[1] + self.arc_h   # позиция по оси Y получается по формуле
            ]

            # Проверка на достижение максимального положения
            if self.stick_passed_length >= self.stick_length:
                self.arc_exist = False
        return

    # Передать информацию в виде списка
    def get_info(self):
        return [
            ["Battery -> U", str(round(self.battery_U, self.output_precision)) + " В"],
            ["Battery -> I", str(round(self.battery_I, self.output_precision)) + " A"],
            ["Stick -> d", str(self.stick_d) + " м"],
            ["Wires -> R", str(round(self.wire_R, self.output_precision)) + " Ом"],
            ["Sticks -> R", str(round(self.stick_passed_R, self.output_precision)) + " Ом"],
            ["Arc -> R", str(round(self.arc_R, self.output_precision)) + " Ом"],
            ["Wires -> U", str(round(self.wire_U, self.output_precision)) + " В"],
            ["Sticks -> U", str(round(self.stick_passed_U, self.output_precision)) + " В"],
            ["Arc -> U", str(round(self.arc_U, self.output_precision)) + " В"],
            ["Arc -> E", str(round(self.arc_start_E, self.output_precision)) + " В/м"],
            ["Arc -> H_max", str(round(self.arc_max_h, self.output_precision)) + " м"],
        ]

    def set_precision(self, precision):
        self.precision = precision
        return
