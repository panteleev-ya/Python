from math import cos
from math import tan
from math import pi
from math import log


class Ladder:
    precision = 7  # точность округления данных
    output_precision = 3  # точность округления выводимых данных

# Заранее известные константы
    # Общие константы
    arc_a = -9.81  # Ускорение дуги по оси Y (масса плазмы отрицательна)
    dielectric_strength = 3 * 10 ** 6  # Электрическая прочность воздушного промежутка (В/м) 3000в/мм => 15000/х = 3000 => х = 5см, а в Галилео было около 3см разница, но дуга все равно разрывалась
    gas_R = 8.31446  # Универсальная газовая постоянная (Дж/(моль*К))
    g = 9.81  # Ускорение свободного падения (м/с^2)
    ion_y = 5 * 10 ** (-2)  # Коэффициент вторичной ионизации

    # Все про воздух
    atmosphere_pressure = 10 ** 5  # Абсолютное давление (Па)
    air_temperature = 273.15  # Температура воздуха (K) (0 *С)
    # air_M = 29 * 10**(-3)  # Молярная масса воздуха (кг/моль)

    # Все про дугу
    arc_temperature = 9273.15  # Температура плазмы (К) (9000 *C)
    # arc_M = 29 * 10**(-3)  # Молярная масса ионизированного воздуха (кг/моль)
    stick_length = 1  # Длина проводников (м)

# Входные данные
    # Все про проводники
    stick_angle = 0  # Угол между проводниками - [0; 90] (в градусах) (до целых) -> переводится в радианы при просчете косинуса
    stick_d = 0.001  # Расстояние между проводниками в нижней точке - [0.001; 1.000] (в метрах) (до тысячных)
    stick_p = 0.015  # Удельное сопротивление проводников - [0.015; 1.500] (в Ом*мм^2/м)
    stick_S = 0.5  # Площадь поперечного сечения провода - [0.5; 1600.0] (в мм^2) (до десятых)

    # Все про источник питания
    battery_U = 0  # Напряжение на выходе из источника питания - [0; 10000] (в Вольтах) (до целых)
    battery_I = 0  # Сила тока источника - [0.0, 10.0] (в Амперах) (до десятых)

    # Все про провода
    wire_length = 0.1  # Длина проводов между источником и проводниками - [0.1; 10.0] (в метрах) (до десятых)
    wire_p = 0.015  # Удельное сопротивление проводов - [0.015; 1.500] (в Ом*мм^2/м)
    wire_S = 0.5  # Площадь поперечного сечения провода - [0.5; 1600.0] (в мм^2) (до десятых)

# Вычисленные, не изменяющиеся данные
    # Все про провода
    wire_R = 0  # wire_p * wire_length / wire_S                                                                              # (R = p*l/S) -> сопротивление каждого провода (они оба одинаковые)
    wire_Q_dt = 0  # (battery_I ** 2) * wire_R                                                                               # (Q/t = I^2*R) -> выделяемое количество теплоты на каждом проводе в секунду
    wire_U = 0  # battery_I * wire_R                                                                                         # (U = I*R) -> напряжение на каждом проводе (В)

    # Все про воздух
    # air_p = 0  # atmosphere_pressure * air_M / (gas_R * air_temperature)                                                     # (P = (p*M)/(R*T)) -> плотность воздуха (кг/м^3)

    # Все про дугу
    arc_start_U = 0  # battery_U - 2 * wire_U                                                                                # (U = Uобщ - Uп1 - Uп2 = Uобщ - 2*Uп) -> начальное напряжение эл. дуги
    arc_start_E = 0  # arc_start_U / stick_d                                                                                 # (E = U/d) -> начальная напряженность поля, образовавшегося между проводниками
    arc_h = 0                                                                                                           # (h = at^2/2, a - ускорение дуги, h0 = 0, v0 = 0) -> высота, на которую поднялась дуга
    # arc_p = 0  # atmosphere_pressure * arc_M / (gas_R * arc_temperature)                                                     # (P = (p*M)/(R*T)) -> плотность дуги (кг/м^3)
    arc_start_position = 0  # [794, 590]                                                                                     # стартовая позиция дуги == [середина между проводниками, самая нижняя точка между проводниками]
    # arc_a = -g  # (air_p / arc_p - 1) * g                                                                                     # (ma = pgV - mg, p - плотность воздуха => a = (p1/p2 - 1)g) -> ускорение дуги (по оси Y)
    arc_max_h = 0  # "undefined"  # cos((stick_angle * pi / 180) / 2)                                                        # h_max = cos(a/2) -> максимальная высота подъема дуги
    ion_a = 0  # 1                                                                                                           # (0.2 * (E - 24.5)^2) -> Коэффициент ударной ионизации

    # Условие образования дуги
    required_stick_U = 0  # dielectric_strength * stick_d                                                                    # (Up = Ep/d) -> мин. напряжение, при котором образуется эл. дуга
