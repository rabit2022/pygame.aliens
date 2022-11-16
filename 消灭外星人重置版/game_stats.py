class GameStats(object):
    # 跟踪游戏的统计信息
    def __init__(self, ai_settings):
        '''
        初始化统计信息
        :param ai_settings:
        '''
        self.ai_settings = ai_settings
        self.reset_stats()
        '''
        在玩家开始新游戏时也能调用reset_stats()，游戏刚启动时处于活动状态
        玩家的飞船都用完后将game_active设置为False
        '''
        
        self.ship_exist = False  # 玩家是否还有生命
        
        # 在任何情况下都不应重置最高得分
        self.high_score = 0
        # 鉴于在任何情况下都不会重置最高得分，我们在__init__()中而不是reset_stats()中初始化high_score
        
        # 显示等级
        self.level = self.ai_settings.ship_initial_level
        # print(self.level)
    
    def reset_stats(self):
        '''
        初始化在游戏运行期间可能变化的统计信息
        :return:
        '''
        self.ships_left = self.ai_settings.ship_limit  # 玩家剩余生命
        self.score = 0
        '''为在每次开始游戏时都重置得分，我们在reset_stats()而不是__init__()中初始化score'''
        # self.level = self.settings.ship_initial_level
