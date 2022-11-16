import random
import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, sb, bullets, aliens, stats):
    '''
    响应按键
    :param event:
    :param ai_settings:
    :param screen:
    :param ship:
    :param sb:
    :param bullets:
    :param aliens:
    :param stats:
    :return:
    '''
    if event.key == pygame.K_RIGHT:
        # print('right')
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # print('left')
        ship.moving_left = True
    
    elif event.key == pygame.K_SPACE:
        # print('firing')
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
        print('强制退出')
        sys.exit()
    elif event.key == pygame.K_v:  # 增加血量
        print('生命+1')
        # 将ships_left减1
        stats.ships_left += 1
        # 更新记分牌,显示还余下多少艘飞船
        sb.prep_ships()
        # 重置外星人
        refresh(ai_settings, screen, ship, aliens, bullets)
    
    elif event.key == pygame.K_c:  # 子弹穿透
        if ai_settings.bullets_collide:
            ai_settings.bullets_collide = False
            print('子弹穿透', not ai_settings.bullets_collide)
        elif not ai_settings.bullets_collide:
            ai_settings.bullets_collide = True
            print('子弹不穿透', not ai_settings.bullets_collide)
    
    elif event.key == pygame.K_r:
        print('全部初始化')
        # 初始化随游戏进行而变化的设置
        ai_settings.initialize_dynamic_settings()
        # 如果整群外星人都被消灭，就提高一个等级
        stats.level = 1
        # 并调用prep_level()，以确保正确地显示新等级
        sb.prep_level()
        # 重置外星人
        refresh(ai_settings, screen, ship, aliens, bullets)
        # # 创建外星人群
        # create_fleet(settings, screen, alien, alien_group)
    elif event.key == pygame.K_z:
        # 更换音乐
        songs = ['./素材/音乐/Old_Memory.mp3', './素材/音乐/kanon.mp3', './素材/音乐/blue.mp3']
        song = random.choice(songs)
        print(song)
        ai_settings.music(song)
    
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    '''
    如果还没有到达限制，就发射一颗子弹，限制子弹数量判断
    :param ai_settings:
    :param screen:
    :param ship:
    :param bullets:
    :return:
    '''
    if len(bullets) < ai_settings.ship_bullets_allowed:
        # 创建一颗子弹，并将其加入到编组bullets中
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    '''
    响应松开
    :param event:
    :param ship:
    :return:
    '''
    
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    '''
    在玩家单击Play按钮时开始新游戏
    :param ai_settings:
    :param screen:
    :param stats:
    :param sb:
    :param play_button:
    :param ship:
    :param aliens:
    :param bullets:
    :param mouse_x:
    :param mouse_y:
    :return:
    '''
    # 使用collidepoint()检查鼠标单击位置是否在Play按钮的rect内
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # 标志button_clicked的值为True或False
    if button_clicked and not stats.ship_exist:
        '''仅当玩家单击了Play按钮且游戏当前处于非活
        动状态时，游戏才重新开始'''
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    '''
    响应按键和鼠标事件
    :param ai_settings:
    :param screen:
    :param stats:
    :param sb:
    :param play_button:
    :param ship:
    :param aliens:
    :param bullets:
    :return:
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, sb, bullets, aliens, stats)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 玩家用鼠标单击Play按钮时作出响应
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # get_pos()，它返回一个元组，其中包含玩家单击时鼠标的x和y坐标
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x,
                              mouse_y)


def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''
    开始游戏
    :param ai_settings:
    :param screen:
    :param stats:
    :param sb:
    :param ship:
    :param aliens:
    :param bullets:
    :return:
    '''
    print('开始游戏')
    # 隐藏光标
    pygame.mouse.set_visible(False)
    # 重置游戏统计信息
    stats.reset_stats()
    stats.ship_exist = True
    sb.prep_images()
    '''重置记分牌图像
        score_board.prep_score()
        score_board.prep_high_score()
        score_board.prep_level()
        #为在游戏开始时让玩家知道他有多少艘飞船，我们在开始新游戏时调用prep_ships()
        score_board.prep_ships()
    '''
    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    # 创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, background, aliens, bullets, play_button):
    '''
    更新屏幕上的图像，并切换到新屏幕
    :param ai_settings:
    :param screen:
    :param stats:
    :param sb:
    :param ship:
    :param background:
    :param aliens:
    :param bullets:
    :param play_button:
    :return:
    '''
    # 绘制背景
    screen.blit(background, (0, 0))
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.background_color)
    # 加载背景
    screen.blit(background, (0, 0))
    
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    # 绘制飞船
    ship.blitme()
    # 绘制外星人
    aliens.draw(screen)
    # 显示得分
    sb.show_score()
    
    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.ship_exist:
        play_button.draw_button()
    
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def check_high_score(stats, sb):
    '''
    检查是否诞生了新的最高得分
    :param stats:
    :param sb:
    :return:
    '''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
    '''
    比较当前得分和最高得分，如果当前得分更高，就更新high_score的值,
    并调用prep_high_score()来更新包含最高得分的图像
    '''


