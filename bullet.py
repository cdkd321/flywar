import pygame

from const import WIDTH, BLACK, WHITE

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=0):
        super().__init__()
        # 增大子弹尺寸
        self.image = pygame.Surface((20, 30), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # 填充透明背景
        # 绘制更大的月亮形状子弹
        pygame.draw.circle(self.image, WHITE + (255,), (10, 14), 10)
        pygame.draw.circle(self.image, BLACK + (255,), (14, 14), 8)
        self.original_image = self.image  # 保存原始图像用于旋转
        self.angle = 0  # 旋转角度
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.speedx = direction * 2
    
    def update(self):
        # 更新位置
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        
        # 旋转子弹
        self.angle += 5  # 每帧旋转5度
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        # 保持子弹中心位置不变
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        # 检查是否超出屏幕
        if self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()