# -*- coding: UTF-8 -*-
"""
@summary:
@usage:
"""
import pygame


class Correct(object):
    # 赏惩系统,修正系统
    def __init__(self, ai_settings, stats, score_board, ship_bullet_group, alien_bullet_group):
        self.ai_settings = ai_settings
        self.ship_bullet_group = ship_bullet_group
        self.alien_bullet_group = alien_bullet_group
        self.score_board = score_board
        self.stats = stats
    
    def life_reward(self):
        '''
        每升一级，生命+1 ship
        :return:
        '''
        if self.stats.level % 5 == 0:
            print('升级奖励，生命+1')
            # 将ships_left减1
            self.stats.ships_left += 1
            # 更新记分牌,显示还余下多少艘飞船
            self.score_board.prep_ships()
            # 重置外星人
            # self.refresh()
    
    def sbullet_abullet_concllide(self):
        '''
        子弹互消系统alien
        :return:
        '''
        # 检查是否有子弹击中了外星人,如果是这样，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.ship_bullet_group, self.alien_bullet_group,
                                                self.ai_settings.bullets_collide, True)
        if collisions:  # 检查这个字典是否存在，如果存在，就将得分加上一个外星人值的点数
            ...
    
    def sbullet_speed_limit(self):
        '''
        飞船子弹速度限制为50 ship
        :return:
        '''
        if self.ai_settings.ship_bullet_speed >= 50:
            self.ai_settings.ship_bullet_speed = 50
        # print(self.settings.ship_bullet_speed)

    