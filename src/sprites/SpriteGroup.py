import pygame
from src.sprites.PlayerTank import PlayerTank
from src.sprites.AutoPlayerTank import AutoPlayerTank
from src.sprites.EnemyTank import EnemyTank
from src.sprites.bullet import Bullet


class SpriteGroup(object):
    def __init__(self):
        self.player_tanks = pygame.sprite.Group()
        self.enemy_tanks = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

    def add(self, sprite):
        if isinstance(sprite, PlayerTank):
            self.player_tanks.add(sprite)
        elif isinstance(sprite, EnemyTank):
            self.enemy_tanks.add(sprite)
        elif isinstance(sprite, Bullet):
            if isinstance(sprite.tank, PlayerTank):
                self.player_bullets.add(sprite)
            elif isinstance(sprite.tank, EnemyTank):
                self.enemy_bullets.add(sprite)

    def remove(self, sprite):
        if isinstance(sprite, PlayerTank):
            self.player_tanks.remove(sprite)
        elif isinstance(sprite, EnemyTank):
            self.enemy_tanks.remove(sprite)
        elif isinstance(sprite, Bullet):
            if isinstance(sprite.tank, PlayerTank):
                self.player_bullets.remove(sprite)
            elif isinstance(sprite.tank, EnemyTank):
                self.enemy_bullets.remove(sprite)

    def update(self, scene_elements, home):
        for bullet in self.player_bullets:
            if bullet.move():
                bullet.kill()

        for bullet in self.enemy_bullets:
            if bullet.move():
                bullet.kill()

        # player坦克
        for tank in self.player_tanks:
            if isinstance(tank, AutoPlayerTank):
                bullet = tank.auto_update(scene_elements, self.enemy_tanks, home)
                if isinstance(bullet, Bullet):
                    self.add(bullet)
            else:
                tank.update()
            tank.update_nickname()

        for tank in self.enemy_tanks:
            self.remove(tank)
            remove_flag, bullet = tank.update(scene_elements, self.player_tanks, self.enemy_tanks, home)
            # print('sprite group')
            # print(remove_flag, bullet)
            self.add(tank)
            if isinstance(bullet, Bullet):
                self.add(bullet)
            if remove_flag:
                self.remove(tank)

    def draw(self, screen, layer):
        if layer == 1:
            self.player_bullets.draw(screen)
            self.enemy_bullets.draw(screen)
            # self.player_tanks.draw(screen)
            for tank in self.player_tanks:
                tank.draw(screen)
            self.enemy_tanks.draw(screen)
