import pygame


class Settings:  # 存储《外星人入侵》的所有设置的类
    def __init__(self):
        '''
        初始化游戏的静态设置
        '''
        #  屏幕设置
        self.screen_width = 800  # 屏幕大小
        self.screen_height = 500
        self.background_color = (100, 100, 230)  # 设置背景色（红，绿，蓝）255
        # (230, 230, 230)浅灰色,(255,255,255)白(0,0,0)黑
        self.fps = 200  # 刷新率
        self.clock = pygame.time.Clock()
        
        # 飞船的设置
        self.ship_speed_factor = 1.5  # 飞船速度
        self.ship_limit = 3  # 玩家拥有的飞船数
        
        # 子弹设置
        self.ship_bullet_speed = 7
        # 创建宽3像素、高15像素的深灰色子弹
        self.ship_bullet_width = 3
        self.ship_bullet_height = 15
        self.ship_bullet_color = 60, 60, 60
        self.ship_bullets_allowed = 1  # 限制子弹数量
        
        # 外星人设置
        self.alien_speed_factor = 1  # 移动速度
        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1
        
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
    
    # @staticmethod
    def music(self, song='./素材/音乐/Old_Memory.mp3'):
        '''
        添加背景音乐
        :return:
        '''
        pygame.mixer.init()
        pygame.mixer.music.load(song)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)  # 循环次数  -1表示无限循环
    
    def initialize_dynamic_settings(self):
        '''
        初始化随游戏进行而变化的设置
        :return:
        '''
        self.ship_speed_factor = 1.5
        self.ship_bullet_speed = 3
        self.alien_speed_factor = 1
        
        # fleet_direction为1表示向右；为-1表示向左
        self.fleet_direction = 1
        
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
        
        # 提高外星人点数
        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)
        '''
        现在每当提高一个等级时，你都会在终端窗口看到新的点数值。
        可能会影响游戏的性能以及分散玩家的注意力
        '''
