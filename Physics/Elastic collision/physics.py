class Object:

    # Входные данные
    name = "Truck"  # вид физического объекта (Truck, Wall)
    start_position = 0  # начальная координата по Х (крайней левой части объекта)
    start_velocity = 0  # начальная скорость
    mass = 0  # масса
    image = 0  # картинка объекта
    size_x = 0  # размер объекта по оси Х
    size_y = 0  # размер объекта по оси У

    # Обновляющиеся данные
    current_position = 0  # нынешняя координата по Х
    current_velocity = 0  # нынешняя скорость
    energy_loss = 0  # потери энергии (отличны от нуля только при неупругом столкновении)

    # Константы
    precision = 5  # точность округления данных, константа, можно поменять, если очень надо
    world_size = 800  # размер "мира" по оси Х

    # Конструктор с заданием начальных значений величин
    def __init__(self, start_position, mass, start_velocity, image, size, name="Truck"):
        self.start_position = self.current_position = start_position
        self.mass = float(mass)
        self.start_velocity = self.current_velocity = start_velocity
        self.image = image
        self.size_x = float(size[0])
        self.size_y = float(size[1])
        self.name = name

    # Столкновение тележки с другой тележкой
    def collision(self, opponent, collision_type):  # функция просчета конечных величин
        if collision_type == 3:  # столкновение со стеной == остановка
            self.current_velocity *= -1
            # self.current_velocity = 0
            self.round_data(self.precision)
        else:
            m1 = self.mass
            m2 = opponent.mass
            v1 = self.current_velocity
            v2 = opponent.current_velocity
            if collision_type == 0:  # упругое столкновение
                # Это было для варианта без столкновений двух движущихся объектов
                # self.current_velocity = (m1 - m2) * v1 / (m1 + m2)  # изменяем скорость первой тележки
                # opponent.current_velocity = 2 * m1 * v1 / (m1 + m2)  # изменяем скорость второй тележки
                self.current_velocity = ((m1 - m2)*v1 + 2*m2*v2) / (m1 + m2)
                opponent.current_velocity = v1 - v2 + self.current_velocity
            else:
                self.current_velocity = opponent.current_velocity = m1 * v1 / (m1 + m2)  # изменение скорости тележек
                self.energy_loss = opponent.energy_loss = m1 * m2 * v1 * v1 / (2 * (m1 + m2))  # потери энергии тележек
            self.round_data(self.precision)
            opponent.round_data(opponent.precision)

    # Вывод информации об объекте в консоль
    def print(self):
        print("Start position:", self.start_position)
        print("Current position:", self.current_position)
        print("Start velocity:", self.start_velocity)
        print("Current velocity:", self.current_velocity)
        print("Energy loss:", self.energy_loss)
        print("Mass:", self.mass)

    # Округление полученных данных
    def round_data(self, precision):
        self.current_position = round(self.current_position, precision)
        self.current_velocity = round(self.current_velocity, precision)
        self.energy_loss = round(self.energy_loss, precision)

    # Функция обновления позиции объекта
    def update_position(self, closest_object, collision_type):
        new_position = round(self.current_position + self.current_velocity, self.precision)  # считаем новую позицию нашего объекта
        # is_rounded = False
        if new_position == self.current_position:
            return

        # Проверка на "упирание" объекта в его соседа
        if round(closest_object.current_position + closest_object.size_x, closest_object.precision) <= self.current_position:  # если сосед был слева
            if new_position < round(closest_object.current_position + closest_object.size_x, closest_object.precision):
                new_position = round(closest_object.current_position + closest_object.size_x, closest_object.precision)  # не упереться в объект слева
                # if closest_object.size_x > 0:  # если это не левая стена
                    # is_rounded = True
            elif new_position > self.world_size - self.size_x:
                new_position = self.world_size - self.size_x  # не упереться в правую границу мира
        elif closest_object.current_position >= round(self.current_position + self.size_x, self.precision):  # если сосед был справа
            if round(new_position + self.size_x, self.precision) > closest_object.current_position:
                new_position = round(closest_object.current_position - self.size_x, self.precision)  # не упереться в объект справа
                # if closest_object.size_x > 0:  # если это не правая стена
                    # is_rounded = True
            elif new_position < 0:
                new_position = 0  # не упереться в левую границу мира
        # if self.current_position == new_position and not is_rounded:
        #     self.current_velocity = 0
        self.current_position = new_position
        self.round_data(self.precision)

        # Проверка на коллизии объекта с соседом
        if self.current_position == round(closest_object.current_position + closest_object.size_x, closest_object.precision):  # объект справа от соседа
            self.collision(closest_object, collision_type)
        elif round(self.current_position + self.size_x, self.precision) == closest_object.current_position:  # объект слева от соседа
            self.collision(closest_object, collision_type)

    def set_world_size(self, world_size):
        self.world_size = world_size

    def set_precision(self, precision):
        self.precision = precision


