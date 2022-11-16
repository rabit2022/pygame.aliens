import pygame
from pygame.sprite import Group

import game_functions as gf  # game_functions指定了别名gf
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
from alien import Alien

def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    
    # tittle
    pygame.display.set_caption("消灭外星人重置版")
    
    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    
    # 创建存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    # 添加背景
    background = pygame.image.load('素材/背景/迷雾.jpg')
    # 添加背景音乐
    ai_settings.music()
    
    # 创建一群外星人
    # alien_group = Alien(settings, screen)
    
    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建一个用于存储子弹的编组
    bullets = Group()
    # 创建一个外星人编组
    alien_group = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, alien_group)
    
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, alien_group, bullets)
        if stats.ship_exist:  # 仅在游戏处于活动状态时才运行
            # 根据移动标志调整飞船的位置
            ship.update()
            # 更新子弹
            gf.update_bullets(ai_settings, screen, stats, sb, ship, alien_group, bullets)
            
            # 更新外星人
            gf.update_aliens(ai_settings, screen, stats, sb, ship, alien_group, bullets)
        
        # 更新屏幕上的图像，并切换到新屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, background, alien_group, bullets, play_button)
        
        # 屏幕刷新率
        ai_settings.clock.tick(ai_settings.fps)


if __name__ == '__main__':
    run_game()
