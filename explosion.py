import pygame

from const import BLACK, RED, ORANGE, YELLOW, WHITE

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.frame = 0
        self.images = []
        # 创建不同大小的爆炸圆圈
        for i in range(5):
            radius = size - (i * size//5)
            surf = pygame.Surface((size * 2, size * 2))
            surf.set_colorkey(BLACK)
            colors = [RED, ORANGE, YELLOW, WHITE]
            pygame.draw.circle(surf, colors[i % len(colors)], (size, size), radius)
            self.images.append(surf)
        
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame >= len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center