# Обновляющиеся данные
    # Все про проводники
    stick_passed_length = 0  # arc_h / cos((stick_angle * pi / 180) / 2)                                                     # (length = h/cos(a/2)) -> длина проводника, которое дуга уже преодолела
    stick_passed_d = 0  # stick_d + 2 * arc_h * tan((stick_angle * pi / 180) / 2)                                                      # (2*d = h * tg(a/2)) -> расстояние между проводниками на данной высоте
    stick_passed_R = 0  # stick_p * stick_passed_length / stick_S                                                            # (R = p*l/S) -> сопротивление участка проводника, который теперь тоже является участком электрической цепи
    stick_passed_U = 0  # battery_I * stick_passed_R                                                                         # (U = I*R) -> напряжение на каждом проводнике (В)

    # Все про дугу
    arc_position = 0  # arc_start_position                                                                                   # стартовая позиция дуги == [середина между проводниками, самая нижняя точка между проводниками]
    arc_U = 0  # battery_U - 2 * (wire_U + stick_passed_U)                                                                   # (U = Uобщ - 2*U_w - 2*U_s) -> напряжение дуги
    arc_E = 0  # arc_U / stick_passed_length                                                                            # (E = U/d)

    # Конструктор с заданием начальных значений величин
    def __init__(self, angle, d, U, I, length, wire_p, wire_S, stick_p, stick_S, y):
        self.stick_angle = angle
        self.stick_d = d
        self.battery_U = U
        self.battery_I = I
        self.wire_length = length
        self.wire_p = wire_p
        self.wire_S = wire_S
        self.stick_p = stick_p
        self.stick_S = stick_S
        self.ion_y = y

    # Округление полученных данных
    def round_data(self):
        self.arc_position = [
            round(self.arc_position[0], self.precision),
            round(self.arc_position[1], self.precision)
        ]
        # self.arc_a = round(self.arc_a, self.precision)
        # return [
        #     f"U: {self.battery_U}",
        #     f"I: {self.battery_I}",
        #     f"Wires -> R: {self.wire_R}",
        #     f"Wires -> Q/t: {self.wire_Q_dt}",
        #     f"Arc -> U: {self.arc_U}",
        #     f"Arc -> length: {self.stick_passed_length}",
        #     f"Arc -> E: {self.arc_E}",
        #     f"Arc -> H_max: {self.arc_max_h}"
        # ]
        # добавить сюда все, что будет выводиться на экран

    # Стартовые рассчеты
    def make_start_calculations(self):
        # Вычисленные, не изменяющиеся данные
        # Все про провода
        self.wire_R = self.wire_p * self.wire_length / self.wire_S                                                      # (R = p*l/S) -> сопротивление каждого провода (они оба одинаковые)
        self.wire_Q_dt = (self.battery_I ** 2) * self.wire_R                                                            # (Q/t = I^2*R) -> выделяемое количество теплоты на каждом проводе в секунду
        self.wire_U = self.battery_I * self.wire_R                                                                      # (U = I/R) -> напряжение на каждом проводе (В)

        # Все про воздух
        # self.air_p = self.atmosphere_pressure * self.air_M / (self.gas_R * self.air_temperature)                        # (P = (p*M)/(R*T)) -> плотность воздуха (кг/м^3)

        # Все про дугу
        self.arc_start_U = self.battery_U - 2 * self.wire_U                                                             # (U = Uобщ - Uп1 - Uп2 = Uобщ - 2*Uп) -> начальное напряжение эл. дуги
        self.arc_start_E = self.arc_start_U / self.stick_d                                                              # (E = U/d) -> начальная напряженность поля, образовавшегося между проводниками
        # self.arc_p = self.atmosphere_pressure * self.arc_M / (self.gas_R * self.arc_temperature)                        # (P = (p*M)/(R*T)) -> плотность дуги (кг/м^3)
        self.arc_start_position = [794, 590]                                                                            # стартовая позиция дуги == [середина между проводниками, самая нижняя точка между проводниками]
        # self.arc_a = (self.air_p / self.arc_p - 1) * self.g                                                             # (ma = pgV - mg, p - плотность воздуха => a = (p1/p2 - 1)g) -> ускорение дуги (по оси Y)
        # self.arc_max_h = cos((self.stick_angle * pi / 180) / 2)                                                         # h_max = cos(a/2), если  -> максимальная высота подъема дуги

        # Условие образования дуги
        self.required_stick_U = self.dielectric_strength * self.stick_d                                                 # (Up = Ep/d) -> мин. напряжение, при котором образуется эл. дуга
        return

    # Функция обновления позиции объекта
    def make_regular_calculations(self, t):

        # Обновляющиеся данные
        # Обновляем высоту дуги
        self.arc_h = self.arc_a * t * t / 2                                                                             # h = at^2 / 2 -> высота, на которую поднялась дуга

        # Все про проводники
        self.stick_passed_length = self.arc_h / cos((self.stick_angle * pi / 180) / 2)                                  # (h/cos(a/2)) -> длина проводника, которое дуга уже преодолела
        self.stick_passed_R = self.stick_p * self.stick_passed_length / self.stick_S                                    # (R = p*l/S) -> сопротивление участка проводника, который теперь тоже является участком электрической цепи
        self.stick_passed_U = self.battery_I * self.stick_passed_R                                                      # (U = I*R) -> напряжение на каждом проводнике (В)
        self.stick_passed_d = self.stick_d + 2 * self.arc_h * tan((self.stick_angle * pi / 180) / 2)

        # Все про дугу
        self.arc_U = self.battery_U - 2 * (self.wire_U + self.stick_passed_U)                                           # (U = Uобщ - 2*U_w - 2*U_s) -> напряжение дуги
        self.arc_E = self.arc_U / self.stick_passed_d                                                                   # (E = U/d)

        self.arc_position = [
            self.arc_start_position[0],                                                                                 # позиция по оси X не меняется
            self.arc_start_position[1] + self.arc_h                                                                     # позиция по оси Y получается по формуле
        ]
        self.round_data()

        # Проверку на то, что дуга не выше ее максимальной высоты или она не оборвалась
        self.ion_a = 0.2 * ((self.arc_E - 24.5) ** 2)                                                                   # рассчитываем коэффициент ударной ионизации
        if self.stick_passed_d <= log(1 / self.ion_y) / self.ion_a:                                                      # обрыв происходит при (y*e^(aS) < 1 => S < log(1/y)/a, где S - расстояние между спицами)
            self.arc_max_h = self.arc_position[1]
            self.arc_position = list(self.arc_start_position)
        return

    # Передать информацию в виде списка
    def get_info(self):
        return [
            ["Battery -> U", round(self.battery_U, self.output_precision)],
            ["Battery -> I", round(self.battery_I, self.output_precision)],
            ["Wires -> R", round(self.wire_R, self.output_precision)],
            ["Wires -> Q/t", round(self.wire_Q_dt, self.output_precision)],
            ["Arc -> U", round(self.arc_U, self.output_precision)],
            ["Arc -> E", round(self.arc_E, self.output_precision)],
            ["Arc -> length", round(self.stick_passed_length, self.output_precision)],
            ["Arc -> H_max", round(self.arc_max_h, self.output_precision)]
        ]

    def set_precision(self, precision):
        self.precision = precision
        return
