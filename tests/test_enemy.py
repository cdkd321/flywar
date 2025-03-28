import pytest

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from enemy import Enemy
from const import ENEMY_TYPES, WIDTH, HEIGHT
import pygame

@pytest.fixture
def enemy():
    pygame.init()
    return Enemy()

def test_enemy_initialization(enemy):
    assert enemy.rect.y < 0
    assert enemy.rect.x in range(0, WIDTH - enemy.rect.width)
    assert enemy.type in ENEMY_TYPES

def test_enemy_movement(enemy):
    initial_y = enemy.rect.y
    enemy.update()
    assert enemy.rect.y == initial_y + enemy.speedy

    # 测试边界回弹
    enemy.rect.x = -10
    enemy.update()
    assert enemy.rect.x == 0

    enemy.rect.x = WIDTH + 10
    enemy.update()
    assert enemy.rect.right == WIDTH

def test_enemy_respawn(enemy):
    # 强制移动到屏幕外触发重生
    enemy.rect.y = HEIGHT + 50
    enemy.update()
    
    assert enemy.rect.y < 0
    assert enemy.rect.x in range(0, WIDTH - enemy.rect.width)
    assert enemy.type in ENEMY_TYPES
    assert enemy.speedy in range(1, 8)