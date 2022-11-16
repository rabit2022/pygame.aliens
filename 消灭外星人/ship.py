import pygame
from pygame.sprite import Sprite
import game_functions as gf


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        '''
        初始化飞船并设置其初始位置
        :param ai_settings:
        :param screen:
        '''
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('素材/外星人/airplane.jpg')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)
        
        # 移动标志
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        '''
        根据移动标志调整飞船的位置
        :return:
        '''
        
        # 更新飞船的center值，而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right:  # 限制飞船的活动范围
            self.center += self.ai_settings.ship_speed_factor
        '''
        如果使用一个elif代码块来处理向左移动的情况，右箭头键将始终处于优先地位，
        玩家可能同时按住左右箭头键，飞船将纹丝不动。
        '''
        
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        
        # 根据self.center更新rect对象
        self.rect.centerx = self.center
    
    def blitme(self):
        '''
        在指定位置绘制飞船
        :return:
        '''
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        '''
        让飞船在屏幕上居中
        :return:
        '''
        self.center = self.screen_rect.centerx
    
    