class Object:

    # Входные данные
    start_position = [0.0, 0.0]  # начальная координата по (Х, Y) (левый верхний угол объекта)
    start_velocity = [0.0, 0.0]  # начальная скорость по (X, Y)
    mass = 0  # масса
    image = 0  # картинка объекта
    size = [0.0, 0.0]  # размер объекта по оси (Х, Y)

    # Обновляющиеся данные
    current_position = [0.0, 0.0]  # нынешняя координата по (Х, Y)
    current_velocity = [0.0, 0.0]  # нынешняя скорость по (X, Y)
    a = [0.0, 0.0]  # ускорение частицы по оси (X, Y)
    q = 0  # заряд частицы

    # Константы
    precision = 7  # точность округления данных, константа, можно поменять, если очень надо
    world_size_x = [0, 800]  # размеры "мира" по оси Х
    world_size_y = [0, 400]  # размеры "мира" по оси Y
    field_size_x = [200, 800]  # размеры электростатического поля по оси Х
    field_size_y = [0, 400]  # размеры электростатического поля по оси Y
    field_E = 1  # напряженность поля, В/м
    field_direction = 1  # направление напряженности поля: 1 - вниз, 2 - вправо, 3 - вверх, 4 - влево
    K = 100  # количество пикселей в одном метре
    stopped = False
    accelerated = False

    # timers
    t = 0  # общий таймер
    help_timer = 0  # помогает подсчитать время действия силы
    a_t = 0  # время действия поля, при котором существует ускорение

    # Конструктор с заданием начальных значений величин
    def __init__(self, start_position, start_velocity, mass, q, size, image, u, d, k=100):
        self.start_position = self.current_position = list(start_position)
        self.start_velocity = self.current_velocity = list(start_velocity)
        self.start_velocity[0] *= k
        self.start_velocity[1] *= k
        self.mass = float(mass)
        self.q = float(q)
        self.size = [
            float(size[0]),
            float(size[1])
        ]
        self.image = image
        self.K = k
        self.field_E = u * 1000 / d  # т.к. d - в мм, а не в м

    # Передать информацию в виде списка
    def get_info(self):
        return [
            f"Current position: {self.current_position}",
            f"Mass: {self.mass * 10 ** 30} * 10^-30 кг",
            f"Current velocity: [{self.current_velocity[0] / self.K}, {self.current_velocity[1] / self.K}] м/с",
            f"Acceleration: [{round(self.a[0] / self.K / (10 ** 11), 3)} * 10^11, {round(self.a[1] / self.K / (10 ** 11), 3)}* 10^11] м/с^2",
            f"Q: {self.q * 10 ** 19} * 10^-19 Кл"
        ]

    # Округление полученных данных
    def round_data(self, precision):
        self.current_position = [
            round(self.current_position[0], precision),
            round(self.current_position[1], precision)
        ]
        self.current_velocity = [
            round(self.current_velocity[0], precision),
            round(self.current_velocity[1], precision)
        ]

    # Обновление скорости частицы, если она летит в электростатическом поле
    def update_velocity(self, t):
        if self.field_size_x[0] <= self.current_position[0] + self.size[0] // 2 <= self.field_size_x[1]:
            if self.field_size_y[0] <= self.current_position[1] + self.size[1] // 2 <= self.field_size_y[1]:
                # F = qE, F = ma => ma = qE => a = qE/m
                new_a = self.q / self.mass * self.field_E
                new_a *= self.K  # переводим из м/с в пиксель/с
                self.accelerated = True
                if self.field_direction == 1:  # вниз -> увеличение Y
                    self.a[1] = new_a
                elif self.field_direction == 2:  # вправо -> увеличение X
                    self.a[0] = new_a
                elif self.field_direction == 3:  # вверх -> уменьшение Y
                    self.a[1] = -new_a
                elif self.field_direction == 4:  # влево -> уменьшение X
                    self.a[0] = -new_a
        else:
            self.accelerated = False
            self.a = [0, 0]
            self.start_velocity[0] = self.current_velocity[0]
            self.start_velocity[1] = self.current_velocity[1]
        self.a_t = t - self.help_timer
        self.current_velocity[0] = self.start_velocity[0] + self.a[0] * self.a_t
        self.current_velocity[1] = self.start_velocity[1] + self.a[1] * self.a_t
        self.round_data(self.precision)

    # Проверки на границы с миром
    def check_collisions(self, new_position):
        self.stopped = True
        # Если уперся в правую границу мира
        if new_position[0] + self.size[0] >= self.world_size_x[1]:
            new_position[0] = self.world_size_x[1] - self.size[0]
        # Если уперся в левую границу
        elif new_position[0] <= self.world_size_x[0]:
            new_position[0] = self.world_size_x[0]
        # Если уперся в верхнюю границу
        elif new_position[1] + self.size[1] >= self.world_size_y[1]:
            new_position[1] = self.world_size_y[1] - self.size[1]
        # Если уперся в нижнюю границу
        elif new_position[1] <= self.world_size_y[0]:
            new_position[1] = self.world_size_y[0]
        else:
            self.stopped = False

    # Функция обновления позиции объекта
    def update_position(self, t):
        if self.stopped:
            return
        if not self.accelerated:
            self.help_timer = t
        self.update_velocity(t)
        # Считаем новую позицию объекта
        # X = X0 + V0*t + a*t^2/2
        # new_position = [
        #     self.current_position[0] + self.start_velocity[0] + self.a[0] / 2,
        #     self.current_position[1] + self.start_velocity[1] + self.a[1] / 2
        # ]
        new_position = [
            self.start_position[0] + self.start_velocity[0] * t + self.a[0] * self.a_t * self.a_t / 2,
            self.start_position[1] + self.start_velocity[1] * t + self.a[1] * self.a_t * self.a_t / 2
        ]
        # Позиция не изменилась - заканчиваем
        if new_position == self.current_position:
            return
        # Проверяем столкновения со стенами
        self.check_collisions(new_position)
        # Записываем новую координату
        self.current_position[0] = new_position[0]
        self.current_position[1] = new_position[1]
        self.round_data(self.precision)

    def set_world_size(self, world_size_x, world_size_y):
        self.world_size_x = world_size_x
        self.world_size_y = world_size_y

    def set_field_state(self, field_size_x, field_size_y, field_E):
        self.field_size_x = field_size_x
        self.field_size_y = field_size_y
        self.field_E = field_E

    def set_precision(self, precision):
        self.precision = precision
