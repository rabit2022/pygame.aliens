import pygame.font


class Button(object):
    def __init__(self, ai_settings, screen, information):
        '''
        初始化按钮的属性
        :param ai_settings:
        :param screen:
        :param information:
        '''
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # 设置按钮的尺寸和其他属性
        self.width, self.height = self.ai_settings.button_width, self.ai_settings.button_height
        self.button_color = self.ai_settings.button_color
        self.text_color = self.ai_settings.text_color
        # 使用什么字体来渲染文本,实参None使用默认字体，而48指定了文本的字号
        # self.font = pygame.font.SysFont(self.ai_settings.font, 48)
        self.font = pygame.font.Font(self.ai_settings.font, 48)
        
        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # 按钮的标签只需创建一次
        # 调用prep_msg()来处理这样的渲染,Pygame通过将你要显示的字符串渲染为图像来处理文本
        self.prep_msg(information)
    
    def prep_msg(self, information):
        '''
        将msg渲染为图像，并使其在按钮上居中
        :param information:
        :return:
        '''
        self.msg_image = self.font.render(information, True, self.text_color, self.button_color)
        # 调用font.render()将存储在msg中的文本转换为图像
        '''布尔实参指定开启还是关闭反锯齿功能（反锯齿让文本的边缘更平滑）.余下的两个实参分别是文本颜色和背景色.
        我们启用了反锯齿功能，将文本的背景色设置为按钮的颜色（如果没有指定背景色，Pygame将以透明背景的方式渲染文本）'''
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        '''
        文本图像在按钮上居中：根据文本图像创建一个rect，并将其center属性设置为按钮的center属性
        :return:
        '''
        # 绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
