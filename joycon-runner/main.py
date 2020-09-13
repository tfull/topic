import pygame
import pygame.locals
import time


# 定数
class Constant:
    max_x = 8.0
    min_x = -8.0
    max_y = 9.0
    min_y = 0.0
    width = 640
    height = 360
    frequency = 30


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
        self.y = 3.6
        self.ax = 0
        self.ay = -9.8 / 2
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.last_update = time.time()

    def move(self, command):
        if command["type"] == "jump":
            if self.on_ground:
                self.vy += 5
                self.on_ground = False
        elif command["type"] == "run":
            self.vx = command["x"]
            if self.on_ground:
                self.vy = command["y"]

    def update(self, blocks):
        big = 1000000
        now = time.time()
        dt = now - self.last_update
        self.vx += self.ax * dt
        self.vy += self.ay * dt

        self.on_ground = False

        # 衝突を無視した場合の座標
        nx = self.x + self.vx * dt
        ny = self.y + self.vy * dt

        # 物体との衝突判定
        for block in blocks:
            # ブロックの中心座標
            bx = block.x + block.width / 2
            by = block.y - block.height / 2

            # 衝突判定用
            c_w = (self.width + block.width) / 2
            c_h = (self.height + block.height) / 2

            # x の衝突判定
            collision_x = abs(bx - nx) < c_w
            # y の衝突判定
            collision_y = abs(by - ny) < c_h

            # 衝突している場合
            if collision_x and collision_y:
                # 4箇所の中で衝突しているかつめり込みが少ない箇所を探す
                # 横方向の衝突
                if collision_x:
                    # 人間のほうが右
                    if nx >= bx:
                        c_left = c_w - (nx - bx)
                        c_right = big
                    # 人間のほうが左
                    else:
                        c_left = big
                        c_right = c_w - (bx - nx)
                else:
                    c_left = big
                    c_right = big

                # 縦方向の衝突
                if collision_y:
                    # 人間のほうが上
                    if ny >= by:
                        c_top = big
                        c_bottom = c_h - (ny - by)
                    # 人間のほうが下
                    else:
                        c_top = c_h - (by - ny)
                        c_bottom = big
                else:
                    c_top = big
                    c_bottom = big

                # 一番小さい箇所を探す
                c_direction = "left"
                c_scale = c_left
                if c_right < c_scale:
                    c_direction = "right"
                    c_scale = c_right
                if c_top < c_scale:
                    c_direction = "top"
                    c_scale = c_top
                if c_bottom < c_scale:
                    c_direction = "bottom"

                # 一番小さい衝突部分を補正
                # 衝突しているためどこかは引っかかる
                if c_direction == "left":
                    nx = bx + c_w
                    self.vx = 0
                elif c_direction == "right":
                    nx = bx - c_w
                    self.vx = 0
                elif c_direction == "top":
                    ny = by - c_h
                    self.vy = 0
                else:
                    ny = by + c_h
                    self.vy = 0
                    # 着地フラグを付ける
                    self.on_ground = True

        # 位置の決定
        self.x = nx
        self.y = ny

        # 更新
        self.last_update = now

    def draw(self, screen):
        cx = self.x - self.width / 2
        cy = self.y + self.height / 2
        px, py = pr(cx, cy)
        width = self.width / (Constant.max_x - Constant.min_x) * Constant.width
        height = self.height / (Constant.max_y - Constant.min_y) * Constant.height
        rect = pygame.locals.Rect(px, py, int(width), int(height))
        pygame.draw.rect(screen, Color.blue, rect, 3)


# 足場と壁
class Block:
    # x, y: 左上の座標
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        px, py = pr(self.x, self.y)
        width = self.width / (Constant.max_x - Constant.min_x) * Constant.width
        height = self.height / (Constant.max_y - Constant.min_y) * Constant.height
        rect = pygame.locals.Rect(px, py, int(width), int(height))
        pygame.draw.rect(screen, Color.yellow, rect, 3)


# 座標マッピング
def pr(x, y):
    min_x = Constant.min_x
    max_x = Constant.max_x
    min_y = Constant.min_y
    max_y = Constant.max_y

    # xy 座標からピクセル位置 (px,py) への変換
    # x 座標
    # - 右方向に正
    # - min_x <= x <= max_x
    # y 座標
    # - 上方向に正
    # - min_y <= y <= max_y
    # px ピクセル
    # - 右方向に正
    # - 0 <= px <= width
    # py ピクセル
    # - 下方向に正
    # - 0 <= py <= height
    px = (x - min_x) / (max_x - min_x) * Constant.width
    py = (max_y - y) / (max_y - min_y) * Constant.height

    return (int(px), int(py))


# メイン処理
def main():
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # 物体の生成
    blocks = [
        Block(-10, 0.5, 20, 1),
        Block(2, 3, 1, 1)
    ]
    human = Human()

    # 初期化
    pygame.init()

    # 画面設定
    pygame.display.set_mode((Constant.width, Constant.height), 0, 32)
    screen = pygame.display.get_surface()
    pygame.display.set_caption("Runner")

    # フレームレート調整用
    clock = pygame.time.Clock()

    count = 0

    while True:
        count += 1

        ### 操作
        for e in pygame.event.get():
            # バツボタンで閉じる
            if e.type == pygame.locals.QUIT:
                pygame.quit()
                return
            elif e.type == pygame.locals.JOYHATMOTION:
                x, y = joystick.get_hat(0)
                human.move({ "type": "run", "x": x, "y": y })
            elif e.type == pygame.locals.JOYBUTTONDOWN:
                if e.button in range(4):
                    human.move({ "type": "jump" })

        ### 動作
        human.update(blocks)

        ### 描画
        # 背景
        screen.fill(Color.black)

        # 足場と壁
        for block in blocks:
            block.draw(screen)

        # 人間
        human.draw(screen)

        # 描画処理
        pygame.display.update()

        ### フレームレート調整
        clock.tick(Constant.frequency)


if __name__ == '__main__':
    main()
