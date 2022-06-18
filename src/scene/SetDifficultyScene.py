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


class SetDifficultyScene(AbstractScene):

    def _load_resources(self):

        config = self.config
        self.background = pygame.image.load(config.IMAGE.get('background'))
        self.logo = pygame.transform.scale(
            pygame.image.load(config.IMAGE.get('logo')),
            (450, 70))
        self.cursor = pygame.image.load(
            config.TANK_IMAGE.get('player1')
        ).convert_alpha().subsurface((0, 144), (48, 48))
        self.font = pygame.font.Font(config.FONT, config.FONT_SIZE)
        self.mode = 0

    def _load_logo(self):
        config = self.config
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.centerx, self.logo_rect.centery = config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 4

    def _load_tips(self):
        config = self.config
        self.easy_normal = self.font.render('简单', True, config.NORMAL)
        self.easy_hover = self.font.render('简单', True, config.HOVER)
        self.easy_rect = self.easy_normal.get_rect()
        self.easy_rect.left, self.easy_rect.top = config.SCREEN_WIDTH / 2.35, config.SCREEN_HEIGHT / 2.5

        self.sample_normal = self.font.render('普通', True, config.NORMAL)
        self.sample_hover = self.font.render('普通', True, config.HOVER)
        self.sample_rect = self.sample_normal.get_rect()
        self.sample_rect.left, self.sample_rect.top = config.SCREEN_WIDTH / 2.35, config.SCREEN_HEIGHT / 2

        self.difficult_normal = self.font.render('困难', True, config.NORMAL)
        self.difficult_hover = self.font.render('困难', True, config.HOVER)
        self.difficult_rect = self.difficult_normal.get_rect()
        self.difficult_rect.left, self.difficult_rect.top = config.SCREEN_WIDTH / 2.35, config.SCREEN_HEIGHT / 1.65

        self.cursor_rect = self.cursor.get_rect()

        self.tip = self.font.render('请按 <Enter> 开始 !', True, config.NORMAL)
        self.tip_rect = self.tip.get_rect()
        self.tip_rect.centerx, self.tip_rect.top = config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 1.3

    def _game_loop(self):
        tip_flash_count = 0
        tip_flash_time = 30
        self.tip_flag = True
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        GameManager().difficulty = self.mode
                        return
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        if self.mode == 0:
                            self.mode = 2
                        else:
                            self.mode -= 1
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        if self.mode == 2:
                            self.mode = 0
                        else:
                            self.mode += 1
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.mode == 0:
                self.cursor_rect.right, self.cursor_rect.top = self.easy_rect.left - 10, self.easy_rect.top - 10
            elif self.mode == 1:
                self.cursor_rect.right, self.cursor_rect.top = self.sample_rect.left - 10, self.sample_rect.top - 10
            else:
                self.cursor_rect.right, self.cursor_rect.top = self.difficult_rect.left - 10, self.difficult_rect.top - 10
            tip_flash_count += 1
            if tip_flash_count > tip_flash_time:
                tip_flash_count = 0
                self.tip_flag = not self.tip_flag

            self._draw_interface()
            pygame.display.update()
            clock.tick(60)

    def _draw_interface(self):
        screen = GameManager().screen
        screen.blit(self.background, (0, 0))
        screen.blit(self.logo, self.logo_rect)
        if self.tip_flag:
            screen.blit(self.tip, self.tip_rect)

        screen.blit(self.cursor, self.cursor_rect)

        if self.mode == 0:
            screen.blit(self.easy_hover, self.easy_rect)
            screen.blit(self.sample_normal, self.sample_rect)
            screen.blit(self.difficult_normal, self.difficult_rect)
        elif self.mode == 1:
            screen.blit(self.easy_normal, self.easy_rect)
            screen.blit(self.sample_hover, self.sample_rect)
            screen.blit(self.difficult_normal, self.difficult_rect)
        else:
            screen.blit(self.easy_normal, self.easy_rect)
            screen.blit(self.sample_normal, self.sample_rect)
            screen.blit(self.difficult_hover, self.difficult_rect)
