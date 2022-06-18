'''
 * @Author: alexander.huang
 * @Date:   2022-05-27 18:12:11
 * @Last Modified by: alexander.huang
 * @Last Modified time: 2022-06-1 21:40:51
'''
from src import config
from src.manager.GameManager import GameManager

if __name__ == '__main__':
    # print(config.AUDIO.items())
    gamectrl = GameManager(config)
    gamectrl.start()