class World:

    # Входные данные
    size_x = 800  # размер мира по оси Х
    size_y = 400  # размер мира по оси У
    collision_type = 0  # тип столкновения

    # Обновляемые данные
    object_list = []

    # Константы
    wall_left = Object(0, 1000, 0, -1, (0, 1000), "Wall")  # левая стена
    wall_right = Object(size_x, 1000, 0, -1, (0, 1000), "Wall")  # правая стена
    wall_collision_type = 1  # 0 - остановиться, 1 - абсолютно упруго удариться (масса стены стремится к бесконечности)

    # Конструктор
    def __init__(self, size, collision_type):
        self.size_x = size[0]
        self.size_y = size[1]
        self.collision_type = collision_type

    # Проверяем все объекты на столкновения
    """def check_collisions(self):
        result = False
        sorted(self.object_list, key=lambda obj: obj.current_position)  # сортируем объекты по их координатам по оси Х
        for i in range(1, len(self.object_list)):  # проверяем все объекты на столкновение
            if self.object_list[i - 1].current_position + self.object_list[i - 1].size_x == self.object_list[i].current_position:  # если находим
                result = True
                self.object_list[i - 1].collision(self.object_list[i], self.collision_type)  # совершаем столкновение
        if not result:  # если еще не было столкновения ни с кем
            if len(self.object_list) > 1:
                # Проверяем столкновение первого объекта с левой и правой стеной
                if self.object_list[0].current_position in [self.wall_left.current_position, (self.wall_right.current_position - self.object_list[0].size_x)]:
                    self.object_list[0].collision(self.object_list[0], 3)
                # Проверяем столкновение последнего объекта с левой и правой стеной
                if self.object_list[len(self.object_list) - 1].current_position in [self.wall_left.current_position, (self.wall_right.current_position - self.object_list[len(self.object_list) - 1].size_x)]:
                    self.object_list[len(self.object_list) - 1].collision(self.object_list[len(self.object_list) - 1], 3)
            else:
                # Проверяем столкновение объекта с левой и правой стеной
                if self.object_list[0].current_position in [self.wall_left.size_x, self.wall_right.size_x]:
                    self.object_list[0].collision(self.object_list[0], 3)"""

    # Обновляем всю информацию о мире
    def update_world_state(self):
        # self.check_collisions()
        if len(self.object_list) > 1:
            # Проверяем для первого объекта, кто ближе: левая стена или второй объект
            if self.object_list[0].current_position - round(self.wall_left.current_position + self.wall_left.size_x, self.object_list[0].precision) < self.object_list[1].current_position - round(self.object_list[0].current_position + self.object_list[0].size_x, self.object_list[0].precision):
                self.object_list[0].update_position(self.wall_left, self.collision_type)  # если стена ближе
            else:
                self.object_list[0].update_position(self.object_list[1], self.collision_type)  # если второй объект ближе

            # Проверяем для всех объектов со 2 по N-1, кто ближе: i-1 или i+1
            for i in range(1, len(self.object_list) - 1):
                if self.object_list[i].current_position - round(self.object_list[i - 1].current_position + self.object_list[i - 1].size_x, self.object_list[i - 1].precision) < self.object_list[i + 1].current_position - round(self.object_list[i].current_position + self.object_list[i].size_x, self.object_list[i].precision):
                    self.object_list[i].update_position(self.object_list[i - 1], self.collision_type)  # если левый объект ближе
                else:
                    self.object_list[i].update_position(self.object_list[i + 1], self.collision_type)  # если правый объект ближе

            # Проверяем для последнего объекта, кто ближе: предпоследний объект или правая стена
            if self.object_list[len(self.object_list) - 1].current_position - round(self.object_list[len(self.object_list) - 2].current_position + self.object_list[len(self.object_list) - 2].size_x, self.object_list[len(self.object_list) - 2].precision) < self.wall_right.current_position - round(self.object_list[len(self.object_list) - 1].current_position + self.object_list[len(self.object_list) - 1].size_x, self.object_list[len(self.object_list) - 1].precision):
                self.object_list[len(self.object_list) - 1].update_position(self.object_list[len(self.object_list) - 2], self.collision_type)  # если предпоследний объект ближе
            else:
                self.object_list[len(self.object_list) - 1].update_position(self.wall_right, self.collision_type)  # если стена ближе
        else:
            # Проверяем для объекта, кто ближе: левая стена или правая стена
            if self.object_list[0].current_position - round(self.wall_left.current_position + self.wall_left.size_x, self.wall_left.precision) < self.wall_right.size_x - round(self.object_list[0].current_position + self.object_list[0].size_x, self.object_list[0].precision):
                self.object_list[0].update_position(self.wall_left, self.collision_type)  # если левая стена ближе
            else:
                self.object_list[0].update_position(self.wall_right, self.collision_type)  # если правая стена ближе

    # Добавление нового объекта в мир
    def add_object(self, obj):
        self.object_list.append(obj)
