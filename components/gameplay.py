import pygame
from components.player import Player
from components.gui import GUI
from components.background import Background
from components.story_text import StoryText
from components.level import Level
from components.music_manager import MusicManager
from components.menu import Menu

class Gameplay:
    """
    Gameplay is a class that manages game flow.
    Note: Object of it should be created only once and used
    in the main game loop.
    """

    def __init__(self, *, screen: pygame.surface.Surface):
        self.all_sprites = pygame.sprite.RenderPlain()
        self.screen = screen

        self.TEXTS = {}
        with open('data/changeable/texts.txt', 'r') as texts:
            for line in texts.readlines():
                line = line.strip('\n')
                key, value = line.split(':', 1)
                
                self.TEXTS[key] = value.strip()

        # Prepares the most important elements
        self.player = Player(image_path='data/sprites/player.png', rect=(48, 48),
            all_sprites_render_plain=self.all_sprites, movement_speed=5,
            bullet_shoot_delay=0.3)
        self.gui = GUI(rect=(100, 20), player=self.player)
        self.music_manager = MusicManager(music_folder_path='data/music')
        self.story_text = StoryText(file_name='data/fonts/Trispace-Bold.ttf',
            size=30, music_manager=self.music_manager)

        self.start_text = lambda: self.story_text.render_text(
            background_color=(20, 20, 20), text=self.TEXTS['start_text'],
            text_color=(255, 255, 255), screen=self.screen, padding=(10, 0),
            soundtrack_name='chopin-9-2-alianello')

        sea_background = Background(1, 'water_1', 'water_2', 'water_3',
            'water_4')
        self.level_1 = Level(level_max_time=180,
            enemy_tiers=(25, 20, 5, 5, 1),
            enemy_delay=3, background=sea_background, gui=self.gui,
            player=self.player, all_sprites=self.all_sprites,
            screen=self.screen, music_manager=self.music_manager,
            soundtrack_name='vivaldi_consordino')

        self.after_level_1_text = lambda: self.story_text.render_text(
            background_color=(20, 20, 20), 
            text=self.TEXTS['after_level_1_text'], text_color=(255, 255, 255),
            screen=self.screen, padding=(10, 0),
            soundtrack_name='2017_Tchaikovsky')

        plain_background = Background(1, 'grass_1', 'grass_2', 'grass_3',
            'grass_4')
        self.level_2 = Level(level_max_time=240, 
            enemy_tiers=(30, 25, 10, 10, 2),
            enemy_delay=3.5, background=plain_background, gui=self.gui,
            player=self.player, all_sprites=self.all_sprites,
            screen=self.screen, music_manager=self.music_manager,
            soundtrack_name='beethoven-furelise-bertoli')

        self.after_level_2_text = lambda: self.story_text.render_text(
            background_color=(20, 20, 20), 
            text=self.TEXTS['after_level_2_text'], text_color=(255, 255, 255),
            screen=self.screen, padding=(10, 0),
            soundtrack_name='liszt-resignazione-s263-djordjevic')

        # check the boss

        rocky_background = Background(1, 'rocky_1', 'rocky_2', 'rocky_3',
            'rocky_4', 'rocky_5', 'rocky_6')
        self.level_3 = Level(level_max_time=300, 
            enemy_tiers=(20, 30, 20, 15, 5),
            enemy_delay=4, background=rocky_background, gui=self.gui,
            player=self.player, all_sprites=self.all_sprites,
            screen=self.screen, music_manager=self.music_manager,
            soundtrack_name='mozart-k550-1-breemer-pfaul')

        self.after_level_3_text = lambda: self.story_text.render_text(
            background_color=(20, 20, 20), 
            text=self.TEXTS['after_level_3_text'], text_color=(255, 255, 255),
            screen=self.screen, padding=(10, 0),
            soundtrack_name='liszt-sancta-dorothea-yamadascriba')

        space_background = Background(1, 'space_1', 'space_2', 'space_3',
            'space_4', 'space_5', 'space_6', 'space_7', 'space_8', 'space_9')
        self.boss_level = Level(level_max_time=3600, enemy_tiers=(0, 0, 0, 0, 0),
            enemy_delay=1, background=space_background, gui=self.gui,
            player=self.player, all_sprites=self.all_sprites,
            screen=self.screen, music_manager=self.music_manager,
            boss_level=True,
            soundtrack_name='vivaldi_op8_mk_06_estate_presto')

        self.end_text = lambda: self.story_text.render_text(
            background_color=(20, 20, 20), text=self.TEXTS['end_text'],
            text_color=(255, 255, 255), screen=self.screen, padding=(10, 0),
            soundtrack_name='vivaldi_rv31_mn_03_adagio')

        self.game_over_text = lambda: self.story_text.render_text(
            background_color=(20, 20, 20), text=self.TEXTS['game_over_text'],
            text_color=(255, 0, 0), screen=self.screen, padding=(10, 0),
            soundtrack_name='chopin-64-2-hudson')

        self.menu = Menu(
            size=(self.screen.get_size()[0], self.screen.get_size()[1]),
            background_color=(20, 20, 20), screen=self.screen,
            options=['start_button', 'exit_button'], text_size=40)

        # Game flow - what's going to be executed (one after another)
        self.game_flow = [self.menu, self.start_text, self.level_1,
            self.after_level_1_text, self.level_2, self.after_level_2_text,
            self.level_3, self.after_level_3_text, self.boss_level,
            self.end_text]

        # Game flow control variables
        self.is_level_playing = False
        self.is_story_text_shown = True

    def update(self):
        # Game's events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            # Level
            if self.is_level_playing:
                self.player.movement(event)
            # Menu
            elif len(self.game_flow) > 0 and \
                isinstance(self.game_flow[0], Menu) and \
                event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.game_flow[0].move_up()
                if event.key == pygame.K_s:
                    self.game_flow[0].move_down()
                if event.key == pygame.K_SPACE:
                    self.game_flow[0].choose_option()
            # Story Text
            elif len(self.game_flow) > 0 and \
                callable(self.game_flow[0]) and \
                not self.is_level_playing and \
                event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.music_manager.stop()
                self.game_flow.pop(0)

        # If game_flow is empty then the game has ended
        if len(self.game_flow) <= 0:
            exit()

        # Checks if player has died
        if self.player.hp <= 0 and self.is_level_playing:
            self.game_flow = [self.game_over_text]
            self.is_level_playing = False
            self.music_manager.stop()

        if isinstance(self.game_flow[0], Level):
            self.is_level_playing = True
            self.gui.current_level = self.game_flow[0]
            self.all_sprites.add(self.player, self.gui)
            self.game_flow[0].update()

            if self.game_flow[0].check_if_level_has_ended():
                self.game_flow.pop(0)
                self.all_sprites.empty()

        elif isinstance(self.game_flow[0], Menu):
            self.game_flow[0].update()

            if self.game_flow[0].check_if_menu_is_closed():
                self.game_flow.pop(0)

        elif callable(self.start_text):
            self.is_level_playing = False
            self.all_sprites.empty()
            self.game_flow[0]()