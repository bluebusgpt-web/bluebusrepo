# -*- coding: utf-8 -*-
"""
한 파일 구성 브록깨기(브레이크아웃) 게임
- 패들 폭을 기준값의 3배로 설정
- 벽돌은 화려한 색상으로 랜덤 칠해짐
- 벽돌 파괴 시 아이템(무기)이 등장, 획득 시 Space로 총알 발사 가능
- 한글 폰트 깨짐 방지 시도 (Windows: 맑은 고딕 사용 시도)
실행: Windows PowerShell에서 `python .\breakout_game.py`
(필요시: pip install pygame)
"""

import random
import pygame
from pygame import Rect
from pathlib import Path

# 게임 설정
WIDTH, HEIGHT = 800, 600
FPS = 60

# 패들 기본 폭(기준값)과 3배 확대 적용
BASE_PADDLE_WIDTH = 60
PADDLE_WIDTH = BASE_PADDLE_WIDTH * 3  # 요구사항: 지금의 3배
PADDLE_HEIGHT = 16
PADDLE_Y_OFFSET = 40
PADDLE_SPEED = 8

BALL_RADIUS = 8
BALL_SPEED = 5

BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_MARGIN = 4
TOP_OFFSET = 60

# 아이템 속성
ITEM_SIZE = 18
ITEM_FALL_SPEED = 3
ITEM_SPAWN_CHANCE = 1.0  # 1.0이면 무조건 스폰, 필요하면 낮출 것

# 총알
BULLET_WIDTH = 4
BULLET_HEIGHT = 12
BULLET_SPEED = 10
BULLET_COOLDOWN = 250  # ms

# 화려한 색상 팔레트
COLOR_PALETTE = [
    (255, 73, 88),   # red pink
    (255, 184, 108), # orange
    (255, 241, 118), # yellow
    (119, 221, 119), # light green
    (115, 204, 255), # sky
    (174, 133, 255), # purple
    (255, 121, 198), # magenta
    (255, 166, 0),   # amber
    (0, 199, 140),   # teal
    (0, 168, 255),   # bright blue
]

def get_font(size):
    # 한글 깨짐 방지: Windows의 맑은 고딕 우선 사용 시도
    try:
        pygame.font.init()
        for name in ["맑은 고딕", "Malgun Gothic", "malgungothic", "MalgunGothic"]:
            f = pygame.font.match_font(name)
            if f:
                return pygame.font.Font(f, size)
    except Exception:
        pass
    return pygame.font.SysFont(None, size)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = BALL_RADIUS
        self.vx = random.choice([-1, 1]) * BALL_SPEED
        self.vy = -BALL_SPEED

    def rect(self):
        return Rect(int(self.x - self.r), int(self.y - self.r), self.r*2, self.r*2)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        # 벽 충돌
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx = -self.vx
        if self.x + self.r >= WIDTH:
            self.x = WIDTH - self.r
            self.vx = -self.vx
        if self.y - self.r <= 0:
            self.y = self.r
            self.vy = -self.vy

    def draw(self, s):
        pygame.draw.circle(s, (255,255,255), (int(self.x), int(self.y)), self.r)

class Paddle:
    def __init__(self):
        self.w = PADDLE_WIDTH
        self.h = PADDLE_HEIGHT
        self.x = WIDTH // 2 - self.w // 2
        self.y = HEIGHT - PADDLE_Y_OFFSET
        self.speed = PADDLE_SPEED

    def rect(self):
        return Rect(self.x, self.y, self.w, self.h)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        # 화면 밖으로 나가지 않게
        self.x = max(0, min(WIDTH - self.w, self.x))

    def draw(self, s):
        pygame.draw.rect(s, (200,200,200), self.rect(), border_radius=6)

class Brick:
    def __init__(self, x, y, w, h, color):
        self.rect = Rect(x, y, w, h)
        self.color = color

    def draw(self, s):
        pygame.draw.rect(s, self.color, self.rect)
        pygame.draw.rect(s, (30,30,30), self.rect, 2)  # 테두리

