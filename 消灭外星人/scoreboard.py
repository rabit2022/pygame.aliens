import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard(object):
    # 显示得分信息的类
    def __init__(self, ai_settings, screen, stats):
        '''
        报告我们跟踪的值
        初始化显示得分涉及的属性
        :param ai_settings:
        :param screen:
        :param stats:
        '''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        
        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)  # 文本颜色
        self.font = pygame.font.SysFont(None, 48)  # 实例化一个字体对象
        self.prep_images()
    
    def prep_images(self):
        '''
        图像显示
        :return:
        '''
        # 准备初始得分图像
        self.prep_score()
        # 准备包含最高得分的图像
        self.prep_high_score()
        # 显示当前等级
        self.prep_level()
        # 显示余下的飞船数
        self.prep_ships()
    
    def prep_score(self):
        # 将得分转换为一幅渲染的图像"""
        # 将设置得分的格式，在大数字中添加用逗号表示的千位分隔符
        rounded_score = round(self.stats.score, -1)
        '''
        rounded_score = int(round(self.stats.score, -1))
        在Python 2.7中, round()总是返回一个小数值，因此我们使用int()来确保报告的得分为整数
        Python 3，可省略对int()的调用
        '''
        '''函数round()通常让小数精确到小数点后多少位，小数位数是由第二个实参指定的。
        如果将第二个实参指定为负数，round()将圆整到最近的10、100、1000等整数倍
        '''
        
        score_str = "{:,}".format(rounded_score)
        '''使用了一个字符串格式设置指令，它让Python将数值转换为字符串时在其中插入逗号，
        例如，输出1,000,000而不是1000000。'''
        
        # score_str = str(self.stats.score)#将数字值stats.score转换为字符串
        
        # 将这个字符串传递给创建图像的render(),向render()传递了屏幕背景色，以及文本颜色。
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.background_color)
        
        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20  # 右边缘与屏幕右边缘相距20像素
        self.score_rect.top = 20  # 上边缘与屏幕上边缘也相距20像素
    
    def show_score(self):
        '''
        得分显示
        :return:
        '''
        # 在屏幕上显示得分
        self.screen.blit(self.score_image, self.score_rect)
        # 在屏幕上显示最高得分
        self.screen.blit(self.high_score_image, self.high_score_rect)
        # 在屏幕上显示飞船
        self.screen.blit(self.level_image, self.level_rect)
        # 绘制飞船
        self.ships.draw(self.screen)
    
    def prep_high_score(self):
        '''
        将最高得分转换为渲染的图像
        :return:
        '''
        high_score = int(round(self.stats.high_score, -1))  # 将最高得分圆整到最近的10的整数倍
        high_score_str = "{:,}".format(high_score)  # 添加了用逗号表示的千分位分隔符
        
        # 根据最高得分生成一幅图像
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.background_color)
        self.high_score_rect = self.high_score_image.get_rect()  # 将最高得分放在屏幕顶部中央
        self.high_score_rect.centerx = self.screen_rect.centerx  # 水平居中
        self.high_score_rect.top = self.score_rect.top  # 将其top属性设置为当前得分图像的top属性
    
    def prep_level(self):
        '''
        将等级转换为渲染的图像
        方法prep_level()根据存储在stats.level中的值创建一幅图像
        :return:
        '''
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.background_color)

        # print(self.stats.level)
        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right  # 并将其right属性设置为得分的right属性
        self.level_rect.top = self.score_rect.bottom + 10
        '''将top属性设置为比得分图像的bottom属性大10像素，以便在得分和等级之间留出一定的空间'''
    
    def prep_ships(self):
        '''
        显示还余下多少艘飞船
        方法prep_ships()创建一个空编组self.ships，用于存储飞船实例
        :return:
        '''
        self.ships = Group()
        # 根据玩家还有多少艘飞船运行一个循环相应的次数
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)  # 创建一艘新飞船
            # 并设置其x坐标，让整个飞船编组都位于屏幕左边，且每艘飞船的左边距都为10像素
            ship.rect.x = 10 + ship_number * ship.rect.width
            # 将y坐标设置为离屏幕上边缘10像素，让所有飞船都与得分图像对齐
            ship.rect.y = 10
            # 将每艘新飞船都添加到编组ships中
            self.ships.add(ship)
