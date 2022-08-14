import pygame, os, random
from utils.utils import load_image
from components.bullet import Bullet
from components_templates.sprite import SpriteTemplate
from components.enemy import Enemy

class Player(SpriteTemplate):

    def __init__(self, *, image_path: str, rect, 
        all_sprites_render_plain: pygame.sprite.RenderPlain,
        movement_speed=10, bullet_shoot_delay=0.5):
        super().__init__(image_path=image_path, rect=rect)

        # Centers player position at (almost) bottom of the game screen
        self.rect.move_ip(
            pygame.display.get_surface().get_size()[0] / 2 -
                (self.image.get_size()[0] / 2),
            pygame.display.get_surface().get_size()[1] - 100)

        # Game related variables
        self.movement_speed = movement_speed
        self.bullet_shoot_delay = bullet_shoot_delay
        self.can_shoot = True
        self.max_hp = 3
        self.hp = 3
        self.max_exp = 100
        self.exp = 0

        # Below 2 lines should be removed and moved to other class later
        # self.time_left = 300
        # self.max_time_left = 300

        self.clock = pygame.time.Clock()
        self.time_since_last_shoot = 0
        self.all_sprites_render_plain = all_sprites_render_plain

        # Movement
        self.active_keys = {
            pygame.K_w: {
                'active': False,
                'action': lambda: self.rect.move_ip(0, -self.movement_speed)
            },
            pygame.K_a: {
                'active': False,
                'action': lambda: self.rect.move_ip(-self.movement_speed, 0)
            },
            pygame.K_s: {
                'active': False,
                'action': lambda: self.rect.move_ip(0, self.movement_speed)
            },
            pygame.K_d: {
                'active': False,
                'action': lambda: self.rect.move_ip(self.movement_speed, 0)
            },
            pygame.K_SPACE: {
                'active': False,
                'action': self._shoot_bullet
            }
        }

    def _shoot_bullet(self):
        if self.can_shoot:
            self.all_sprites_render_plain.add(
                    Bullet(image_path='data/sprites/bullet.png',
                        rect=(8, 20), player=self,
                        all_sprites_render_plain=self.all_sprites_render_plain,
                        object_to_fire_from=self,
                        movement_speed=15))
            self.can_shoot = False
    
    def _check_if_touched_enemy(self):
        collided_objects = \
            pygame.sprite.spritecollide(self, self.all_sprites_render_plain,
                False)

        for collided_object in collided_objects:
            if isinstance(collided_object, Enemy):
                dealt_dmg = collided_object.suicide()
                self.hp -= dealt_dmg

    def _check_player_movement(self):
        """Checks if player isn't going out of the screen border."""
        screen_size = pygame.display.get_surface().get_size()

        # continue here with making this working somehow
        if self.rect.centerx <= 0:
            self.active_keys[pygame.K_a]['active'] = False
        if self.rect.centery <= 0:
            self.active_keys[pygame.K_w]['active'] = False
        if self.rect.centerx >= screen_size[0]:
            self.active_keys[pygame.K_d]['active'] = False
        if self.rect.centery >= screen_size[1]:
            self.active_keys[pygame.K_s]['active'] = False

    def movement(self, event):
        for key in self.active_keys.keys():
            if event.type == pygame.KEYDOWN and event.key == key:
                self.active_keys[key]['active'] = True
            if event.type == pygame.KEYUP and event.key == key:
                self.active_keys[key]['active'] = False

    def enemy_killed(self, exp_min, exp_max):
        gained_exp = random.randint(exp_min, exp_max)
        self.exp += gained_exp
    
    def level_up(self):
        self.max_hp += 1
        self.hp = self.max_hp
        self.exp -= self.max_exp

    def update(self):
        self.clock.tick()

        # Checks if bullet delay time has passed
        if self.time_since_last_shoot >= self.bullet_shoot_delay * 1000:
            self.can_shoot = True
            self.time_since_last_shoot = 0

        if not self.can_shoot:
            # Updates timer
            self.time_since_last_shoot += self.clock.get_time()

        self._check_if_touched_enemy()
        for key, value in self.active_keys.items():
            self._check_player_movement()
            if value['active']:
                value['action']()