class Item:
    def __init__(self, x, y, kind="gun"):
        self.x = x
        self.y = y
        self.size = ITEM_SIZE
        self.kind = kind
        self.vy = ITEM_FALL_SPEED
        self.rect = Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
        self.color = (255, 215, 0) if kind == "gun" else (200,200,200)

    def update(self):
        self.y += self.vy
        self.rect.topleft = (int(self.x - self.size//2), int(self.y - self.size//2))

    def draw(self, s):
        pygame.draw.rect(s, self.color, self.rect, border_radius=4)
        # gun 아이콘 간단 표시
        if self.kind == "gun":
            mid = self.rect.center
            pygame.draw.line(s, (30,30,30), (mid[0]-4, mid[1]), (mid[0]+6, mid[1]), 3)

class Bullet:
    def __init__(self, x, y):
        self.rect = Rect(x - BULLET_WIDTH//2, y - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)

    def update(self):
        self.rect.y -= BULLET_SPEED

    def draw(self, s):
        pygame.draw.rect(s, (255, 60, 60), self.rect)

def create_bricks():
    bricks = []
    total_margin = (BRICK_COLS+1) * BRICK_MARGIN
    brick_w = (WIDTH - total_margin) // BRICK_COLS
    brick_h = 20
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = BRICK_MARGIN + col * (brick_w + BRICK_MARGIN)
            y = TOP_OFFSET + row * (brick_h + BRICK_MARGIN)
            color = random.choice(COLOR_PALETTE)
            bricks.append(Brick(x, y, brick_w, brick_h, color))
    return bricks

def rect_circle_collision(rect: Rect, cx, cy, r):
    # 간단한 원-사각형 충돌 검사
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))
    dx = cx - closest_x
    dy = cy - closest_y
    return (dx*dx + dy*dy) <= r*r

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("블럭깨기 (한글 폰트 지원)")
    clock = pygame.time.Clock()

    font = get_font(18)
    big_font = get_font(32)

    paddle = Paddle()
    ball = Ball(WIDTH//2, HEIGHT - PADDLE_Y_OFFSET - 30)
    bricks = create_bricks()
    items = []
    bullets = []
    gun_enabled = False
    last_shot = 0

    lives = 3
    score = 0
    running = True

    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        paddle.update(keys)

        # 총알 발사
        if gun_enabled and keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - last_shot >= BULLET_COOLDOWN:
                bx = paddle.x + paddle.w // 2
                by = paddle.y
                bullets.append(Bullet(bx, by))
                last_shot = now

        ball.update()

        # 공과 패들 충돌
        if rect_circle_collision(paddle.rect(), ball.x, ball.y, ball.r) and ball.vy > 0:
            ball.vy = -abs(ball.vy)
            # 공 속도 x 성분은 패들에서의 충돌 위치에 따라 변화
            offset = (ball.x - (paddle.x + paddle.w/2)) / (paddle.w/2)
            ball.vx = BALL_SPEED * offset * 1.8

        # 공이 바닥에 떨어지면
        if ball.y - ball.r > HEIGHT:
            lives -= 1
            if lives <= 0:
                # 게임 오버
                screen.fill((10,10,10))
                text = big_font.render("게임 오버", True, (255,255,255))
                screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))
                pygame.display.flip()
                pygame.time.wait(1500)
                running = False
                continue
            else:
                # 공 재생성
                ball = Ball(WIDTH//2, HEIGHT - PADDLE_Y_OFFSET - 30)

        # 공과 벽돌 충돌 검사
        hit_brick = None
        for b in bricks:
            if rect_circle_collision(b.rect, ball.x, ball.y, ball.r):
                hit_brick = b
                break
        if hit_brick:
            # 간단 반사: y 방향 반전
            ball.vy = -ball.vy
            # 벽돌 제거, 점수 추가
            bricks.remove(hit_brick)
            score += 100
            # 아이템 스폰 (설정된 확률로)
            if random.random() <= ITEM_SPAWN_CHANCE:
                items.append(Item(hit_brick.rect.centerx, hit_brick.rect.centery, kind="gun"))

        # 아이템 업데이트 및 수집
        for it in items[:]:
            it.update()
            if it.rect.colliderect(paddle.rect()):
                if it.kind == "gun":
                    gun_enabled = True
                items.remove(it)
            elif it.y - it.size/2 > HEIGHT:
                items.remove(it)

        # 총알 업데이트 및 벽돌과 충돌 처리
        for b in bullets[:]:
            b.update()
            # 화면 밖이면 제거
            if b.rect.bottom < 0:
                bullets.remove(b)
                continue
            for br in bricks[:]:
                if b.rect.colliderect(br.rect):
                    try:
                        bricks.remove(br)
                    except ValueError:
                        pass
                    if b in bullets:
                        bullets.remove(b)
                    score += 100
                    # 파괴된 벽돌에서 아이템 스폰 가능
                    if random.random() <= 0.25:
                        items.append(Item(br.rect.centerx, br.rect.centery, kind="gun"))
                    break

        # 화면 그리기
        screen.fill((12, 12, 30))
        # 상단 정보
        info_text = f"점수: {score}   목숨: {lives}   총알: {'활성' if gun_enabled else '비활성'} (아이템 획득 시 활성)"
        screen.blit(font.render(info_text, True, (230,230,230)), (10, 10))

        # 벽돌 그리기
        for b in bricks:
            b.draw(screen)

        # 아이템, 총알, 패들, 공 그리기
        for it in items:
            it.draw(screen)
        for blt in bullets:
            blt.draw(screen)
        paddle.draw(screen)
        ball.draw(screen)

        # 남은 벽돌이 없으면 성공
        if not bricks:
            screen.fill((8, 80, 20))
            t = big_font.render("클리어!", True, (255,255,255))
            screen.blit(t, t.get_rect(center=(WIDTH//2, HEIGHT//2)))
            pygame.display.flip()
            pygame.time.wait(1500)
            running = False
            continue

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()