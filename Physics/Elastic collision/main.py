import pygame
import time
from physics import Object
from physics import World
from pygame.locals import *

# Объявляем "Мир"
collision_type = 0
world_size = (800, 400)
world = World(world_size, collision_type)  # задаем миру размеры и тип столкновений в нем

# Добавляем в мир объекты
# mass_rate = 3

small_cube_start_position = 100
small_cube_mass = 3
small_cube_start_velocity = 0  # маленький куб стоит на месте
small_cube_image = pygame.image.load('small_cube.png')
small_cube_size = (60, 60)
small_cube = Object(small_cube_start_position,  # создали объект по заданным параметрам
                    small_cube_mass,
                    small_cube_start_velocity,
                    small_cube_image,
                    small_cube_size)
world.add_object(small_cube)

big_cube_start_position = 100 + 100 + small_cube.size_x  # двойное расстояние + размер первого куба для наглядности
big_cube_mass = 15
big_cube_start_velocity = -1  # большой куб двигается по направлению к маленькому
big_cube_image = pygame.image.load('big_cube.png')
big_cube_size = (120, 120)
big_cube = Object(big_cube_start_position,  # создали объект по заданным параметрам
                  big_cube_mass,
                  big_cube_start_velocity,
                  big_cube_image,
                  big_cube_size)
world.add_object(big_cube)

# Подготовка для работы с графикой
pygame.init()
screen = pygame.display.set_mode(world_size)  # окно мира
pygame.display.set_caption("Physics modulation")  # настройка названия окна
running = True  # переменная, определяющая, работает окно мира или его надо закрыть
delay = 25  # потом разберусь какой ставить делей и как он влияет на скорости

# Переменные для графики
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.SysFont('inconsolata', 30)

# Счетчик времени работы программы
working_time = 0
start_time = time.time()

# Цикл обработки событий окна
while running:
    # Заливаем окно белым
    screen.fill(WHITE)

    # Обновляем всю информацию о мире (двигаем объекты и проверяем коллизии)
    world.update_world_state()

    # Добавляем все объекты на экран
    for obj in world.object_list:
        screen.blit(obj.image, (int(obj.current_position), world_size[1] - obj.size_y))

    # Вывод актуальной позиции и скорости, стартовых позиции и скорости, массы и потери энергии
    # Для первого тела
    writable1 = [f"Current position: {small_cube.current_position}", f"Current velocity: {small_cube.current_velocity}", f"System energy loss: {small_cube.energy_loss}"]
    screen.blit(font.render("First truck info", 1, BLACK), (20, 10))
    for i in range(len(writable1)):
        s = writable1[i]
        screen.blit(font.render(s, 1, BLACK), (10, 30 + i * 20))
    # Для второго тела
    writable2 = [f"Current position: {big_cube.current_position}", f"Current velocity: {big_cube.current_velocity}", f"System energy loss: {big_cube.energy_loss}"]
    screen.blit(font.render("Second truck info", 1, BLACK), (320, 10))
    for i in range(len(writable2)):
        s = writable2[i]
        screen.blit(font.render(s, 1, BLACK), (320, 30 + i * 20))
    pygame.display.update()
    pygame.time.delay(delay)

    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            pass
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
