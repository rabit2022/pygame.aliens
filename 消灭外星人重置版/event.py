# -*- coding: UTF-8 -*-
"""
@summary:
@usage:
"""

import pygame


class Event(object):
    def __init__(self, ai_settings, screen, stats, score_board, play_button, ship, aliens):
        '''
        
        :param ai_settings:
        :param screen:
        :param stats:
        :param score_board:
        :param play_button:
        :param ship:
        :param aliens:
        '''
        self.aliens = aliens
        self.ship = ship
        self.play_button = play_button
        self.score_board = score_board
        self.stats = stats
        self.screen = screen
        self.ai_settings = ai_settings
    
    def check_keydown_events(self, event):
        '''
        响应按键
        :param event:
        :return:
        '''
        
        if event.key == pygame.K_SPACE:
            #     self.ship.fire_bullet()
            # elif event.key == pygame.K_n:
            self.ship.double_hit()
        
        elif event.key == pygame.K_m:
            self.ship.fire_opposite_bullet()
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            print('强制退出')
            self.ai_settings.game_over = True
        elif event.key == pygame.K_v:  # 增加血量
            print('生命+1')
            # 将ships_left减1
            self.stats.ships_left += 1
            # 更新记分牌,显示还余下多少艘飞船
            self.score_board.prep_ships()
            # 重置外星人
            self.aliens.refresh()
        
        elif event.key == pygame.K_c:  # 子弹穿透
            if self.ai_settings.bullets_collide:
                self.ai_settings.bullets_collide = False
                print('子弹穿透', not self.ai_settings.bullets_collide)
            elif not self.ai_settings.bullets_collide:
                self.ai_settings.bullets_collide = True
                print('子弹不穿透', not self.ai_settings.bullets_collide)
        elif event.key == pygame.K_s:  # 无敌
            if self.ai_settings.invincible:
                self.ai_settings.invincible = False
                print('脆皮', not self.ai_settings.bullets_collide)
            elif not self.ai_settings.invincible:
                self.ai_settings.invincible = True
                print('无敌', not self.ai_settings.bullets_collide)
        elif event.key == pygame.K_r:
            print('全部初始化')
            # 初始化随游戏进行而变化的设置
            self.ai_settings.initialize_dynamic_settings()
            # 如果整群外星人都被消灭，就提高一个等级
            self.stats.level = 1
            # 并调用prep_level()，以确保正确地显示新等级
            self.score_board.prep_level()
            # 重置外星人
            self.start_game()
        
        elif event.key == pygame.K_z:
            # 更换音乐
            self.ai_settings.music()
        
        elif event.key == pygame.K_p:
            self.start_game()
        
        elif event.key == pygame.K_x:
            if self.ai_settings.pause:
                print('运行')
                self.ai_settings.pause = not self.ai_settings.pause
            elif not self.ai_settings.pause:
                print('暂停')
                self.ai_settings.pause = not self.ai_settings.pause
    
    def check_keyup_events(self, event):
        '''
        响应松开,人物恢复到立正姿势
        :param event:
        :return:
        '''
        if event.key == pygame.K_RIGHT:
            self.ship.image = self.ship.animation.get_direction_image(self.ship.direction)
        elif event.key == pygame.K_LEFT:
            self.ship.image = self.ship.animation.get_direction_image(self.ship.direction)
        elif event.key == pygame.K_UP:
            self.ship.image = self.ship.animation.get_direction_image(self.ship.direction)
        elif event.key == pygame.K_DOWN:
            self.ship.image = self.ship.animation.get_direction_image(self.ship.direction)
    
    def check_play_button(self, mouse_x, mouse_y):
        '''
        在玩家单击Play按钮时开始新游戏
        :param mouse_x:
        :param mouse_y:
        :return:
        '''
        # 使用collidepoint()检查鼠标单击位置是否在Play按钮的rect内
        button_clicked = self.play_button.rect.collidepoint(mouse_x, mouse_y)
        # 标志button_clicked的值为True或False
        if button_clicked and not self.stats.ship_exist:
            '''仅当玩家单击了Play按钮且游戏当前处于非活
            动状态时，游戏才重新开始'''
            # 重置游戏设置
            self.ai_settings.initialize_dynamic_settings()
            # # 隐藏光标
            # pygame.mouse.set_visible(False)
            self.start_game()
    
    def start_game(self):
        '''
        开始游戏
        :return:
        '''
        print('开始游戏')
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        self.stats.reset_stats()
        self.stats.ship_exist = True
        self.score_board.prep_images()
        '''
        重置记分牌图像
        score_board.prep_score()
        score_board.prep_high_score()
        score_board.prep_level()
        #为在游戏开始时让玩家知道他有多少艘飞船，我们在开始新游戏时调用prep_ships()
        score_board.prep_ships()
        '''
        # 重置外星人
        self.aliens.refresh()
    
    def check_events(self):
        '''
        响应按键和鼠标事件
        :return:
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # sys.exit()
                self.ai_settings.game_over = True
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 玩家用鼠标单击Play按钮时作出响应
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # get_pos()，它返回一个元组，其中包含玩家单击时鼠标的x和y坐标
                self.check_play_button(mouse_x, mouse_y)
