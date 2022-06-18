'''
 * @Author: alexander.huang
 * @Date:   2022-05-27 18:12:11
 * @Last Modified by: alexander.huang
 * @Last Modified time: 2022-06-1 21:40:51
'''
import sys
import pygame
from src.manager.GameManager import GameManager
from src.scene.AbstractScene import AbstractScene


class GameLoadScene(AbstractScene):

    def _load_resources(self):
        config = self.config
        self.loadbar = pygame.image.load(config.IMAGE.get('loadbar')).convert_alpha()
        self.background = pygame.image.load(config.IMAGE.get('background'))
        self.logo_img = pygame.image.load(config.IMAGE.get('logo'))
        self.logo_img = pygame.transform.scale(self.logo_img, (450, 70))
        self.font = pygame.font.Font(config.FONT, config.SCREEN_WIDTH // 20)
        self.tank_cursor = pygame.image.load(
            config.TANK_IMAGE.get('1')[0]
        ).convert_alpha().subsurface((0, 144), (48, 48))

    def _load_tips(self):
        config = self.config
        self.font_render = self.font.render(
            'LEVEL%d' % (GameManager().level+1),
            True,
            (0, 220, 0)
        )
        self.font_rect = self.font_render.get_rect()
        self.font_rect.centerx, self.font_rect.centery = config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2

    def _load_logo(self):
        self.logo_rect = self.logo_img.get_rect()
        self.logo_rect.centerx, self.logo_rect.centery = self.config.SCREEN_WIDTH / 2, self.config.SCREEN_HEIGHT // 4

    def _load_bar(self):
        config = self.config
        self.loadbar_rect = self.loadbar.get_rect()
        self.loadbar_rect.centerx, self.loadbar_rect.centery = config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 1.6
        self.tank_rect = self.tank_cursor.get_rect()
        self.tank_rect.left = self.loadbar_rect.left
        self.tank_rect.centery = self.loadbar_rect.centery

    def _draw_interface(self):
        screen = GameManager().screen
        screen.blit(self.background, (0, 0))
        screen.blit(self.logo_img, self.logo_rect)
        screen.blit(self.font_render, self.font_rect)
        screen.blit(self.loadbar, self.loadbar_rect)
        screen.blit(self.tank_cursor, self.tank_rect)
        pygame.draw.rect(screen, (0, 160, 0), (
            self.loadbar_rect.left + 8,
            self.loadbar_rect.top + 8,
            self.tank_rect.left - self.loadbar_rect.left - 8,
            self.tank_rect.bottom - self.loadbar_rect.top - 16
        ))
        self.tank_rect.left += 8

    def _game_loop(self):
        load_time = self.loadbar_rect.right - self.tank_rect.right + 8
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if load_time <= 0:
                return
            self._draw_interface()
            load_time -= 8
            pygame.display.update()
            clock.tick(60)

    def show(self):
        self._load_bar()
        super().show()



