import pygame
from physics import Ladder
from pygame.locals import *


def input_from_file(filename):
    file = open(filename, 'r')

    stick_angle = float(file.readline().split()[1])
    stick_d = float(file.readline().split()[1])
    battery_U = float(file.readline().split()[1])
    battery_I = float(file.readline().split()[1])

    passed_line = file.readline()

    wire_length = float(file.readline().split()[1])
    wire_p = float(file.readline().split()[1])
    wire_S = float(file.readline().split()[1])

    passed_line = file.readline()

    stick_p = float(file.readline().split()[1])
    stick_S = float(file.readline().split()[1])
    ion_y = float(file.readline().split()[1])

    ladder_object = Ladder(stick_angle,
                           stick_d,
                           battery_U,
                           battery_I,
                           wire_length,
                           wire_p,
                           wire_S,
                           stick_p,
                           stick_S,
                           ion_y)

    file.close()
    return ladder_object


def graphics():

    slow = 10  # 20 * 10 ** 6  # замедление времени
    correction_factor = 1.43  # коэффициент, умножение на который даст сильно приближенное к реальному обновление времени в условиях программы, так как расчтеты производятся не мгновенно
    precision = 3  # точность вывода, количество знаков после запятой при выводе (рассчеты все равно проводятся с максимально возможной для Python3 точностью)

    # Объявляем объект лестницы
    ladder = input_from_file('input.txt')

    # Подготовка для работы с графикой
    window_size = (1200, 675)
    pygame.init()
    screen = pygame.display.set_mode(window_size)  # окно мира
    pygame.display.set_caption("Смоделированная установка \"лестницы Иакова\"")  # настройка названия окна
    running = True  # переменная, определяющая, работает окно мира или его надо закрыть
    delay = 25  # задержка между обновлениями состояния установки, "единица" времени, в милисекундах
    world_bg_img = pygame.image.load('src/background.png')  # картинка заднего фона мира
    started = False
    start_img = pygame.image.load('src/start_btn.png')

    # Переменные для графики
    BLACK = (0, 0, 0)
    font = pygame.font.SysFont('inconsolata', 30)

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
        screen.blit(font.render(f"t = {round(t, precision)} c", 1, BLACK), (55, 225))

        if started:
            # Добавляем на экран дугу (или не добавляем)
            # screen.blit(particle.image, (int(particle.current_position[0]), int(particle.current_position[1])))

            # Добавляем информацию о ней
            writable = ladder.get_info()
            for i in range(len(writable)):
                screen.blit(font.render(writable[i], 1, BLACK), (55, 250 + i * 25))

            # Обновляем ее состояние
            ladder.make_regular_calculations(t)
            pygame.display.update()
            pygame.time.delay(delay)

            # Увеличиваем время
            # t += 1
            t += (delay / 1000) * correction_factor / slow  # синхронизируемся с реальным временем
        else:
            screen.blit(start_img, (100, 360))


if __name__ == '__main__':
    graphics()
