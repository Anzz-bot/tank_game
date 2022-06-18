import pygame
from src.sprites.bullet import Bullet
from src.uiutil import DIRECTION, COLLISION
from pygame.sprite import spritecollide


class Tank(pygame.sprite.Sprite):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.tank_image = None

        self.speed = 8
        self.life = 0

        self.switch_time = 1
        self.switch_count = 0
        self.switch_flag = False

        self.cache_time = 4
        self.cache_count = 0

        self.bullet_cooling = False
        self.bullet_count = 0
        self.__bullet_limit = 1

        self.boom_flag = False
        self.boom_time = 5
        self.boom_count = 0

        self.border_len = config.BORDER_LEN
        self.screen_size = [config.SCREEN_WIDTH, config.SCREEN_HEIGHT]
        self._load_resources()

    @property
    def bullet_limit(self):
        return self.__bullet_limit

    @property
    def image(self):
        if self.boom_flag:
            return self.boom_image
        return self.tank_direction_image.subsurface((48*int(self.switch_flag), 0), (48,48))

    def load_tank_image(self, image):
        self.tank_image = pygame.image.load(image).convert_alpha()

    def _load_resources(self):
        self.bullet_image = self.config.BULLET_IMAGE
        self.boom_image = pygame.image.load(self.config.IMAGE.get('boom_static'))

    def _update_direction(self, direction):
        self.direction = direction
        if self.direction == DIRECTION.UP:
            self.tank_direction_image = self.tank_image.subsurface((0, 0), (96, 48))
        elif self.direction == DIRECTION.DOWN:
            self.tank_direction_image = self.tank_image.subsurface((0, 48), (96, 48))
        elif self.direction == DIRECTION.LEFT:
            self.tank_direction_image = self.tank_image.subsurface((0, 96), (96, 48))
        elif self.direction == DIRECTION.RIGHT:
            self.tank_direction_image = self.tank_image.subsurface((0, 144), (96, 48))

    def roll(self):
        self.switch_count += 1
        if self.switch_count > self.switch_time:
            self.switch_count = 0
            self.switch_flag = not self.switch_flag

    def move(self, direction, scene_elements, player_group, enemy_group, home):
        if self.boom_flag:
            return
        if self.direction != direction:
            self._update_direction(direction)
            self.switch_count = self.switch_time
            self.cache_count = self.cache_time

        self.cache_count += 1
        if self.cache_count < self.cache_time:
            return
        self.cache_count = 0

        new_position = (self.direction.value[0] * self.speed, self.direction.value[1]*self.speed)
        old_rect = self.rect
        self.rect = self.rect.move(new_position)
        collision = 0
        cannot_pass = [scene_elements.brick_group, scene_elements.iron_group, scene_elements.river_group]
        for element in cannot_pass:
            if spritecollide(self, element, False, None):
                self.rect = old_rect
                collision |= COLLISION.WITH_SCENE_ELEMENTS

        if spritecollide(self, player_group, False, None) or spritecollide(self, enemy_group, False, None):
            collision |= COLLISION.WITH_TANK
            self.rect = old_rect

        if pygame.sprite.collide_rect(self, home):
            collision |= COLLISION.WITH_HOME
            self.rect = old_rect

        if self.rect.left < self.border_len:
            self.rect.left = self.border_len
            collision |= COLLISION.WITH_BORDER
        elif self.rect.right > self.screen_size[0] - self.border_len:
            collision |= COLLISION.WITH_BORDER
            self.rect.right = self.screen_size[0] - self.border_len
        elif self.rect.top < self.border_len:
            collision |= COLLISION.WITH_BORDER
            self.rect.top = self.border_len
        elif self.rect.bottom > self.screen_size[1] - self.border_len:
            collision |= COLLISION.WITH_BORDER
            self.rect.bottom = self.screen_size[1] - self.border_len

        return collision

    def shoot(self):
        if self.boom_flag:
            return False
        if not self.bullet_cooling:
            if self.bullet_count >= self.bullet_limit:
                return False
            else:
                self.bullet_count += 1
            self.bullet_cooling = True
            position = (self.rect.centerx + self.direction.value[0], self.rect.centery + self.direction.value[1])
            bullet = Bullet(direction=self.direction, position=position,tank=self,config=self.config)
            return bullet
        return False










