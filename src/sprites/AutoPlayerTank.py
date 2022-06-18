import random
from src.sprites.PlayerTank import PlayerTank
from src.uiutil import DIRECTION, COLLISION


class AutoPlayerTank(PlayerTank):
    Protection_Wall_Top = 603
    Protection_Wall_Bottom = 555
    Protection_Wall_Left = 267
    Protection_Wall_Right = 339

    def __init__(self, name, position, config):
        super().__init__(name, position, config)
        self.change_direction_flag = False
        self.change_direction_time = 60
        self.change_direction_count = 0

    def shoot_strategy(self):
        if self.rect.bottom >= self.Protection_Wall_Top:
            if self.rect.left >= self.Protection_Wall_Right and self.direction == DIRECTION.LEFT:
                return False
            if self.rect.right <= self.Protection_Wall_Left and self.direction == DIRECTION.RIGHT:
                print(self.rect.right, self.rect.centery)
                return False
            if self.rect.left >= self.Protection_Wall_Left and self.rect.right <= self.Protection_Wall_Right \
                    and self.direction == DIRECTION.DOWN:
                return False

        return True

    def auto_update(self, scene_elements, enemy_group, home):
        bullet = None

        if self.boom_flag:
            self.boom_count += 1
            if self.boom_count > self.boom_time:
                self.boom_count = 0
                self.boom_flag = False
                self._reborn()
            return bullet

        self.move(self.direction, scene_elements, enemy_group, enemy_group, home)
        self.roll()
        if self.bullet_cooling:
            self.bullet_cooling_count += 1
            if self.bullet_cooling_count >= self.bullet_time:
                self.bullet_cooling_count = 0
                self.bullet_cooling = False
        if self.shoot_strategy():
            bullet = self.shoot()
        return bullet

    def change_direction(self, current_direction=False):
        direction_list = DIRECTION.list()
        if current_direction:
            direction_list.remove(self.direction)

        self._update_direction(random.choice(direction_list))

    def move(self, direction, scene_elements, player_group, enemy_group, home):
        if self.change_direction_flag:
            direction = random.choices(DIRECTION.list(), weights=[16, 8, 13, 13])[0]
            self.change_direction_flag = False
            self.change_direction_count = 0
        else:
            self.change_direction_count += 1
            if self.change_direction_count >= self.change_direction_time:
                self.change_direction_flag = True

        collisions = super().move(direction, scene_elements, player_group, enemy_group, home)
        if collisions is None or collisions == 0:
            return
        change_direction = False
        if collisions & COLLISION.WITH_BORDER:
            change_direction = True
        self.change_direction(change_direction)
