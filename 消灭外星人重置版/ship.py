import time

import pygame
from pygame.sprite import Sprite

from alien import Alien
from animation_realize import Animation
from bullet import ShipBullet, OppositeShipBullet


class Ship(Sprite):
    def __init__(self, ai_settings, screen, stats, score_board, alien_group, ship_bullet_group,
                 alien_bullet_group, correct):
        '''
        初始化飞船并设置其初始位置
        :param ai_settings:
        :param screen:
        '''
        super(Ship, self).__init__()
        self.alien_bullet_group = alien_bullet_group
        self.ship_bullet_group = ship_bullet_group
        self.alien_group = alien_group
        self.score_board = score_board
        self.stats = stats
        self.screen = screen
        self.ai_settings = ai_settings
        
        # 加载飞船图像并获取其外接矩形
        # self.image = pygame.image.load(self.settings.ship_path)
        self.animation = Animation()
        self.images = self.animation.get_images(self.ai_settings.ship_path, rows=4, columns=4)
        self.image = self.images[0]
        
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # self.rect.centery = self.screen_rect.centery
        # 在飞船的属性center中存储小数值
        self.centerx = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)
        
        # 移动标志
        self.direction = 'down'
        self.correct = correct
    
    def update(self):
        '''
        根据移动标志调整飞船的位置
        :return:
        '''
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] and self.rect.left > 0:
            self.direction = 'left'
            self.image = self.animation.get_direction_images('left')
            self.centerx -= self.ai_settings.ship_speed_factor
        if keystate[pygame.K_RIGHT] and self.rect.right < self.screen_rect.right:
            self.direction = 'right'
            self.image = self.animation.get_direction_images('right')
            self.centerx += self.ai_settings.ship_speed_factor
        if keystate[pygame.K_UP] and self.rect.top > 0:
            self.direction = 'up'
            self.image = self.animation.get_direction_images('up')
            self.bottom -= self.ai_settings.ship_speed_factor
        if keystate[pygame.K_DOWN] and self.rect.bottom < self.screen_rect.bottom:
            self.direction = 'down'
            self.image = self.animation.get_direction_images('down')
            self.bottom += self.ai_settings.ship_speed_factor
        
        # 根据self.center更新rect对象
        self.rect.centerx = self.centerx
        self.rect.bottom = self.bottom
    
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
        self.centerx = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom
    
    def update_bullets(self):
        '''
        更新子弹的位置，并删除已消失的子弹
        :return:
        '''
        # 更新子弹的位置
        self.ship_bullet_group.update()
        # 删除已消失的子弹
        for bullet in self.ship_bullet_group.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.bottom >= self.ai_settings.screen_height:
                self.ship_bullet_group.remove(bullet)
        # print(len(ship_bullet_group))  # 如果你留下这条语句，游戏的速度将大大降低
        self.check_bullet_alien_collisions()
    
    def check_bullet_alien_collisions(self):
        '''
        响应子弹和外星人的碰撞
        :return:
        '''
        # 检查是否有子弹击中了外星人,如果是这样，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.ship_bullet_group, self.alien_group,
                                                self.ai_settings.bullets_collide, self.ai_settings.alien_collide)
        """方法sprite.groupcollide()
         将每颗子弹的rect同每个外星人的rect进行比较，并返回一个字典，其中包含发生了碰撞的子弹和外星人。
         在这个字典中，每个键都是一颗子弹，而相应的值都是被击中的外星人
         可将第一个布尔实参设置为False，并让第二个布尔实参为True。这样被击中的外星人将消失，
         但所有的子弹都始终有效，直到抵达屏幕顶端后消失。
        """
        if collisions:  # 检查这个字典是否存在，如果存在，就将得分加上一个外星人值的点数
            # 代码可能遗漏了一些被消灭的外星人
            for alien_group in collisions.values():  # collisions.values()每个值都是一个列表，包含被同一颗子弹击中的所有外星人
                # 都将一个外星人的点数乘以其中包含的外星人数量，并将结果加入到当前得分中
                self.stats.score += self.ai_settings.alien_points * len(alien_group)
                
                # 调用prep_score()来创建一幅显示最新得分的新图像
                self.score_board.prep_score()
            self.check_high_score()
            '''
            第一次玩这款游戏时，当前得分就是最高得分，因此两个地方显示的都是当前得分。
            但再次开始这个游戏时，最高得分出现在中央，而当前得分出现在右边
            '''
        # print(len(self.alien_group))
        if len(self.alien_group) == 0:
            # 删除现有的子弹，加快游戏节奏，并创建一群新的外星人
            self.ship_bullet_group.empty()
            self.start_new_level()
    
    def check_high_score(self):
        '''
        检查是否诞生了新的最高得分
        :return:
        '''
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.score_board.prep_high_score()
        '''
        比较当前得分和最高得分，如果当前得分更高，就更新high_score的值,
        并调用prep_high_score()来更新包含最高得分的图像
        '''
    
    def start_new_level(self):
        '''
        升级
        :return:
        '''
        # print('升级')
        self.ai_settings.increase_speed()
        # 如果整群外星人都被消灭，就提高一个等级
        self.stats.level += 1
        # 并调用prep_level()，以确保正确地显示新等级
        self.score_board.prep_level()
        
        # 创建一个外星人
        alien = Alien(self.ai_settings, self.screen, self.stats, self.score_board, self,
                      self.alien_group, self.alien_bullet_group, self.correct)
        # 创建外星人群
        alien.create_fleet()
        
        self.correct.life_reward()  # 每升一级，生命+1
        self.correct.sbullet_speed_limit()  # 飞船子弹速度限制50
    
    def fire_bullet(self):
        '''
        如果还没有到达限制，就发射一颗子弹，限制子弹数量判断
        :return:
        '''
        if len(self.ship_bullet_group) < self.ai_settings.ship_bullets_allowed - 0.5:  # 0.5修正值
            # 创建一颗子弹，并将其加入到编组bullets中
            new_bullet = ShipBullet(self.ai_settings, self.screen, self)
            self.ship_bullet_group.add(new_bullet)
    
    def fire_opposite_bullet(self):
        '''
        如果还没有到达限制，就发射一颗子弹，限制子弹数量判断
        :return:
        '''
        if len(self.ship_bullet_group) < self.ai_settings.ship_bullets_allowed - 0.5:  # 0.5修正值
            # 创建一颗子弹，并将其加入到编组bullets中
            new_bullet = OppositeShipBullet(self.ai_settings, self.screen, self)
            self.ship_bullet_group.add(new_bullet)
    
    def double_hit(self):
        '''
        如果还没有到达限制，就发射多颗子弹，限制子弹数量判断
        :return:
        '''
        if len(self.ship_bullet_group) < self.ai_settings.ship_bullets_allowed - 0.5:  # 0.5修正值
            # 创建多颗子弹，并将其加入到编组bullets中
            # print(self.stats.level)
            # print(self.stats.level // 5+1)
            for item in range(self.stats.level // 5+1):
                new_bullet = ShipBullet(self.ai_settings, self.screen, self)
                self.ship_bullet_group.add(new_bullet)
                # time.sleep(0.5)
                
        # self.correct.double_hit()
