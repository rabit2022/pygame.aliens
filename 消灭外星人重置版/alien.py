import random
import time

import pygame
from pygame.sprite import Sprite

from animation_realize import Animation
from bullet import AlienBullet


class Alien(Sprite):  # 表示单个外星人的类
    def __init__(self, ai_settings, screen, stats, score_board, ship, alien_group, alien_bullet_group, correct):
        '''
        初始化外星人并设置其起始位置
        :param ai_settings:
        :param screen:
        :param stats:
        :param score_board:
        :param ship:
        :param alien_group:
        '''
        super(Alien, self).__init__()
        self.correct = correct
        self.alien_bullet_group = alien_bullet_group
        self.alien_group = alien_group
        self.ship = ship
        self.score_board = score_board
        self.stats = stats
        self.screen = screen
        self.ai_settings = ai_settings
        
        # 加载外星人图像，并设置其rect属性
        # self.image = pygame.image.load(self.settings.alien_path)
        
        self.animation = Animation()
        # self.images = self.animation.get_images('外星人.jpg', rows=3, columns=4)
        # self.image = self.images[0]
        self.image = self.animation.get_random_image(self.ai_settings.alien_path, rows=3, columns=4)
        
        self.rect = self.image.get_rect()
        # print(self.rect)
        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 存储外星人的准确位置
        self.x = float(self.rect.x)
        
        self.one_time = pygame.time.get_ticks()
    
    def blitme(self):
        '''
        在指定位置绘制外星人
        :return:
        '''
        self.screen.blit(self.image, self.rect)
    
    def check_edges(self):
        '''
        如果外星人位于屏幕边缘
        :return: 返回True
        '''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
    
    def update(self):
        '''
        向左或向右移动外星人
        :return:
        '''
        # self.image = self.animation.get_current_image()  # 当前帧数的图片
        
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        # print(self.rect.x,self.rect.y)
    
    # 以下对多个外星人
    def update_aliens(self):
        '''
        检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
        :return:
        '''
        self.check_fleet_edges()
        # 更新外星人群中所有外星人的位置
        self.alien_group.update()  # 图形
        self.update()  # 坐标
        
        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.alien_group):
            print("Ship hit!!!")
            self.ship_hit()
        # 检查是否有外星人到达屏幕底端
        self.check_aliens_bottom()
        
        self.two_time = pygame.time.get_ticks()
        
        delta = self.two_time - self.one_time
        # print(delta)
        
        if delta >= 500 * 8:
            self.ai_settings.invincible = False
            if delta <= 500 * 8 + 3 and self.ai_settings.invincible == False:
                print('小脆皮')
        
        # self.one_time = pygame.time.get_ticks()
    
    def change_fleet_direction(self):
        '''
        将整群外星人下移，并改变它们的方向
        :return:
        '''
        for alien in self.alien_group.sprites():
            alien.rect.y += self.ai_settings.fleet_drop_speed
        self.ai_settings.fleet_direction *= -1
    
    def check_fleet_edges(self):
        '''
        有外星人到达边缘时采取相应的措施
        :return:
        '''
        for alien in self.alien_group.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break
    
    def ship_hit(self):
        '''
        响应被外星人撞到的飞船
        :return:
        '''
        if not self.ai_settings.invincible:
            if self.stats.ships_left > 0:  # 检查玩家是否至少还有一艘飞船
                # 将ships_left减1
                self.stats.ships_left -= 1
                # 更新记分牌
                self.score_board.prep_ships()
                # 重置外星人
                self.refresh()
                
                print('小无敌，持续6秒')
                self.ai_settings.invincible = True
                self.one_time = pygame.time.get_ticks()
                
            else:
                # game over
                self.stats.ship_exist = False
                # 游戏结束后，我们将重新显示光标
                pygame.mouse.set_visible(True)
    
    def check_aliens_bottom(self):
        '''
        检查是否有外星人到达了屏幕底端
        :return:
        '''
        screen_rect = self.screen.get_rect()
        for alien in self.alien_group.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样进行处理
                self.ship_hit()
                self.refresh()
                break
    
    def get_number_aliens_x(self, alien_width):
        '''
        计算每行可容纳多少个外星人
        :param alien_width:
        :return:
        '''
        available_space_x = self.ai_settings.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x
    
    def get_number_rows(self, ship_height, alien_height):
        '''
        计算屏幕可容纳多少行外星人
        :param ship_height:
        :param alien_height:
        :return:
        '''
        available_space_y = (self.ai_settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (2 * alien_height))
        
        # if self.stats.level >= 40:
        #     number_rows -= 1
        return number_rows
    
    def create_alien(self, alien_number, row_number):
        '''
        创建一个外星人
        :param alien_number:
        :param row_number:
        :return:
        '''
        # 创建一个外星人，并计算一行可容纳多少个外星人  外星人间距为外星人宽度
        alien = Alien(self.ai_settings, self.screen, self.stats, self.score_board, self.ship,
                      self.alien_group, self.alien_bullet_group, self.correct)
        
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.alien_group.add(alien)
    
    def create_fleet(self):
        '''
        创建外星人群
        :return:
        '''
        number_aliens_x = self.get_number_aliens_x(self.rect.width)
        number_rows = self.get_number_rows(self.ship.rect.height, self.rect.height)
        # 创建第一行外星人
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number)
    
    def refresh(self):
        '''
        重置外星人
        :return:
        '''
        # print('重置外星人')
        # print(len(self.alien_group), len(self.ship.ship_bullet_group), len(self.alien_bullet_group))
        # 清空外星人列表和子弹列表
        self.alien_group.empty()
        self.ship.ship_bullet_group.empty()
        self.alien_bullet_group.empty()
        
        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        self.create_fleet()
        self.ship.center_ship()
        # 暂停
        time.sleep(0.5)
    
    def update_bullets(self):
        '''
        更新子弹的位置，并删除已消失的子弹
        :return:
        '''
        # 更新子弹的位置
        self.alien_bullet_group.update()
        
        screen_rect = self.screen.get_rect()
        # 删除已消失的子弹
        for bullet in self.alien_bullet_group.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.top >= screen_rect.bottom:
                self.alien_bullet_group.remove(bullet)
        # print(len(ship_bullet_group))  # 如果你留下这条语句，游戏的速度将大大降低
        self.check_bullet_alien_collisions()  # 子弹和外星人的碰撞
        self.correct.sbullet_abullet_concllide()  # 子弹和子弹的碰撞
    
    def check_bullet_alien_collisions(self):
        '''
        响应子弹和外星人的碰撞
        :return:
        '''
        
        ship_group = pygame.sprite.Group()
        ship_group.add(self.ship)
        # 检查是否有子弹击中了外星人,如果是这样，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.alien_bullet_group, ship_group,
                                                self.ai_settings.bullets_collide, self.ai_settings.alien_collide)
        
        if collisions:  # 检查这个字典是否存在，如果存在，就将得分加上一个外星人值的点数
            # 像飞船被撞到一样进行处理
            self.ship_hit()
    
    def fire_bullet(self):
        '''
        如果还没有到达限制，就发射一颗子弹，限制子弹数量判断
        :return:
        '''
        # print(len(self.alien_group))
        for alien in self.alien_group.sprites():  # 每个外星人都能发射子弹
            if random.randint(1, int(1 / self.ai_settings.alien_bullets_probability)) == 1:  # 发射子弹概率
                if len(self.alien_bullet_group) < self.ai_settings.alien_bullets_allowed:  # 限制子弹数量
                    # 创建一颗子弹，并将其加入到编组bullets中
                    # print(alien)
                    new_bullet = AlienBullet(self.ai_settings, self.screen, alien)
                    self.alien_bullet_group.add(new_bullet)
