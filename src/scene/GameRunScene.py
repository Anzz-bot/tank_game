'''
 * @Author: alexander.huang
 * @Date:   2022-05-27 18:12:11
 * @Last Modified by: alexander.huang
 * @Last Modified time: 2022-06-1 21:40:51
'''
import sys
import random
import pygame
from src.factory import *
from src.elements import *
from src.uiutil import DIRECTION
from src.scene.AbstractScene import AbstractScene
from src.manager.GameManager import GameManager
from src.sprites.SpriteGroup import SpriteGroup
from src.sprites.SceneElementGroup import SceneElementGroup
from pygame.sprite import groupcollide, spritecollide


class GameRunScene(AbstractScene):

    def _load_resources(self):
        config = self.config
        self.tank_factory = TankFactory(self.config)
        self.scene_factory = SceneElementFactory(self.config)
        self.sprites = SpriteGroup()

        self.music = GameManager().music
        self.home_image = config.HOME_IMAGE
        self.grid_size = config.GRID_SIZE
        self.border_len = config.BORDER_LEN
        self.background = pygame.image.load(config.IMAGE.get('background'))
        self.font = pygame.font.Font(config.FONT, config.SCREEN_HEIGHT // 36)
        self.grid_size = config.GRID_SIZE

        self.scene_elements = SceneElementGroup()
        self.win_flag = False
        self.over_flag = False
        self.has_next_loop = True

    def __load_tanks(self):
        self.__tank_player1 = self.tank_factory.create_tank(self.__player_point[0], TankFactory.PLAYER1_TANK)
        self.sprites.add(self.__tank_player1)
        self.__tank_player2 = None
        if GameManager().double_mode:
            self.__tank_player2 = self.tank_factory.create_tank(self.__player_point[1], TankFactory.PLAYER2_TANK)
            self.sprites.add(self.__tank_player2)
        for position in self.__enemy_point:
            self.sprites.add(self.tank_factory.create_tank(position, TankFactory.ENEMY_TANK))


    def load_game_screen(self):
        GameManager().load_screen(
            (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT)
        )

    def __load_collision(self):
        self.collision = {
            'elements': {
                'PlayerBulletWithBrick': (self.sprites.player_bullets, self.scene_elements.brick_group, True, True),
                'EnemyBulletWithBrick': (self.sprites.enemy_bullets, self.scene_elements.brick_group, True, True),
                'EnemyBulletWithIron': (self.sprites.enemy_bullets, self.scene_elements.iron_group, True, False),
                'BulletWithBullet': (self.sprites.player_bullets, self.sprites.enemy_bullets, True, True),
            },
            'home': {
                'PlayerBulletWithHome': (self.__home, self.sprites.player_bullets, True, None),
                'EnemyBulletWithHome': (self.__home, self.sprites.enemy_bullets, True, None),

            },
            'bullets': {
                'PlayerTankWithEnemyBullet': (self.sprites.player_tanks, self.sprites.enemy_bullets, True, None),
                'EnemyTankWithPlayerBullet': (self.sprites.enemy_tanks, self.sprites.player_bullets, True, None),
            }

        }

    def __load_event(self):
        self.__generate_enemies_event = pygame.constants.USEREVENT
        pygame.time.set_timer(self.__generate_enemies_event, 20000)

    def __load_game(self):
        elements_map = {
            'B': SceneElementFactory.BRICK,
            'I': SceneElementFactory.IRON,
            'T': SceneElementFactory.TREE,
            'R': SceneElementFactory.RIVER_1,
            'C': SceneElementFactory.ICE,
        }

        home_position = ()
        home_protection_position = []

        f = open(GameManager().game_file)
        num_row = -1
        for line in f.readlines():
            line = line.strip('\n')
            if line.startswith('#') or (not line):
                continue
            elif line.startswith('%TOTALENEMYNUM'):
                self.total_enemy_num = 20 + GameManager().level
            elif line.startswith('%MAXENEMYNUM'):
                self.max_enemy_num = 6 + GameManager().level
            elif line.startswith('%HOMEPOS'):
                home_position = line.split(':')[-1]
                home_position = [
                    int(home_position.split(',')[0]), int(home_position.split(',')[1])
                ]
                home_position = (
                    self.border_len + home_position[0] * self.grid_size,
                    self.border_len + home_position[1] * self.grid_size
                )
            # home周围
            elif line.startswith('%HOMEAROUNDPOS'):
                home_protection_position = line.split(':')[-1]
                home_protection_position = [
                    [
                        int(pos.split(',')[0]), int(pos.split(',')[1])
                    ] for pos in home_protection_position.split(' ')
                ]
                home_protection_position = [
                    (
                        self.border_len + pos[0] * self.grid_size, self.border_len + pos[1] * self.grid_size
                    ) for pos in home_protection_position
                ]
            # 我方坦克初始位置
            elif line.startswith('%PLAYERTANKPOS'):
                self.__player_point = line.split(':')[-1]
                self.__player_point = [
                    [
                        int(pos.split(',')[0]), int(pos.split(',')[1])
                    ] for pos in self.__player_point.split(' ')
                ]
                self.__player_point = [
                    (self.border_len + pos[0] * self.grid_size, self.border_len + pos[1] * self.grid_size
                     ) for pos in self.__player_point
                ]
            # 敌方坦克初始位置
            elif line.startswith('%ENEMYTANKPOS'):
                self.__enemy_point = line.split(':')[-1]
                self.__enemy_point = [
                    [
                        int(pos.split(',')[0]), int(pos.split(',')[1])
                    ] for pos in self.__enemy_point.split(' ')
                ]
                self.__enemy_point = [
                    (
                        self.border_len + pos[0] * self.grid_size, self.border_len + pos[1] * self.grid_size
                    ) for pos in self.__enemy_point
                ]
                # 地图元素
            else:
                num_row += 1
                for num_col, elem in enumerate(line.split(' ')):
                    position = self.border_len + num_col * self.grid_size, self.border_len + num_row * self.grid_size

                    scene_element = None
                    if elem in elements_map:
                        scene_element = self.scene_factory.create_element(position, elements_map[elem])
                    elif elem == 'R':
                        scene_element = self.scene_factory.create_element(
                            position, random.choice([SceneElementFactory.RIVER_1, SceneElementFactory.RIVER_2])
                        )
                    if scene_element is not None:
                        self.scene_elements.add(scene_element)
        self.__home = Home(position=home_position, image=self.home_image, protection_position=home_protection_position)

    def play_music(self, music):
        self.music[music].play()

    def dispatch_player_operation(self):
        key_press = pygame.key.get_pressed()
        key_map = {
            'direction': {
                self.__tank_player1: {
                    pygame.K_UP: DIRECTION.UP,
                    pygame.K_DOWN: DIRECTION.DOWN,
                    pygame.K_LEFT: DIRECTION.LEFT,
                    pygame.K_RIGHT: DIRECTION.RIGHT
                }
            },
            'shoot': {
                self.__tank_player1: pygame.K_SPACE,
            }
        }
        player_tank_list = []
        if self.__tank_player1.life >= 0:
            player_tank_list.append(self.__tank_player1)
        # if GameManager().double_mode and self.__tank_player2.life >= 0:
        #     player_tank_list.append(self.__tank_player2)

        for tank in player_tank_list:
            for key, direction in key_map['direction'][tank].items():
                if key_press[key]:
                    self.sprites.remove(tank)
                    tank.move(direction, self.scene_elements, self.sprites.player_tanks, self.sprites.enemy_tanks, self.__home)
                    tank.roll()
                    self.sprites.add(tank)
                    break
            if key_press[key_map['shoot'][tank]]:
                bullet = tank.shoot()
                if bullet:
                    self.play_music('shoot')
                    self.sprites.add(bullet)

    def dispatch_collision(self):
        collision_map = {
            'elements': {},
            'home': {},
            'bullets': {},
        }
        for (collision, args) in self.collision['elements'].items():
            collision_map['elements'][collision] = groupcollide(*args)

        for (collision, args) in self.collision['home'].items():
            collision_map['home'][collision] = spritecollide(*args)

        for (collision, args) in self.collision['bullets'].items():
            args_list = list(args)
            sprite_list = args_list[0]
            for sprite in sprite_list:
                args_list[0] = sprite
                args = tuple(args_list)
                collision_map['bullets'][sprite] = spritecollide(*args)

        for bullet in self.sprites.player_bullets:
            collision = spritecollide(bullet, self.scene_elements.iron_group, False, None)
            if collision:
                bullet.kill()

        for tank in self.sprites.enemy_tanks:
            if collision_map['bullets'][tank]:
                if tank.decrease_level():
                    GameManager().kill_enemies += 1
                    self.play_music('bang')
                    self.total_enemy_num -= 1

        for tank in self.sprites.player_tanks:
            if collision_map['bullets'][tank]:
                if tank.decrease_life():
                    self.play_music('bang')
                    if tank.life <= 0:
                        self.sprites.remove(tank)

        if collision_map['home']['PlayerBulletWithHome'] or collision_map['home']['EnemyBulletWithHome']:
            self.win_flag = False
            self.has_next_loop = False
            self.play_music('bang')
            self.__home.destroyed = True

    def game_loop(self):
        clock = pygame.time.Clock()

        while self.has_next_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == self.__generate_enemies_event:
                    if self.max_enemy_num > len(self.sprites.enemy_tanks):
                        for position in self.__enemy_point:
                            if len(self.sprites.enemy_tanks) == self.total_enemy_num:
                                break
                            enemy_tank = self.tank_factory.create_tank(position, TankFactory.ENEMY_TANK)
                            if spritecollide(enemy_tank, self.sprites.enemy_tanks, False, None) or \
                                    spritecollide(enemy_tank, self.sprites.player_tanks, False, None):
                                del enemy_tank
                            else:
                                self.sprites.add(enemy_tank)
            self.dispatch_player_operation()
            self.dispatch_collision()
            self.sprites.update(self.scene_elements, self.__home)
            self._draw_interface()

            if len(self.sprites.player_tanks) == 0:
                self.win_flag = False
                self.has_next_loop = False

            if self.total_enemy_num <= 0:
                self.win_flag = True
                self.has_next_loop = False

            clock.tick(60)

    def _draw_interface(self):
        screen = GameManager().screen
        screen.blit(self.background, (0, 0))
        self.scene_elements.draw(screen, 1)
        self.sprites.draw(screen, 1)
        self.scene_elements.draw(screen, 2)

        self.__home.draw(screen)
        pygame.display.flip()

    def show(self):
        self.load_game_screen()
        self.__load_game()
        self.__load_event()
        self.__load_tanks()
        self.__load_collision()
        self.play_music('start')
        self.game_loop()
        GameManager().win_game = self.win_flag
