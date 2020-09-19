import pygame
import pygame.locals
import random
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
    ga = - 9.8 / 1.4
    font = None


# 色
class Color:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    yellow = (255, 255, 0)
    aqua = (0, 255, 255)


# 操作キャラ
class Human:
    vy_jump = 7

    def __init__(self):
        self.width = 0.6
        self.height = 1.0
        self.x = 0
        self.y = 3.6
        self.ax = 0
        self.ay = Constant.ga
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.last_update = time.time()
        self.over = False

    def move(self, command):
        if self.over:
            return

        if command["type"] == "jump":
            if self.on_ground:
                self.vy += Human.vy_jump
        elif command["type"] == "run":
            self.vx = command["x"]

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

    def stop(self):
        self.over = True
        self.vx = 0

    def draw(self, screen):
        cx = self.x - self.width / 2
        cy = self.y + self.height / 2
        px, py = pr(cx, cy)
        width = self.width / (Constant.max_x - Constant.min_x) * Constant.width
        height = self.height / (Constant.max_y - Constant.min_y) * Constant.height
        rect = pygame.locals.Rect(px, py, int(width), int(height))
        color = Color.blue if not self.over else Color.aqua
        pygame.draw.rect(screen, color, rect, 3)


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


# 弾
class Bullet:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.last_update = time.time()

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        px, py = pr(self.x, self.y)
        pygame.draw.circle(screen, Color.white, (px, py), 2)


# 発射台
class Shooter:
    sps = 2

    def __init__(self, x0, y0, x1, y1, vx, vy):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.vx = vx
        self.vy = vy
        self.last_shoot = time.time()

    def shoot(self, bullets):
        t = random.random()
        x = self.x0 + (self.x1 - self.x0) * t
        y = self.y0 + (self.y1 - self.y0) * t
        bullet = Bullet(x, y, self.vx, self.vy)
        bullets.append(bullet)

    def update(self, bullets):
        now = time.time()
        dt = now - self.last_shoot

        if dt > 1 / Shooter.sps:
            self.shoot(bullets)
            self.last_shoot = now


# タイマー
class Watch:
    def __init__(self):
        self.start = time.time()
        self.end = None

    def stop(self):
        if self.end is None:
            self.end = time.time()

    def draw(self, screen):
        if self.end is None:
            score = int(time.time() - self.start)
        else:
            score = int(self.end - self.start)

        text = Constant.font.render(str(score), True, Color.green)
        screen.blit(text, (Constant.width - 50, 0))


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


# 弾が人間に当たったか
def hit(human, bullets):
    x0 = human.x - human.width / 2
    x1 = human.x + human.width / 2
    y0 = human.y - human.height / 2
    y1 = human.y + human.height / 2

    for b in bullets:
        if x0 < b.x < x1 and y0 < b.y < y1:
            return True

    return False


# メイン処理
def main():
    # 初期化
    pygame.init()
    Constant.font = pygame.font.SysFont(None, 50)

    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # 画面設定
    pygame.display.set_mode((Constant.width, Constant.height), 0, 32)
    screen = pygame.display.get_surface()
    pygame.display.set_caption("Runner")

    # フレームレート調整用
    clock = pygame.time.Clock()

    # 時間計測開始
    watch = Watch()

    # 物体の生成
    blocks = [
        Block(-10, 0.5, 20, 1),
        Block(2, 3, 1, 1)
    ]

    human = Human()

    shooters = [
        Shooter(Constant.min_x, Constant.max_y, Constant.max_x, Constant.max_y, 0, -0.1),
        Shooter(Constant.max_x, Constant.max_y, Constant.max_x, Constant.min_y, -0.1, 0)
    ]

    bullets = []

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
        # 人間
        human.update(blocks)
        # 弾
        for bullet in bullets:
            bullet.update()
        # 発射
        for shooter in shooters:
            shooter.update(bullets)

        # 画面外に消えた弾を消す
        bullets = [b for b in bullets if Constant.min_x <= b.x <= Constant.max_x and Constant.min_y <= b.y <= Constant.max_y]

        # ゲームステータス判定
        if hit(human, bullets):
            human.stop()
            watch.stop()

        ### 描画
        # 背景
        screen.fill(Color.black)
        # 足場と壁
        for block in blocks:
            block.draw(screen)
        # 人間
        human.draw(screen)
        # 弾
        for bullet in bullets:
            bullet.draw(screen)
        # 得点
        watch.draw(screen)

        # 描画処理
        pygame.display.update()

        ### フレームレート調整
        clock.tick(Constant.frequency)


if __name__ == '__main__':
    main()
