'''
 * @Author: alexander.huang
 * @Date:   2022-05-27 18:12:11
 * @Last Modified by: alexander.huang
 * @Last Modified time: 2022-06-1 21:40:51
'''
import os

SCREEN_WIDTH = 630
SCREEN_HEIGHT = 630
BORDER_LEN = 3
GRID_SIZE = 24

NORMAL = (255, 255, 255)
HOVER = (128, 0, 128)

TITLE = 'TankWar --190702941024黄小龙'

FONT = os.path.join(os.getcwd(),"..", 'resources/font/STXINWEI.TTF')
FONT_SIZE = SCREEN_WIDTH // 16

# 关卡
LEVEL = os.path.join(os.getcwd(), 'levels')

IMAGE = {
    'input': os.path.join(os.getcwd(),"..", 'resources/others/input.png'),
    'appear': os.path.join(os.getcwd(),"..", 'resources/others/appear.png'),
    'background': os.path.join(os.getcwd(),"..", 'resources/others/background.png'),
    'boom_dynamic': os.path.join(os.getcwd(),"..", 'resources/others/boom_dynamic.png'),
    'boom_static': os.path.join(os.getcwd(),"..", 'resources/others/boom_normal.png'),
    'gameover': os.path.join(os.getcwd(),"..", 'resources/others/gameover.png'),
    'logo': os.path.join(os.getcwd(),"..", 'resources/others/logo.png'),
    'tip': os.path.join(os.getcwd(),"..", 'resources/others/tip.png'),
    'loadbar': os.path.join(os.getcwd(),"..", 'resources/others/gamebar.png')
}
TANK_IMAGE = {
    # player tank
    'player1': os.path.join(os.getcwd(),"..", 'resources/tank/tank_T1_0.png'),
    'player2': os.path.join(os.getcwd(),"..", 'resources/tank/tank_T2_0.png'),

    # enemy tank
    '0': [os.path.join(os.getcwd(),"..", 'resources/tank/enemy_1_0.png'),
          os.path.join(os.getcwd(),"..", 'resources/tank/enemy_1_1.png'),
          os.path.join(os.getcwd(),"..", 'resources/tank/enemy_1_2.png'),
          os.path.join(os.getcwd(),"..", 'resources/tank/enemy_1_3.png')],
    '1': [os.path.join(os.getcwd(),"..", 'resources/tank/enemy_2_0.png'),
          os.path.join(os.getcwd(),"..", 'resources/tank/enemy_2_1.png'),
          os.path.join(os.getcwd(),"..", 'resources/tank/enemy_2_2.png'),
          os.path.join(os.getcwd(),"..", 'resources/tank/enemy_2_3.png')],
    '2': [os.path.join(os.getcwd(),"..", 'resources/tank/enemy_3_0.png'),
          os.path.join(os.getcwd(),"..", 'resources/tank/enemy_3_1.png'),
          os.path.join(os.getcwd(),"..", 'resources/tank/enemy_3_2.png'),
          os.path.join(os.getcwd(),"..", 'resources/tank/enemy_3_3.png')],
}

BULLET_IMAGE = {
    (0, 1): os.path.join(os.getcwd(),"..", 'resources/bullet/bullet_down.png'),
    (1, 0): os.path.join(os.getcwd(),"..", 'resources/bullet/bullet_right.png'),
    (0, -1): os.path.join(os.getcwd(),"..", 'resources/bullet/bullet_up.png'),
    (-1, 0): os.path.join(os.getcwd(),"..", 'resources/bullet/bullet_left.png')
}

SCENE_IMAGE = {
    'brick': os.path.join(os.getcwd(),"..", 'resources/scene/brick.png'),
    'iron': os.path.join(os.getcwd(),"..", 'resources/scene/iron.png'),
    'river1': os.path.join(os.getcwd(),"..", 'resources/scene/river1.png'),
    'river2': os.path.join(os.getcwd(),"..", 'resources/scene/river2.png'),
    'tree': os.path.join(os.getcwd(),"..", 'resources/scene/tree.png')
}

HOME_IMAGE = [os.path.join(os.getcwd(),"..", 'resources/home/home1.png'),
              os.path.join(os.getcwd(),"..", 'resources/home/home_destroyed.png')]


# 音乐
AUDIO = {
    'add': os.path.join(os.getcwd(),"..", 'resources/audios/add.wav'),
    'bang': os.path.join(os.getcwd(),"..", 'resources/audios/bang.wav'),
    'shoot': os.path.join(os.getcwd(), "..",'resources/audios/fire.wav'),
    'start': os.path.join(os.getcwd(), "..",'resources/audios/start.wav')
}



