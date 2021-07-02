import pygame as pg
import time
from random import randint


class Snack:
    posX = None
    posY = None

    def __init__(self, color, size, eaten=True):
        self.color = color
        self.size = size
        self.eaten = eaten

    def place(self, res, posX, posY):
        self.posX = randint(0, res[0] - self.size)
        self.posY = randint(0, res[1] - self.size)
        retry = True
        while retry:
            for i in range(len(posX)-1):
                if (posX[i] - self.size) < self.posX < (posX[i] + self.size) and (posY[i] - self.size) < self.posY < (posY[i] + self.size):
                    self.posX = randint(0, res[0] - self.size)
                    self.posY = randint(0, res[1] - self.size)
                    break
            else:
                retry = False

    def load(self, screen):
        pg.draw.rect(screen, self.color,
                     (self.posX, self.posY, self.size, self.size))


class Player:
    directions = ["UP", "RIGHT", "DOWN", "LEFT"]

    def __init__(self, color, size, velocity, posX, posY, heading="UP"):
        self.color = color
        self.size = size
        self.velocity = velocity
        self.posX = posX
        self.posY = posY
        self.heading = heading

    def load(self, screen):
        for i in range(len(self.posX)):
            pg.draw.rect(screen, self.color,
                         (self.posX[i], self.posY[i], self.size, self.size))

    def moving(self, res):
        if self.heading == "UP":
            del self.posX[0]
            del self.posY[0]
            self.posX.append(self.posX[-1])
            self.posY.append(self.posY[-1] - self.velocity)

        if self.heading == "DOWN":
            del self.posX[0]
            del self.posY[0]
            self.posX.append(self.posX[-1])
            self.posY.append(self.posY[-1] + self.velocity)

        if self.heading == "LEFT":
            del self.posX[0]
            del self.posY[0]
            self.posY.append(self.posY[-1])
            self.posX.append(self.posX[-1] - self.velocity)

        if self.heading == "RIGHT":
            del self.posX[0]
            del self.posY[0]
            self.posY.append(self.posY[-1])
            self.posX.append(self.posX[-1] + self.velocity)

        self.outOfbounds(res)

    def turn(self, dir):
        if dir == "LEFT":
            for i in range(4):
                if self.directions[i] == self.heading:
                    self.heading = self.directions[i - 1]
                    break

        if dir == "RIGHT":
            for i in range(4):
                if self.directions[i] == self.heading:
                    if i + 1 == 4:
                        self.heading = self.directions[0]
                    else:
                        self.heading = self.directions[i + 1]
                    break

    def grow(self):
        if self.heading == "UP":
            self.posY.append(self.posY[-1] - self.velocity)
            self.posX.append(self.posX[-1])

        if self.heading == "DOWN":
            self.posY.append(self.posY[-1] + self.velocity)
            self.posX.append(self.posX[-1])

        if self.heading == "LEFT":
            self.posX.append(self.posX[-1] - self.velocity)
            self.posY.append(self.posY[-1])

        if self.heading == "RIGHT":
            self.posX.append(self.posX[-1] + self.velocity)
            self.posY.append(self.posY[-1])

    def collision(self):
        for i in range(len(self.posX) - 1):
            if self.posX[i] == self.posX[-1] and self.posY[i] == self.posY[-1]:
                return False
        return True

    def outOfbounds(self, res):
        if self.posY[-1] == (0 - self.size):
            self.posY[-1] = (res[1] - self.size)
        if self.posY[-1] == (res[1]):
            self.posY[-1] = 0
        if self.posX[-1] == (0 - self.size):
            self.posX[-1] = (res[0] - self.size)
        if self.posX[-1] == (res[0]):
            self.posX[-1] = 0


pg.init()
res = (400, 600)
bgColor = (0, 20, 0)
pg.display.set_caption("bellaSnake")
screen = pg.display.set_mode(res)
gameClock = pg.time.Clock()
framerate = 12

snake = Player(color=(0, 255, 0), size=10, velocity=10, posX=[
    200, 200, 200, 200, 200, 200, 200, 200], posY=[340, 330, 320, 310, 300, 290, 280, 270], heading="UP")

snack = Snack(color=(255, 0, 0), size=10)

running = True
pTime = time.time()
while running:
    # dt = (time.time() - pTime) * 60
    # pTime = time.time()
    running = snake.collision()

    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
            snake.turn("LEFT")
        if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
            snake.turn("RIGHT")

    screen.fill(bgColor)
    snake.load(screen)
    snake.moving(res)
    if snack.eaten == True:
        snack.place(res, snake.posX, snake.posY)
        snack.eaten = False
    snack.load(screen)
    if (snack.posX - snake.size) <= snake.posX[-1] <= (snack.posX + snake.size) and (snack.posY - snake.size) <= snake.posY[-1] <= (snack.posY + snake.size) and snack.eaten == False:
        snack.eaten = True
        snake.grow()
    pg.display.update()
    gameClock.tick(framerate)
