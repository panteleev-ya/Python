import pygame
import sys
from pygame.locals import *

# Выбирете свою ОС
# Windows - 'img\\', Linux - 'img//'
os = 'img//'

# Объявление дисплея
pygame.init()
size = (860, 740)
display = pygame.display.set_mode(size)
pygame.display.set_caption('Calculator')

# Объявления объектов, добавляемых на дисплей
bg = (pygame.image.load('{}bg.png'.format(os)), (0, 0))
top = (pygame.image.load('{}top.png'.format(os)), (0, 0))
digits = ['1', '2', '3', 'multiply', 'plus',
          '4', '5', '6', 'divide', 'minus',
          '7', '8', '9', 'st', 'equal',
          '0', 'c', 'sqrt', 'dot']
digCoords = [(42, 219), (202, 219), (362, 219), (522, 219), (682, 219),
             (42, 359), (202, 359), (362, 359), (522, 359), (682, 359),
             (42, 499), (202, 499), (362, 499), (522, 499), (682, 499),
             (42, 639), (362, 639), (522, 639), (682, 639)]
ends = [(140, 120), (140, 120), (140, 120), (140, 120), (140, 120),
        (140, 120), (140, 120), (140, 120), (140, 120), (140, 120),
        (140, 120), (140, 120), (140, 120), (140, 120), (140, 120),
        (300, 80), (140, 80), (140, 80), (140, 80)]
chars = ['1', '2', '3', '*', '+',
         '4', '5', '6', '/', '-',
         '7', '8', '9', '**', '=',
         '0', 'c', '**(0.5)', '.']

# Добавление объектов на дисплей
display.blit(bg[0], bg[1])
for i in range(len(digits)):
    image = (pygame.image.load('{}.png'.format(os+digits[i])), digCoords[i])
    display.blit(image[0], image[1])
pygame.display.update()

# Объявление переменных
stroka = ''


# Объявление функции обновления итоговой строки
def CheckForPress(x, y):
    global display, digCoords, ends, chars
    for i in range(len(digCoords)):
        x1 = digCoords[i][0]
        x2 = x1 + ends[i][0]
        y1 = digCoords[i][1]
        y2 = y1 + ends[i][1]
        if x1 <= x <= x2 and y1 <= y <= y2:
            return chars[i]
    return 'None'


# Главный цикл программы
while True:
    l = len(stroka)
    ss = min(75, int(1.8*700//(l+1)))
    shrift = pygame.font.Font('freesansbold.ttf', ss)
    display.blit(top[0], top[1])
    display.blit(shrift.render(stroka, True, (80, 255, 80)), (30, 100-(ss//2)))
    for e in pygame.event.get():
        if e.type == MOUSEBUTTONUP:
            new = CheckForPress(e.pos[0], e.pos[1])
            if new == '=':
                try:
                    stroka = str(eval(stroka))+'~'
                except:
                    stroka += ' ?'
            elif new == 'c':
                if l > 0:
                    if stroka[l-1] != '~':
                        stroka = stroka[:-1]
                    else:
                        stroka = ''
                else:
                    stroka = ''
            elif new != 'None':
                stroka += new
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
