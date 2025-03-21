import pygame

from const import WIDTH, HEIGHT, WHITE

# 玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/player/smart_one.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 8

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        # 发射三个方向的子弹
        from bullet import Bullet
        from game import all_sprites, bullets
        bullet1 = Bullet(self.rect.centerx, self.rect.top, -1)  # 左
        bullet2 = Bullet(self.rect.centerx, self.rect.top, 0)   # 中
        bullet3 = Bullet(self.rect.centerx, self.rect.top, 1)   # 右
        all_sprites.add(bullet1, bullet2, bullet3)
        bullets.add(bullet1, bullet2, bullet3)