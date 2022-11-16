import pygame
from pygame.sprite import Group

from alien import Alien
from button import Button
from correction_system import Correct
from event import Event
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


class Game(object):
    def __init__(self):
        # 初始化游戏并创建一个屏幕对象
        pygame.init()
        
        self.ai_settings = Settings()
        self.screen = pygame.display.set_mode((self.ai_settings.screen_width, self.ai_settings.screen_height))
        
        # tittle
        pygame.display.set_caption(self.ai_settings.caption)
        
        # # 设置图标
        surface = pygame.image.load(self.ai_settings.icon)
        pygame.display.set_icon(surface)
        
        # 创建一个用于存储子弹的编组
        self.ship_bullet_group = Group()
        self.alien_bullet_group = Group()
        # 创建一个外星人编组
        self.alien_group = Group()
        
        # 创建Play按钮
        self.play_button = Button(self.ai_settings, self.screen, self.ai_settings.play_button)
        
        # 创建存储游戏统计信息的实例，并创建记分牌
        self.stats = GameStats(self.ai_settings)
        self.score_board = Scoreboard(self.ai_settings, self.screen, self.stats, self.alien_group,
                                      self.ship_bullet_group, self.alien_bullet_group)
        
        # 添加背景
        self.background = pygame.image.load(self.ai_settings.background_path)
        
        # 赏惩系统
        self.correct = Correct(self.ai_settings, self.stats, self.score_board, self.ship_bullet_group,
                               self.alien_bullet_group)
        # 创建一艘飞船
        self.ship = Ship(self.ai_settings, self.screen, self.stats, self.score_board, self.alien_group,
                         self.ship_bullet_group, self.alien_bullet_group, self.correct)
        # 创建一群外星人
        self.aliens = Alien(self.ai_settings, self.screen, self.stats, self.score_board, self.ship, self.alien_group,
                            self.alien_bullet_group, self.correct)
        
        # 键盘事件
        self.events = Event(self.ai_settings, self.screen, self.stats, self.score_board, self.play_button, self.ship,
                            self.aliens)
        # 添加背景音乐
        self.ai_settings.music()
        # 创建外星人群
        self.aliens.create_fleet()
    
    def game_running(self):
        while not self.ai_settings.game_over:
            # 监视键盘和鼠标事件
            self.events.check_events()
            if not self.ai_settings.pause:  # 暂停
                if self.stats.ship_exist:  # 仅在游戏处于活动状态时才运行
                    # 根据移动标志调整飞船的位置
                    self.ship.update()
                    # 更新子弹
                    self.ship.update_bullets()
                    
                    # 更新外星人
                    self.aliens.update_aliens()
                    self.aliens.fire_bullet()
                    self.aliens.update_bullets()
                # 更新屏幕上的图像，并切换到新屏幕
                self.update_screen()
                
                # 屏幕刷新率
                self.ai_settings.clock.tick(self.ai_settings.FPS)
    
    def update_screen(self):
        '''
        更新屏幕上的图像，并切换到新屏幕
        :return:
        '''
        # # 每次循环时都重绘屏幕
        self.screen.fill(self.ai_settings.background_color)
        # 加载背景
        self.screen.blit(self.background, (0, 0))
        
        # 在飞船和外星人后面重绘所有子弹
        for bullet in self.ship_bullet_group.sprites():
            bullet.draw_bullet()
            # time.sleep(0.5)
        for bullet in self.alien_bullet_group.sprites():
            bullet.draw_bullet()
        
        # 绘制飞船
        self.ship.blitme()
        # 绘制外星人
        self.alien_group.draw(self.screen)
        # 显示得分
        self.score_board.show_score()
        
        # 如果游戏处于非活动状态，就绘制Play按钮
        if not self.stats.ship_exist:
            self.play_button.draw_button()
        
        # 让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.game_running()
