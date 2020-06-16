import pygame
from pygame.locals import *
from physics import Ladder
from math import sqrt
from math import tan
from math import pi


def input_from_file(filename):
    file = open(filename, 'r')

    stick_angle = float(file.readline().split()[1])
    stick_d = float(file.readline().split()[1])
    battery_U = float(file.readline().split()[1])

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
                           wire_length,
                           wire_p,
                           wire_S,
                           stick_p,
                           stick_S,
                           ion_y)

    file.close()
    return ladder_object


def calculate_lines(angle, start_pos1, start_pos2, length):
    L = length

    q = (angle * pi / 180) / 2 # pi / 2 - (angle * pi / 180) / 2  # alpha / 2
    tg_q = tan(q)
    delta_x = round(abs(L * tg_q / sqrt(tg_q**2 + 1)))  # a1 + pixel_len * sin(q1)  # (a * tanq2 + a + sqrt(tanq2 * (tanq2 + 1))) / (tanq2 + 1)
    delta_y = round(sqrt(L**2 - delta_x**2))  # b1 + sqrt(pixel_len**2 - (x1 - a1)**2)  # (b * sqrt(tanq2 * (tanq2 + 1)) + tan(q))/sqrt(tanq2 * (tanq2 + 1))

    left_line = [start_pos1[0], start_pos1[1], start_pos1[0] - delta_x, start_pos1[1] - delta_y]
    right_line = [start_pos2[0], start_pos2[1], start_pos2[0] + delta_x, start_pos2[1] - delta_y]

    return left_line, right_line


def graphics():

    slow = 10  # 20 * 10 ** 6  # замедление времени
    correction_factor = 1.43  # коэффициент, умножение на который даст сильно приближенное к реальному обновление времени в условиях программы, так как расчтеты производятся не мгновенно
    precision = 3  # точность вывода, количество знаков после запятой при выводе (рассчеты все равно проводятся с максимально возможной для Python3 точностью)
    start_pos_left = [774, 590]
    start_pos_right = [814, 590]
    meter_div_by_pix = 500  # количество пикселей в одном метре
    # Объявляем объект лестницы
    ladder = input_from_file('input.txt')
    # Делаем стартовые рассчеты
    ladder.make_start_calculations()
    left_line, right_line = calculate_lines(ladder.stick_angle, start_pos_left, start_pos_right, meter_div_by_pix)
    # print(left_line)
    # print(right_line)

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
    PURPLE = (163, 73, 164)
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

        # Добавляем проводники, расположенные под углом stick_angle между ними
        pygame.draw.line(screen, BLACK, [left_line[0], left_line[1]], [left_line[2], left_line[3]], 3)
        pygame.draw.line(screen, BLACK, [right_line[0], right_line[1]], [right_line[2], right_line[3]], 3)

        if started:
            # Добавляем на экран дугу (или не добавляем)
            print("passed:", ladder.stick_passed_length)
            print("h:", ladder.arc_h)
            pygame.draw.line(screen, PURPLE,
                             [round(ladder.arc_start_position[0] - (ladder.delta_X * meter_div_by_pix + 20)),
                              round(ladder.arc_start_position[1] - ladder.arc_h * meter_div_by_pix)
                              ],
                             [round(ladder.arc_start_position[0] + (ladder.delta_X * meter_div_by_pix + 20)),
                              round(ladder.arc_start_position[1] - ladder.arc_h * meter_div_by_pix)
                              ], 2)

            # Добавляем информацию о ней
            # writable = ladder.get_info()
            # for i in range(len(writable)):
            #     screen.blit(font.render(writable[i], 1, BLACK), (55, 250 + i * 25))

            # Обновляем ее состояние
            ladder.make_regular_calculations(t)
            pygame.display.update()
            pygame.time.delay(delay)

            # Увеличиваем время
            t += (delay / 1000) * correction_factor / slow  # синхронизируемся с реальным временем
        else:
            screen.blit(start_img, (80, 360))


if __name__ == '__main__':
    graphics()
