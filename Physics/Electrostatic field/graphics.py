import pygame
from physics import Object
from pygame.locals import *


def graphics():
    file = open('input.txt', 'r')

    # Зададим масштаб (отношение длины метра к длине пикселя)
    # Зная, сколько пикселей в одном метре - можно переводить скорость из м/с в пиксель/с
    meter_div_by_pixel = 100  # количество пикселей в одном метре
    slow = 6 * 10 ** 6  # замедление времени

    # Объявляем объект частицы
    world_size = [
        [
            int(file.readline().split()[1]),
            int(file.readline().split()[1])
        ],
        [
            int(file.readline().split()[1]),
            int(file.readline().split()[1])
        ]
    ]
    window_size = [
        int(file.readline().split()[1]),
        int(file.readline().split()[1])
    ]
    particle_start_coordinates = [
        int(file.readline().split()[1]),
        int(file.readline().split()[1])
    ]
    particle_mass = float(file.readline().split()[1]) * 10 ** (-30)
    particle_q = float(file.readline().split()[1]) * 10 ** (-19)
    particle_size = [
        int(file.readline().split()[1]),
        int(file.readline().split()[1])
    ]
    particle_start_velocity = [
        float(file.readline().split()[1]) * 10 ** 5,
        float(file.readline().split()[1]) * 10 ** 5
    ]
    particle_image = pygame.image.load('src/particle_-.png')
    if particle_q > 0:
        particle_image = pygame.image.load('src/particle_+.png')
    capacitor_u = float(file.readline().split()[1])
    capacitor_d = float(file.readline().split()[1])
    particle = Object(
        particle_start_coordinates,
        particle_start_velocity,
        particle_mass,
        particle_q,
        particle_size,
        particle_image,
        capacitor_u,
        capacitor_d,
        meter_div_by_pixel
    )
    particle.set_world_size(world_size[0], world_size[1])

    # Подготовка для работы с графикой
    pygame.init()
    screen = pygame.display.set_mode(window_size)  # окно мира
    pygame.display.set_caption("Physics modulation")  # настройка названия окна
    running = True  # переменная, определяющая, работает окно мира или его надо закрыть
    delay = 25  # задержка, в милисекундах
    world_bg_img = pygame.image.load('src/background.png')  # картинка заднего фона мира
    started = False
    start_img = pygame.image.load('src/start_btn.png')

    # Переменные для графики
    BLACK = (0, 0, 0)
    font = pygame.font.SysFont('inconsolata', 30)
    file.close()

    # Переменная времени, в секундах
    t = 0.0

    # Цикл обработки событий окна
    while running:

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                started = True
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()

        # Добавляем задний фон
        screen.blit(world_bg_img, (0, 0))

        if started:
            # Добавляем на экран частицу
            screen.blit(particle.image, (int(particle.current_position[0]), int(particle.current_position[1])))

            # Добавляем информацию о ней
            writable = particle.get_info()
            for i in range(len(writable)):
                screen.blit(font.render(writable[i], 1, BLACK), (810, 80 + i * 25))

            # print(particle.help_timer, t - particle.help_timer)

            # Обновляем ее состояние
            particle.update_position(t)
            pygame.display.update()
            pygame.time.delay(delay)

            # print(particle.help_timer, t - particle.help_timer)

            # Увеличиваем время
            # t += 1
            t += (delay / 1000) * 1.43 / slow  # синхронизируемся с реальным временем
        else:
            screen.blit(start_img, (200, 100))


if __name__ == '__main__':
    graphics()
