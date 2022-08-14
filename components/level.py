import pygame, random, pickle, json
from components.enemy import Enemy
from components.background import Background
from components.player import Player
from components.gui import GUI
from components.music_manager import MusicManager

class Level:

    def __init__(self, *, level_max_time: int, enemy_tiers: tuple, 
        enemy_delay: int, background: Background, gui: GUI, player: Player,
        all_sprites: pygame.sprite.RenderPlain,
        screen: pygame.surface.Surface, music_manager: MusicManager,
        soundtrack_name=None, boss_level=False):
        # level_max_time and enemy_delay are in seconds
        self.level_max_time = level_max_time
        self.enemy_tiers = enemy_tiers
        self.enemy_delay = enemy_delay

        # "Imported" instances
        self.background = background
        self.gui = gui
        self.player = player
        self.all_sprites = all_sprites
        self.screen = screen
        self.music_manager = music_manager

        self.window_size = pygame.display.get_window_size()
        self.time_left = self.level_max_time

        self.is_boss_level = boss_level
        self.soundtrack_name = soundtrack_name

        # Min, max stats of the enemy (depending on tier)
        self.ENEMY_TIER_STATS = {
            # key names must be the same as in the class constructor
            # The way below stats are done stinks (redundant)
            'tier_1': {
                'max_hp': [1, 3],
                'dmg_dealt': [1, 1],
                'movement_speed': [1, 3],
                'movement_type': ['stand', 'left_right'],
                'given_exp_min': [1, 2],
                'given_exp_max': [2, 3],
                'rect': [(24, 24), (48, 48)],
                'image_path': ['data/sprites/enemy_1.png'],
                'start_min_position': (0, 0),
                'start_max_position': [
                    (self.window_size[0], self.window_size[1] // 2),
                    (self.window_size[0], self.window_size[1] // 2)],
                'movement_func_rand_min': (1, 1),
                'movement_func_rand_max': (50, 5),
                'fall_movement_speed': [0, 3]
            },
            'tier_2': {
                'max_hp': [2, 5],
                'dmg_dealt': [1, 2],
                'movement_speed': [2, 5],
                'movement_type': ['left_right', 'sin', 'cos'],
                'given_exp_min': [1, 3],
                'given_exp_max': [3, 4],
                'rect': [(32, 32), (56, 56)],
                'image_path': ['data/sprites/enemy_2.png'],
                'start_min_position': (0, 0),
                'start_max_position': [
                    (self.window_size[0], self.window_size[1] // 3),
                    (self.window_size[0], self.window_size[1] // 3)],
                'movement_func_rand_min': (1, 1),
                'movement_func_rand_max': (60, 6),
                'fall_movement_speed': [0, 5]
            },
            'tier_3': {
                'max_hp': [3, 7],
                'dmg_dealt': [1, 3],
                'movement_speed': [4, 8],
                'movement_type': ['sin', 'cos'],
                'given_exp_min': [1, 4],
                'given_exp_max': [4, 7],
                'rect': [(48, 48), (64, 64)],
                'image_path': ['data/sprites/enemy_3.png'],
                'start_min_position': (0, 0),
                'start_max_position': (self.window_size[0], 100),
                'movement_func_rand_min': (1, 1),
                'movement_func_rand_max': (70, 7),
                'fall_movement_speed': [0, 7]
            },
            'tier_4': {
                'max_hp': [8, 12],
                'dmg_dealt': [1, 1],
                'movement_speed': [5, 9],
                'movement_type': ['sin', 'cos'],
                'given_exp_min': [1, 5],
                'given_exp_max': [5, 8],
                'rect': [(48, 48), (80, 80)],
                'image_path': ['data/sprites/enemy_4.png'],
                'start_min_position': (0, 0),
                'start_max_position': (self.window_size[0], 100),
                'movement_func_rand_min': (1, 1),
                'movement_func_rand_max': (80, 8),
                'fall_movement_speed': [0, 8]
            },
            'tier_5': {
                'max_hp': [6, 10],
                'dmg_dealt': [1, 4],
                'movement_speed': [5, 8],
                'movement_type': ['sin', 'cos'],
                'given_exp_min': [1, 6],
                'given_exp_max': [6, 9],
                'rect': [(64, 64), (96, 96)],
                'image_path': ['data/sprites/enemy_5.png'],
                'start_min_position': (0, 0),
                'start_max_position': (self.window_size[0], 100),
                'movement_func_rand_min': (1, 1),
                'movement_func_rand_max': (100, 10),
                'fall_movement_speed': [0, 9]
            },
            # tier_6 should be treated like a "boss" enemy
            'tier_6': {
                'max_hp': [40, 80],
                'dmg_dealt': [100, 100],
                'movement_speed': [6, 10],
                'movement_type': ['sin', 'cos'],
                'given_exp_min': [1, 5],
                'given_exp_max': [5, 10],
                'rect': [(64, 64), (112, 112)],
                'image_path': ['data/sprites/boss.png'],
                'start_min_position': (0, 0),
                'start_max_position': (self.window_size[0], 200),
                'movement_func_rand_min': (60, 7),
                'movement_func_rand_max': (120, 12),
                'fall_movement_speed': [8, 16]
            }
        }

        if self.is_boss_level:
            enemy_tiers_altered = list(self.enemy_tiers)
            enemy_tiers_altered.append(1)
            self.enemy_tiers = tuple(enemy_tiers_altered)

        self.level_enemies = {}

        # Creating enemies
        for tier, num_of_enemies in enumerate(self.enemy_tiers):
            if f'tier_{tier + 1}' not in list(self.level_enemies.keys()):
                self.level_enemies[f'tier_{tier + 1}'] = []

            for _ in range(num_of_enemies):
                enemy_creation_args = {}

                for attribute_name, values in \
                    list(self.ENEMY_TIER_STATS[f'tier_{tier + 1}'].items()):
                    value = None

                    # Checks if all of the values are ints (if are then random 
                    # value from given min/max can be drawn)
                    if isinstance(values, tuple):
                        value = values
                    elif len(list(filter(lambda x: isinstance(x, int), values))) \
                        == len(values):
                        value = random.randint(*values)
                    elif len(list(filter(lambda x: isinstance(x, tuple),
                        values))) == len(values):
                        min_max_list = []
                        for min_val, max_val in zip(*values):
                            min_max_list.append([min_val, max_val])

                        value = []
                        for min_max in min_max_list:
                            rand_val = random.randint(min_max[0], min_max[1])
                            value.append(rand_val)
                        value = tuple(value)
                    else:
                        rand_elem = random.randint(0, len(values) - 1)
                        value = values[rand_elem]
                    
                    enemy_creation_args[attribute_name] = value

                # now add to created enemies to move and random their creation position
                enemy = Enemy(**enemy_creation_args)
                self.level_enemies[f'tier_{tier + 1}'].append(enemy)

        self.enemies_list = [x for y in self.level_enemies.values() for x in y]
        self.clock = pygame.time.Clock()
        self.counter = 0
        self.counter_2 = 0

    def spawn_new_enemy(self):
        """Checks if enemy can be spawned and if can, then does it."""
        if self.counter >= self.enemy_delay * 1000 \
            and len(self.enemies_list) > 0:
            self.counter = 0
            rand_num = random.randint(0, len(self.enemies_list) - 1)
            self.all_sprites.add(self.enemies_list[rand_num])
            self.enemies_list.pop(rand_num)

    def check_if_level_has_ended(self):
        """Returns True if level has ended and false if hasn't."""
        if self.is_boss_level and all(
            [not isinstance(x, Enemy) for x in self.all_sprites.sprites()]):
            self.music_manager.stop()
            return True
        if self.counter_2 >= 1000 and self.time_left == 1:
            self.time_left -= 1
            self.music_manager.stop()
            return True
        elif self.counter_2 >= 1000 and self.time_left >= 0:
            self.counter_2 = 0
            self.time_left -= 1
        return False

    def update(self):
        self.clock.tick()
        self.counter += self.clock.get_time()
        self.counter_2 += self.clock.get_time()

        # Starts the music
        if self.soundtrack_name != None and \
            not self.music_manager.is_currently_playing():
            self.music_manager.play(self.soundtrack_name)
        
        # self.check_if_level_has_ended()
        self.spawn_new_enemy()

        self.all_sprites.update()
        self.background.update()

        self.screen.blit(self.background.image, (0, 0))
        self.all_sprites.draw(self.screen)