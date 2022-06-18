'''
 * @Author: alexander.huang
 * @Date:   2022-05-27 18:12:11
 * @Last Modified by: alexander.huang
 * @Last Modified time: 2022-06-1 21:40:51
'''
from src.elements import *


class SceneElementFactory(object):
    BRICK = 'brick'
    IRON = 'iron'
    RIVER_1 = 'river1'
    RIVER_2 = 'river2'
    ICE = 'ice'
    TREE = 'tree'
    SCENE_MAPS = {
        BRICK: Brick,
        IRON: Iron,
        RIVER_1: River,
        RIVER_2: River,
        TREE: Tree,
        # ICE: Ice,
    }

    def __init__(self, config):
        self.__scene_images = config.SCENE_IMAGE

    def create_element(self, position, element_type):
        # print(element_type)
        # print(self.__scene_images.get(element_type))
        return SceneElementFactory.SCENE_MAPS[element_type](position, self.__scene_images.get(element_type))
