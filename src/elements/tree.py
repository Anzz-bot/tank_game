'''
 * @Author: alexander.huang
 * @Date:   2022-05-27 18:12:11
 * @Last Modified by: alexander.huang
 * @Last Modified time: 2022-06-1 21:40:51
'''
from src.elements.SceneElements import SceneElement


class Tree(SceneElement):
    # 树
    def __init__(self, position,  image):
        super().__init__(position, image, True)