# 以下对多个外星人
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''
    检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    :param ai_settings:
    :param screen:
    :param stats:
    :param sb:
    :param ship:
    :param aliens:
    :param bullets:
    :return:
    '''
    check_fleet_edges(ai_settings, aliens)
    # 更新外星人群中所有外星人的位置
    aliens.update()
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        print("Ship hit!!!")
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def change_fleet_direction(ai_settings, aliens):
    '''
    将整群外星人下移，并改变它们的方向
    :param ai_settings:
    :param aliens:
    :return:
    '''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    '''
    有外星人到达边缘时采取相应的措施
    :param ai_settings:
    :param aliens:
    :return:
    '''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''
    响应被外星人撞到的飞船
    :param ai_settings:
    :param screen:
    :param stats:
    :param sb:
    :param ship:
    :param aliens:
    :param bullets:
    :return:
    '''
    if stats.ships_left > 0:  # 检查玩家是否至少还有一艘飞船
        # 将ships_left减1
        stats.ships_left -= 1
        # 更新记分牌
        sb.prep_ships()
        # 重置外星人
        refresh(ai_settings, screen, ship, aliens, bullets)
    else:
        # game over
        stats.ship_exist = False
        # 游戏结束后，我们将重新显示光标
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''
    检查是否有外星人到达了屏幕底端
    :param ai_settings:
    :param screen:
    :param stats:
    :param sb:
    :param ship:
    :param aliens:
    :param bullets:
    :return:
    '''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def get_number_aliens_x(ai_settings, alien_width):
    '''
    计算每行可容纳多少个外星人
    :param ai_settings:
    :param alien_width:
    :return:
    '''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    '''
    计算屏幕可容纳多少行外星人
    :param ai_settings:
    :param ship_height:
    :param alien_height:
    :return:
    '''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''
    创建一个外星人
    :param ai_settings:
    :param screen:
    :param aliens:
    :param alien_number:
    :param row_number:
    :return:
    '''
    # 创建一个外星人，并计算一行可容纳多少个外星人  外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    '''
    创建外星人群
    :param ai_settings:
    :param screen:
    :param ship:
    :param aliens:
    :return:
    '''
    # 创建一个外星人，并计算每行可容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def refresh(ai_settings, screen, ship, aliens, bullets):
    '''
    重置外星人
    :param ai_settings:
    :param screen:
    :param ship:
    :param aliens:
    :param bullets:
    :return:
    '''
    # print('重置外星人')
    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    # 创建一群新的外星人，并将飞船放到屏幕底端中央
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    # 暂停
    sleep(0.5)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''
    更新子弹的位置，并删除已消失的子弹
    :param ai_settings:
    :param screen:
    :param stats:
    :param sb:
    :param ship:
    :param aliens:
    :param bullets:
    :return:
    '''
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(ship_bullet_group))  # 如果你留下这条语句，游戏的速度将大大降低
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''
    响应子弹和外星人的碰撞
    :param ai_settings:
    :param screen:
    :param stats:
    :param sb:
    :param ship:
    :param aliens:
    :param bullets:
    :return:
    '''
    # 检查是否有子弹击中了外星人,如果是这样，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, ai_settings.bullets_collide, ai_settings.alien_collide)
    """方法sprite.groupcollide()
     将每颗子弹的rect同每个外星人的rect进行比较，并返回一个字典，其中包含发生了碰撞的子弹和外星人。
     在这个字典中，每个键都是一颗子弹，而相应的值都是被击中的外星人
     可将第一个布尔实参设置为False，并让第二个布尔实参为True。这样被击中的外星人将消失，
     但所有的子弹都始终有效，直到抵达屏幕顶端后消失。
    """
    if collisions:  # 检查这个字典是否存在，如果存在，就将得分加上一个外星人值的点数
        # 代码可能遗漏了一些被消灭的外星人
        for aliens in collisions.values():  # collisions.values()每个值都是一个列表，包含被同一颗子弹击中的所有外星人
            # 都将一个外星人的点数乘以其中包含的外星人数量，并将结果加入到当前得分中
            stats.score += ai_settings.alien_points * len(aliens)
            
            # 调用prep_score()来创建一幅显示最新得分的新图像
            sb.prep_score()
        check_high_score(stats, sb)
        '''
        第一次玩这款游戏时，当前得分就是最高得分，因此两个地方显示的都是当前得分。
        但再次开始这个游戏时，最高得分出现在中央，而当前得分出现在右边
        '''
    if len(aliens) == 0:
        # 删除现有的子弹，加快游戏节奏，并创建一群新的外星人
        bullets.empty()
        start_new_level(ai_settings, stats, sb, screen, ship, aliens)


def start_new_level(ai_settings, stats, sb, screen, ship, aliens):
    '''
    升级
    :param ai_settings:
    :param stats:
    :param sb:
    :param screen:
    :param ship:
    :param aliens:
    :return:
    '''
    ai_settings.increase_speed()
    # 如果整群外星人都被消灭，就提高一个等级
    stats.level += 1
    # 并调用prep_level()，以确保正确地显示新等级
    sb.prep_level()
    # 创建外星人群
    create_fleet(ai_settings, screen, ship, aliens)
    
    # # 强制结束游戏
    # if stats.level >= 10:
    #     settings.alien_collide = False
