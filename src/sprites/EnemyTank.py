import random
import pygame
from src.sprites.tank import Tank
from src.uiutil import DIRECTION, COLLISION
from src.manager import GameManager


class EnemyTank(Tank):
    def __init__(self, position, config):
        super().__init__(config)
        level_images = self.config.TANK_IMAGE
        self.tank_type = random.choices(['0', '1', '2'], weights=[10, 10, GameManager().difficulty+GameManager().level+10])[0]
        self.level_image = level_images.get(self.tank_type)

        self.level = int(self.tank_type)
        self.speed = 8 - self.level*3 + 2*GameManager().difficulty

        self.bullet_cooling_time = 100 - self.level*10 - GameManager().difficulty*10
        self.bullet_cooling_count = 0

        self.born_flag = True
        self.born_time = 90
        self.stop_flag = False
        self.stop_count = 0
        self.stop_time = 100

        appear_image = pygame.image.load(self.config.IMAGE.get('appear')).convert_alpha()
        self.appear_images = [
            appear_image.subsurface((0, 0), (48, 48)),
            appear_image.subsurface((48, 0), (48, 48)),
            appear_image.subsurface((96, 0), (48, 48))
        ]

        self.tank_image = pygame.image.load(self.level_image[self.level])
        self._update_direction(DIRECTION.random())
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position

    @property
    def image(self):
        if self.born_flag:
            return self.appear_images[(90 - self.born_time//10) % 3]
        return super().image

    def update(self, scene_elements, player_group, enemy_group, home):
        remove_flag = False
        bullet = None

        if self.boom_flag:
            self.boom_count += 1
            if self.boom_count > self.boom_time:
                self.boom_count = 0
                self.boom_flag = False
                remove_flag = True
            return remove_flag, bullet

        if self.stop_flag:
            self.stop_count += 1
            if self.stop_count > self.stop_time:
                self.stop_flag = False
                self.stop_count = 0
            return remove_flag, bullet

        if self.born_flag:
            self.born_time -= 1
            if self.born_time < 0:
                self.born_flag = False
        else:
            self.move(self.direction, scene_elements, player_group, enemy_group, home)
            self.roll()
            if self.bullet_cooling:
                self.bullet_cooling_count += 1
                if self.bullet_cooling_count >= self.bullet_cooling_time:
                    self.bullet_cooling_count = 0
                    self.bullet_cooling = False
            bullet = self.shoot()
        # print('enemy')
        return remove_flag, bullet

    def decrease_level(self):
        if self.boom_flag:
            return False
        self.level -= 1
        self.tank_image = pygame.image.load(self.level_image[self.level]).convert_alpha()
        self._update_direction(self.direction)
        if self.level < 0:
            self.boom_flag = True
        return self.level < 0

    def change_direction(self, current_direction=False):
        direction_list = DIRECTION.list()
        if current_direction:
            direction_list.remove(self.direction)

        self._update_direction(random.choice(direction_list))

    def move(self, direction, scene_elements, player_group, enemy_group, home):
        collisions = super().move(direction, scene_elements, player_group, enemy_group, home)

        if collisions is None or collisions == 0:
            return
        change_direction = False
        if collisions & COLLISION.WITH_SCENE_ELEMENTS & COLLISION.WITH_BORDER:
            change_direction = True
        self.change_direction(change_direction)

    def set_stop(self):
        self.stop_flag = True





