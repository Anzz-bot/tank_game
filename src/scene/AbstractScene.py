'''
 * @Author: alexander.huang
 * @Date:   2022-05-27 18:12:11
 * @Last Modified by: alexander.huang
 * @Last Modified time: 2022-06-1 21:40:51
'''
from src.manager.GameManager import GameManager


class AbstractScene:
    def __init__(self):
        self._load_resources()
        self._load_logo()

    @property
    def config(self):
        return GameManager().config

    def _load_resources(self):
        pass

    def _load_logo(self):
        pass

    def _load_tips(self):
        pass

    def _load_bottons(self):
        pass

    def _game_loop(self):
        pass

    def _draw_interface(self):
        pass

    def show(self):
        GameManager().load_screen()
        self._load_tips()
        self._load_bottons()
        self._game_loop()

