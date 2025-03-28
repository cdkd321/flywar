import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from player import Player
from const import WIDTH, HEIGHT

@pytest.fixture
def player():
    return Player()

def test_player_movement(player):
    # 测试左右边界限制
    player.rect.x = -10
    player.update()
    assert player.rect.x == 0

    player.rect.x = WIDTH + 10
    player.update()
    assert player.rect.right == WIDTH

def test_shoot_bullets(player, mocker):
    # 使用mocker模拟子弹生成
    mock_bullet = mocker.patch('bullet.Bullet')
    player.shoot()
    assert mock_bullet.call_count == 3