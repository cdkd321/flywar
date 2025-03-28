import pygame
import random
import sys
from explosion import Explosion
from player import Player
from enemy import Enemy
from bullet import Bullet
import pygame.mixer

# 初始化 Pygame
pygame.init()

# 设置游戏窗口
WIDTH = 480
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('打飞机游戏')

from const import WIDTH, HEIGHT, BLACK, RED, YELLOW, ORANGE, WHITE, ENEMY_TYPES

# 设置游戏窗口
from const import WIDTH, HEIGHT

# 移除原有的类定义
# 玩家飞机类



# 创建精灵组
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# 创建玩家
player = Player()
all_sprites.add(player)

# 创建敌机
for i in range(8):
    enemy = Enemy()
    enemies.add(enemy)
all_sprites.add(enemies) # 将 enemies 中的所有敌机添加到 all_sprites 中

# 定义关卡数据结构
levels = [
    {
        'enemy_count': 8,
        'enemy_speed': 3,
        'background_speed': 120
    },
    {
        'enemy_count': 12,
        'enemy_speed': 5,
        'background_speed': 180
    },
    {
        'enemy_count': 16,
        'enemy_speed': 7,
        'background_speed': 240
    }
]
current_level = 0

# 定义按钮
button_width = 100
button_height = 50
button_x = WIDTH - button_width - 10
button_y = 10
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# 初始化音频
pygame.mixer.init()

# 定义关卡背景音乐映射
level_music = {
    0: 'mp3/Ghana_Fighter_BGM_60Hz_P02_Moon_Star.mp3',
    1: 'mp3/Ghana_Fighter_BGM_60Hz_p03_Star_of_Fire.mp3',
    2: 'mp3/Ghana_Fighter_BGM_60Hz_p04_Water_Star.mp3'
}

# 游戏主循环
clock = pygame.time.Clock()
running = True

# 播放当前关卡的背景音乐
pygame.mixer.music.load(level_music[current_level])
pygame.mixer.music.play(-1)

# 加载背景图片
background_image = pygame.image.load('images/level1_bg.jpeg')
background_y = 0
background_speed = levels[current_level]['background_speed'] / 60  # 使用关卡配置的背景速度

while running:
    clock.tick(60)
    
    # 事件处理
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE: 
                player.shoot() 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                current_level = (current_level + 1) % len(levels)
                # 重新生成敌机
                for enemy in enemies:
                    enemy.kill()
                for i in range(levels[current_level]['enemy_count']):
                    enemy = Enemy()
                    enemy.speed = levels[current_level]['enemy_speed']
                    all_sprites.add(enemy)
                    enemies.add(enemy)
                    # 切换背景音乐和更新背景速度
                    pygame.mixer.music.load(level_music[current_level])
                    pygame.mixer.music.play(-1)
                    background_speed = levels[current_level]['background_speed'] / 60
    # 更新所有精灵的位置
    all_sprites.update()
    # 子弹击中敌机检测
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        # 创建爆炸效果
        expl = Explosion(hit.rect.center, 30)
        all_sprites.add(expl)
        # 生成新的敌机
        enemy = Enemy()
        enemy.speed = levels[current_level]['enemy_speed']
        all_sprites.add(enemy)
        enemies.add(enemy)
    # 敌机撞到玩家检测
    hits = pygame.sprite.spritecollide(player, enemies, True)
    if hits:
        # 创建大爆炸效果
        expl = Explosion(player.rect.center, 50)
        all_sprites.add(expl)
        running = False
    # 更新背景位置
    background_y += background_speed
    if background_y >= HEIGHT:
        background_y = 0
    
    # 渲染背景
    screen.fill(BLACK)
    screen.blit(background_image, (0, background_y))
    screen.blit(background_image, (0, background_y - HEIGHT))

    # 绘制游戏元素
    all_sprites.draw(screen)
    # pygame.draw.rect(screen, WHITE, button_rect)

    # 双缓冲刷新
    pygame.display.flip()
    
    # 控制帧率
    clock.tick(60)
                
                