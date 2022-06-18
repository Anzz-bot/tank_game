import pygame
from src.elements import *


class SceneElementGroup(object):
    def __init__(self):
        self.brick_group = pygame.sprite.Group()
        self.iron_group = pygame.sprite.Group()
        self.tree_group = pygame.sprite.Group()
        self.river_group = pygame.sprite.Group()

    def add(self, scene_element):
        if isinstance(scene_element, Brick):
            self.brick_group.add(scene_element)
        elif isinstance(scene_element, Iron):
            self.iron_group.add(scene_element)
        elif isinstance(scene_element, Tree):
            self.tree_group.add(scene_element)
        elif isinstance(scene_element, River):
            self.river_group.add(scene_element)

    def draw(self, screen, layer):
        if layer == 1:
            self.river_group.draw(screen)
            self.brick_group.draw(screen)
            self.iron_group.draw(screen)
        elif layer == 2:
            self.tree_group.draw(screen)