'''
 * @Author: alexander.huang
 * @Date:   2022-05-27 18:12:11
 * @Last Modified by: alexander.huang
 * @Last Modified time: 2022-06-1 21:40:51
'''
import random
from enum import Enum


class DIRECTION(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @classmethod
    def random(cls):
        return random.choice([DIRECTION.DOWN, DIRECTION.LEFT, DIRECTION.RIGHT, DIRECTION.UP])

    @classmethod
    def list(cls):
        return [DIRECTION.UP, DIRECTION.DOWN, DIRECTION.LEFT, DIRECTION.RIGHT]


class COLLISION:
    WITH_HOME = 0b00010
    WITH_TANK = 0b00001
    WITH_BORDER = 0b00100
    WITH_SCENE_ELEMENTS = 0b01000


class AutoName(Enum):
    @classmethod
    def random(cls):
        return random.choice(['Julia', 'Jonathan', 'Jack', 'Kevin', 'Nick', 'Mike', 'Handsome Boy', 'Pretty Girl'])
