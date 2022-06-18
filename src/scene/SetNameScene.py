'''
 * @Author: alexander.huang
 * @Date:   2022-05-27 18:12:11
 * @Last Modified by: alexander.huang
 * @Last Modified time: 2022-06-1 21:40:51
'''
import sys
import pygame
from pygame_textinput import TextInputVisualizer, TextInputManager
from src.manager.GameManager import GameManager
from src.scene.AbstractScene import AbstractScene


class SetNameScene(AbstractScene):

    def _load_resources(self):
        config = self.config
        self.background = pygame.image.load(config.IMAGE.get('background'))
        self.logo = pygame.transform.scale(
            pygame.image.load(config.IMAGE.get('logo')),
            (450, 70))
        self.font = pygame.font.Font(config.FONT, config.FONT_SIZE)
        self.__init_textbox()

    def __init_textbox(self):
        config = self.config
        self.input_img = pygame.transform.scale(
            pygame.image.load(config.IMAGE.get('input')),
            (500, 70))
        self.input_rect = self.input_img.get_rect()
        self.input_rect.centerx, self.input_rect.top = config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2
        self.manager = TextInputManager(validator=lambda input: len(input) <= 25)
        self.textbox = TextInputVisualizer(manager=self.manager, antialias=True, font_object=self.font)
        self.textbox.cursor_width = 3
        self.textbox.cursor_blink_interval = 500  # blinking interval in ms
        self.textbox.font_color = (0, 85, 170)
        self.textbox_pos = (self.input_rect.left + 18, self.input_rect.top + 15)

    def _load_logo(self):
        config = self.config
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.centerx, self.logo_rect.centery = config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 4

    def _load_tips(self):
        config = self.config
        self.tips = self.font.render('请输入坦克名字: ', True, config.NORMAL)
        self.tips_rect = self.tips.get_rect()
        self.tips_rect.centerx, self.tips_rect.top = config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2.5

        self.tip = self.font.render('请按 <Enter> 确认 !', True, (0, 220, 0))
        self.tip_rect = self.tip.get_rect()
        self.tip_rect.centerx, self.tip_rect.top = config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 1.4

    def _draw_interface(self):
        screen = GameManager().screen

        screen.blit(self.background, (0, 0))
        screen.blit(self.logo, self.logo_rect)

        screen.blit(self.tips, self.tips_rect)
        screen.blit(self.input_img, self.input_rect)
        screen.blit(self.textbox.surface, self.textbox_pos)
        self.textbox.font_color = [(c + 10) % 255 for c in self.textbox.font_color]
        if self.tip_flag:
            screen.blit(self.tip, self.tip_rect)

    def _game_loop(self):
        tip_flash_count = 0
        tip_flash_time = 15
        self.tip_flag = True
        clock = pygame.time.Clock()
        while True:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    GameManager().player_name = self.textbox.value
                    return

            tip_flash_count += 1
            if tip_flash_count > tip_flash_time:
                tip_flash_count = 0
                self.tip_flag = not self.tip_flag

            self.textbox.update(events)
            self._draw_interface()
            pygame.display.update()
            clock.tick(30)

