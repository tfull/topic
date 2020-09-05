import pygame
from pygame.locals import *
import time


# 定数
class Constant:
    max_x = 8.0
    min_x = -8.0
    max_y = 9.0
    min_y = 0.0
    width = 640
    height = 360


# 色
class Color:
    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    yellow = (255, 255, 0)


# 操作キャラ
class Human:
    def __init__(self):
        self.width = 0.6
        self.height = 1.0
        self.x = 0
        self.y = 1.6
        self.ax = 0
        self.ay = 0
        self.vx = 0
        self.vy = 0
        self.last_update = time.time()

    def update(self):
        now = time.time()
        dt = now - self.last_update
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.last_update = now


    def draw(self, screen):
        cx = self.x - self.width / 2
        cy = self.y + self.height / 2
        px, py = pr(cx, cy)
        width = self.width / (Constant.max_x - Constant.min_x) * Constant.width
        height = self.height / (Constant.max_y - Constant.min_y) * Constant.height
        rect = Rect(px, py, int(width), int(height))
        pygame.draw.rect(screen, Color.blue, rect, 3)


# 足場と壁
class Block:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        px, py = pr(self.x, self.y)
        width = self.width / (Constant.max_x - Constant.min_x) * Constant.width
        height = self.height / (Constant.max_y - Constant.min_y) * Constant.height
        rect = Rect(px, py, int(width), int(height))
        pygame.draw.rect(screen, Color.yellow, rect, 3)


# 座標マッピング
def pr(x, y):
    min_x = Constant.min_x
    max_x = Constant.max_x
    min_y = Constant.min_y
    max_y = Constant.max_y

    px = (x - min_x) / (max_x - min_x) * Constant.width
    py = (max_y - y) / (max_y - min_y) * Constant.height

    return (int(px), int(py))


# メイン処理
def main():
    blocks = [
        Block(-10, 0.5, 20, 1),
        Block(2, 3, 1, 1)
    ]
    human = Human()
    # pygame.joystick.init()
    # joystick = pygame.joystick.Joystick(0)
    # joystick.init()

    pygame.init()


    pygame.display.set_mode((Constant.width, Constant.height), 0, 32)
    screen = pygame.display.get_surface()
    pygame.display.set_caption("Runner")

    while True:
        screen.fill(Color.black)

        for block in blocks:
            block.draw(screen)

        human.draw(screen)

        pygame.display.update()
        pygame.time.wait(10)

        for e in pygame.event.get():
            if e.type == QUIT:
                return



if __name__ == '__main__':
    main()
