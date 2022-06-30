import objects as objects
import pygame
from random import randint

pygame.init()

width, heigth = 800, 600
FPS = 60
TILE = 32  # размеры танка

window = pygame.display.set_mode((width, heigth))
pygame.display.set_caption('My tanks')
clock = pygame.time.Clock()

#загружаем шрифт
fontUI = pygame.font.Font(None, 30) #30 = размер

imgBrick = pygame.image.load("Tanks/images/block_brick.png")
imgTanks = [
    pygame.image.load("Tanks/images/tank1.png"),
    pygame.image.load("Tanks/images/tank2.png"),
    pygame.image.load("Tanks/images/tank3.png"),
    pygame.image.load("Tanks/images/tank4.png"),
    pygame.image.load("Tanks/images/tank5.png"),
    pygame.image.load("Tanks/images/tank6.png"),
    pygame.image.load("Tanks/images/tank7.png"),
    pygame.image.load("Tanks/images/tank8.png")
    ]
imgBanks = [
    pygame.image.load("Tanks/images/bang1.png"),
    pygame.image.load("Tanks/images/bang2.png"),
    pygame.image.load("Tanks/images/bang3.png")
    ]

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        i = 0  # подсчитывает какого игрока по счету выводить на экран
        for obj in objects:  # перебираем список обьектов и выделяем все обьекты которые имеют значение переменной type равное tank
            if obj.type == 'tank':  # если obj(поле) = tank значит мы нашли на поле игрока
                pygame.draw.rect(window, obj.color,(5 + i * 70, 5, 22, 22))  # (5 - координата прямоугольника, 22 - высота, 22 - ширина

                text = fontUI.render(str(obj.hp ), 1, obj.color)
                rect = text.get_rect(center = (5 + i * 70 + 32, 5 + 11))
                window.blit(text, rect)
                i += 1

# создадим класс для каджого игрока
class Tank:
    def __init__(self, color, px, py, direct, keyList):  # цвет, координаты метоположения, направление, размеры танка
        objects.append(self)  # добавляет ссылку на танк
        self.type = 'tank'    # переменна type, тип tank, чтобы программа могла различать какой это обьект
        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct # направление танка
        self.moveSpeed = 2
        self.hp = 5  # здоровье танка

        self.shotTimer = 0
        self.shotDelay = 60  # задержка между выстрелами
        self.bulletSpeed = 5
        self.bulletDamage = 1

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

        self.rank = 0
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90) # поварачиваем картинку согласно направлению
        self.rect = self.image.get_rect(center = self.rect.center)


    def update(self):
        # трансформируем блок и поворачиваем его согласно картинке
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        # возвращаем обьект и уменьшаем его длинну и высоту на 5
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() -5))
        self.rect = self.image.get_rect(center=self.rect.center)

        # сохраним значение старых позиций танка, до обновления
        # проверим не столкнулся ли с чем то танк, если столкнулся, возвращаем обратно
        oldX, oldY = self.rect.topleft
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2

        for obj in objects:
            # если обьект не равен самому себе, т.е не проверяем себя
            # если не берем для проверки себя и self.rect.colliderect сталкивается с обектом obj
            # значит произошло столкновение с блоком
            # в этом случае вернем нстарые значения нашей позиции (oldX, oldY = self.rect.topleft 41ст)
            if obj != self and obj.type == 'block' and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay  # когда произведен выстрел shottimer принимает состояние задержки

        if self.shotTimer > 0:  # задержка
            self.shotTimer -= 1

    # метод отрисовки
    def draw(self):

        window.blit(self.image, self.rect)
        '''pygame.draw.rect(window, self.color, self.rect)  # рисуем на экране
        x = self.rect.centerx + DIRECTS[self.direct][0] * 30
        y = self.rect.centery + DIRECTS[self.direct][1] * 30
        pygame.draw.line(window, 'white', self.rect.center, (x, y), 4)'''



    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            print(self.color, 'убит')

class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        # механика пули
        self.px += self.dx
        self.py += self.dy

        # удаляем обьекты/пули за пределами экрана
        if self.px < 0 or self.px > width or self.py < 0 or self.py > heigth:
            bullets.remove(self)
        # проверяем столновенеи с другими обьектами
        else:
            for obj in objects:
                if obj != self.parent and obj.type != 'bang' and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)  # когда произошло столновение с обьектом
                    bullets.remove(self)  # удаляем пулю при столновении с обьектом
                    Bang(self.px, self.py)
                    break  # прерываем столновение при попадании в обьект, чтобы исключить двойное попадание

    def draw(self):
        # рисуем пулю
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)

class Bang:
    def __init__(self, px, py): #центр позиции где происходит взрыв
        objects.append(self) #обьект добавляем в список всех оюбектов который используется для отрисовки на экране
        self.type = 'bang'#переменная внутри класса это - поле, чтобы программа понимала что это взрыв

        self.px, self.py = px, py #точка, где происходит взрыв
        self.frame = 0 #поле где содержиться номер кадра

    def update(self):
        self.frame += 0.2
        if self.frame >= 3:
            objects.remove(self)

    def draw(self):
        image = imgBanks[int(self.frame)] #image временная локальная переменная
        rect = image.get_rect(center = (self.px, self.py))
        window.blit(image, rect)

class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        window.blit(imgBrick, self.rect)
        '''pygame.draw.rect(window, 'green', self.rect)
        pygame.draw.rect(window, 'gray20', self.rect, 2)'''

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)

# список для хранения в игре, пули, танки, стены и тд
objects = []
bullets = []
Tank('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Tank('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_0))
ui = UI()

#генератор карты
for _ in range(50):  # создаем боки
    while True:  # делаем чтобы блоки не сталкивались друг с другом(сетка)
        x = randint(0, width // TILE - 1) * TILE  # вычисляем сколько блоков помещается на карте
        y = randint(1, heigth // TILE - 1) * TILE
        rect = pygame.Rect(x, y, TILE, TILE)  # проверяем не сталкивается ли наш обьект с теми что уже в списке обьектов
        fined = False
        for obj in objects:  # проверяем сталкивается ли область rect которая есть на карте
            if rect.colliderect(obj.rect):
                fined = True
        if not fined:
            break
    Block(x, y, TILE)

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    keys = pygame.key.get_pressed()  # поместим в key результат команды

    for obj in objects:  # переберем все обьекты в списке obj и у каждого обьекта вызывать метод update
        obj.update()
    for bullet in bullets:
        bullet.update()
    ui.update()

    window.fill('black')  # закрасим экран в черный цвет

    for obj in objects:  # переберем все обьекты в списке obj и у каждого обьекта вызывать метод draw
        obj.draw()
    for bullet in bullets:
        bullet.draw()
    ui.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
