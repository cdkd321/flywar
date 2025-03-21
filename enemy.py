import pygame
import random

from const import WIDTH, HEIGHT, BLACK, RED, YELLOW, ORANGE, WHITE, ENEMY_TYPES

# 敌机类
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.type = random.choice(ENEMY_TYPES)
        self._draw_enemy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = 0

    def _draw_enemy(self):
        if self.type == 'owl':
            # 画猫头鹰
            pygame.draw.circle(self.image, ORANGE, (20, 20), 15)  # 脸
            pygame.draw.circle(self.image, WHITE, (12, 15), 6)    # 左眼
            pygame.draw.circle(self.image, WHITE, (28, 15), 6)    # 右眼
            pygame.draw.circle(self.image, BLACK, (12, 15), 3)    # 左眼珠
            pygame.draw.circle(self.image, BLACK, (28, 15), 3)    # 右眼珠
            pygame.draw.polygon(self.image, ORANGE, [(15,5), (20,0), (25,5)])  # 耳朵
        elif self.type == 'dog':
            # 画小狗
            pygame.draw.circle(self.image, RED, (20, 20), 15)     # 脸
            pygame.draw.circle(self.image, BLACK, (15, 15), 3)    # 左眼
            pygame.draw.circle(self.image, BLACK, (25, 15), 3)    # 右眼
            pygame.draw.ellipse(self.image, BLACK, (15, 22, 10, 6))  # 嘴巴
            pygame.draw.ellipse(self.image, RED, (5, 5, 12, 20))   # 左耳
            pygame.draw.ellipse(self.image, RED, (23, 5, 12, 20))  # 右耳
        else:  # cat
            # 画小猫
            pygame.draw.circle(self.image, YELLOW, (20, 20), 15)   # 脸
            pygame.draw.polygon(self.image, YELLOW, [(10,5), (20,15), (30,5)])  # 耳朵
            pygame.draw.circle(self.image, BLACK, (15, 15), 2)     # 左眼
            pygame.draw.circle(self.image, BLACK, (25, 15), 2)     # 右眼
            pygame.draw.polygon(self.image, BLACK, [(20,20), (17,25), (23,25)])  # 鼻子
            pygame.draw.line(self.image, BLACK, (17,25), (10,23), 2)  # 左胡须
            pygame.draw.line(self.image, BLACK, (23,25), (30,23), 2)  # 右胡须

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.type = random.choice(ENEMY_TYPES)
            self._draw_enemy()
        # 以下可添加敌机移动逻辑，示例：左右移动
        if random.random() < 0.01:  # 1%的概率改变水平方向
            self.speedx = random.randrange(-3, 4)
        self.rect.x += self.speedx
        # 确保敌机不会移出屏幕
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH