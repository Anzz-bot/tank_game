from src.sprites.tank import Tank
from src.uiutil import DIRECTION
import pygame


class PlayerTank(Tank):
    def __init__(self, name, position, config):
        super().__init__(config=config)
        # print(self.config.TANK_IMAGE.get(name))
        self.name = name
        self.nick = None
        self.nickname = None
        self.nickname_rect = None
        self.font = pygame.font.Font(config.FONT, config.SCREEN_HEIGHT // 36)
        self.load_tank_image(self.config.TANK_IMAGE.get(name))
        self.init_direction = DIRECTION.UP
        self.init_position = position

        self.life = 3
        self._reborn()

    def set_nickname(self, nick):
        self.nick = nick
        self.nickname = self.font.render(self.nick, True, (0, 255, 0))

    def update_nickname(self):
        self.nickname_rect = self.nickname.get_rect()
        self.nickname_rect.centerx = self.rect.centerx
        self.nickname_rect.centery = self.rect.centery - 35

    def _load_resources(self):
        super()._load_resources()

    def update(self):
        if self.bullet_cooling:
            self.bullet_cooling_count += 1
            if self.bullet_cooling_count >= self.bullet_time:
                self.bullet_cooling_count = 0
                self.bullet_cooling = False

        if self.boom_flag:
            self.boom_count += 1
            if self.boom_count > self.boom_time:
                self.boom_count = 0
                self.boom_flag = False
                self._reborn()

    def decrease_life(self):
        if self.boom_flag:
            return False
        self.boom_flag = True
        self.life -= 1
        return True

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.nickname, self.nickname_rect)

    def _reborn(self):
        # print(self.life)
        self.bullet_cooling = False
        self.bullet_time = 30
        self.bullet_cooling_count = 0
        self._update_direction(self.init_direction)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.init_position

