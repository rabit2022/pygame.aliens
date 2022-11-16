import random

import pygame
from pygame.sprite import Sprite

'''
Bullet类继承了我们从模块pygame.sprite中导入的Sprite类。
通过使用精灵，可将游戏中相关的元素编组，进而同时操作编组中的所有元素
'''


class ShipBullet(Sprite):
    # 一个对飞船发射的子弹进行管理的类
    def __init__(self, ai_settings, screen, ship):
        '''
        在飞船所处的位置创建一个子弹对象
        :param ai_settings:
        :param screen:
        :param ship:
        '''
        # super(HeroBullet, self).__init__()     2.7
        super().__init__()  # 3.0
        # 为创建子弹实例，需要向__init__()传递ai_settings、screen和ship实例，还调用了super()来继承Sprite
        self.screen = screen
        
        # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.ship_bullet_width, ai_settings.ship_bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # 存储用小数表示的子弹位置,以便能够微调子弹的速度
        self.y = float(self.rect.y)
        
        # 颜色和速度设置
        self.color = ai_settings.get_random_colour()
        self.speed_factor = ai_settings.ship_bullet_speed
    
    def update(self):
        '''
        向上移动子弹
        :return:
        '''
        # 更新表示子弹位置的小数值
        self.y -= self.speed_factor
        # 更新表示子弹的rect的位置
        self.rect.y = self.y
    
    def draw_bullet(self):
        '''
        # 在屏幕上绘制子弹"""
        :return:
        '''
        pygame.draw.rect(self.screen, self.color, self.rect)


class AlienBullet(Sprite):
    # 一个对飞船发射的子弹进行管理的类
    def __init__(self, ai_settings, screen, alien):
        '''
        在飞船所处的位置创建一个子弹对象
        :param ai_settings:
        :param screen:
        :param alien:
        '''
        super(AlienBullet, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.alien_bullet_width, ai_settings.alien_bullet_height)
        # print(alien.rect.x, alien.rect.y)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.top
        
        # 存储用小数表示的子弹位置,以便能够微调子弹的速度
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        
        # 颜色和速度设置
        self.color = ai_settings.alien_bullet_color
        self.alien_bullet_speed = ai_settings.alien_bullet_speed
        
        # x轴偏离
        self.alien_bullet_deviation = ai_settings.alien_bullet_deviation  # 偏离速度
        self.alien_bullet_deviation_direction = random.random() * self.ai_settings.fleet_direction  # 偏离方向
    
    def update(self):
        '''
        向下移动子弹
        :return:
        '''
        # 更新表示子弹位置的小数值
        self.y += self.alien_bullet_speed
        # 更新表示子弹的rect的位置
        self.rect.y = self.y
        
        self.x += self.alien_bullet_deviation * self.alien_bullet_deviation_direction
        # print(self.alien_bullet_deviation * self.alien_bullet_deviation_direction)
        self.rect.x = self.x
        
        # self.rect.x += self.x_speed
        # self.rect.y += self.y_speed
        if self.rect.x > self.ai_settings.screen_width - self.rect.width or self.rect.x < 0:
            # self.x_speed = -self.x_speed
            self.alien_bullet_deviation_direction = -self.alien_bullet_deviation_direction
        # if self.rect.y > self.settings.screen_height - self.rect.height or self.rect.y < -50:
        #     # self.y_speed = -self.y_speed
        #     self.alien_bullet_speed = -self.alien_bullet_speed
    
    def draw_bullet(self):
        '''
        # 在屏幕上绘制子弹"""
        :return:
        '''
        pygame.draw.rect(self.screen, self.color, self.rect)


class OppositeShipBullet(Sprite):
    # 一个对飞船发射的子弹进行管理的类
    def __init__(self, ai_settings, screen, ship):
        '''
        在飞船所处的位置创建一个子弹对象
        :param ai_settings:
        :param screen:
        :param ship:
        '''
        # super(HeroBullet, self).__init__()     2.7
        super().__init__()  # 3.0
        # 为创建子弹实例，需要向__init__()传递ai_settings、screen和ship实例，还调用了super()来继承Sprite
        self.screen = screen
        
        # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.ship_bullet_width, ai_settings.ship_bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # 存储用小数表示的子弹位置,以便能够微调子弹的速度
        self.y = float(self.rect.y)
        
        # 颜色和速度设置
        self.color = ai_settings.ship_bullet_color
        self.speed_factor = ai_settings.ship_bullet_speed
    
    def update(self):
        '''
        向上移动子弹
        :return:
        '''
        # 更新表示子弹位置的小数值
        self.y += self.speed_factor
        # 更新表示子弹的rect的位置
        self.rect.y = self.y
    
    def draw_bullet(self):
        '''
        # 在屏幕上绘制子弹"""
        :return:
        '''
        pygame.draw.rect(self.screen, self.color, self.rect)
