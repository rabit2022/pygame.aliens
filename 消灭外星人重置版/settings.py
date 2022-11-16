import os
import random

import pygame


class Settings:
    # 存储《外星人入侵》的所有设置的类
    def __init__(self):
        '''
        初始化游戏的静态设置
        '''
        # Define colors（红，绿，蓝）255
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.LIGHT_GREY = (230, 230, 230)

        self.prefix = "./素材/"

        self.moe_sister = '亚丝娜.png'
        # 路径设置
        self.caption = self.moe_sister.split('.')[0] + "与小怪兽"
        self.icon = self.prefix + 'loli.jpg'  # 图标
        self.play_button = '凡是过往皆为序章'

        # 凡是过往皆为序章
        self.background_path = self.prefix + '背景/蓝天白云.png'
        self.alien_path = self.prefix + '外星人/外星人.png'
        self.ship_path = self.prefix + '英雄/' + self.moe_sister

        # 字体
        self.font = self.prefix + '字体/小南同学.ttf'
        self.text_color = self.BLUE
        # (30, 30, 30)

        # 按钮
        self.button_width, self.button_height = 200, 50
        self.button_color = self.GREEN

        #  屏幕设置
        self.screen_width = 800  # 屏幕大小
        self.screen_height = 500
        self.background_color = self.GREEN
        # (100, 100, 230)
        self.FPS = 200  # 刷新率
        self.clock = pygame.time.Clock()
        self.pause = False
        self.game_over = False

        # 子弹设置

        # 创建宽3像素、高15像素的深灰色子弹
        self.ship_bullet_width = 5
        self.ship_bullet_height = 15

        self.ship_bullet_speed = 3
        self.ship_bullet_color = self.GREEN
        self.ship_bullets_allowed = 1  # ship限制子弹数量

        self.alien_bullet_width = 3
        self.alien_bullet_height = 15

        self.alien_bullet_speed = self.ship_bullet_speed * 0.1

        self.alien_bullet_color = self.RED
        self.alien_bullets_allowed = 4  # alien限制子弹数量
        self.alien_bullets_probability = 0.001  # alien发射子弹的概率

        # 飞船的设置
        self.ship_speed_factor = 1.5  # 飞船速度
        self.ship_limit = 3  # 玩家拥有的飞船数
        self.invincible = False  # 无敌
        self.ship_initial_level = 1  # 等级

        # 外星人设置
        self.alien_speed_factor = 1  # 移动速度
        self.fleet_drop_speed = 3  # 下落速度
        self.fleet_direction = 1  # fleet_direction为1表示向右移，为-1表示向左移

        # 偏离速度
        self.alien_bullet_deviation = self.ship_bullet_speed * self.alien_bullets_probability * 100

        # 游戏设置
        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        '''
        控制游戏节奏的加快速度：
        2表示玩家每提高一个等级，游戏的节奏就翻倍；
        1表示游戏节奏始终不变。
        设置为1.1能够将游戏节奏提高到够快，让游戏既有难度，又并非不可完成
        '''

        # 外星人分数的提高速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

        # 子弹击中了外星人,子弹是否消失
        self.bullets_collide = True
        self.alien_collide = True

    def music(self, music_path=None):
        '''
        添加背景音乐
        :return:
        '''
        '''
        音乐格式转换在线
        https://convertio.co/zh/audio-converter/
        '''
        if music_path is None:
            music_path = self.get_random_image('./素材/音乐')

        song = './素材/音乐/' + music_path
        print(music_path)
        pygame.mixer.init()
        pygame.mixer.music.load(song)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)  # 循环次数  -1表示无限循环

    def initialize_dynamic_settings(self):
        '''
        初始化随游戏进行而变化的设置
        :return:
        '''
        self.ship_speed_factor = 1.5  # 1.5
        self.ship_bullet_speed = 3

        self.alien_speed_factor = 1
        self.alien_bullet_speed = self.ship_bullet_speed * 0.1

        # fleet_direction为1表示向右；为-1表示向左
        self.fleet_direction = 1

        # 限制子弹数量
        self.ship_bullets_allowed = 1  # ship限制子弹数量
        self.alien_bullets_allowed = 4
        self.alien_bullets_probability = 0.003

        # 记分
        self.alien_points = 50

        # 子弹击中了外星人,子弹是否消失
        self.bullets_collide = True
        self.alien_collide = True

    def increase_speed(self):
        '''
        提高速度设置:提高飞船、子弹和外星人的速度
        提高这些游戏元素的速度，我们将每个速度设置都乘以speedup_scale的值
        :return:
        '''
        self.ship_speed_factor *= self.speedup_scale
        self.ship_bullet_speed *= self.speedup_scale

        self.alien_speed_factor *= self.speedup_scale
        self.alien_bullet_speed *= self.speedup_scale
        # 提高外星人点数
        self.alien_points = int(self.alien_points * self.score_scale)

        # 子弹数量
        self.alien_bullets_allowed *= self.speedup_scale
        self.ship_bullets_allowed *= self.speedup_scale
        # print(self.ship_bullets_allowed)
        # print(self.alien_points)
        '''
        现在每当提高一个等级时，你都会在终端窗口看到新的点数值。
        可能会影响游戏的性能以及分散玩家的注意力
        '''

    @staticmethod
    def get_random_colour():
        # tum = []
        # for i in range(3):
        #     a = random.randint(0, 256)
        #     tum.append(a)
        # print(tum)
        tum = [random.randint(0, 255) for _ in range(3)]
        # print(tum)
        return tuple(tum)

    @staticmethod
    def get_random_image(path):
        hero = os.listdir(path)
        # print(hero)
        moe_sister = random.choice(hero)
        return moe_sister


if __name__ == '__main__':
    s = Settings()
    a = s.get_random_colour()
    # print(a)
    b = s.get_random_image('./素材/音乐')
    print(b)
