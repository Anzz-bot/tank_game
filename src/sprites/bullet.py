import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, direction, position, config, tank, speed=8):
        super().__init__()
        self.image = pygame.image.load(config.BULLET_IMAGE.get(direction.value))
        self.width = config.SCREEN_WIDTH
        self.height = config.SCREEN_HEIGHT
        self.border_len = config.BORDER_LEN
        self.direction = direction
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.center = position
        self.speed = speed
        self.tank = tank

    def move(self):
        self.rect = self.rect.move(self.direction.value[0] * self.speed, self.direction.value[1] * self.speed)
        return (self.rect.top < self.border_len) or (self.rect.bottom > self.height) or \
               (self.rect.left < self.border_len) or (self.rect.right > self.width)

    def kill(self):
        super().kill()
        self.tank.bullet_count -= 1
        # self.tank.bullet_cooling = False
