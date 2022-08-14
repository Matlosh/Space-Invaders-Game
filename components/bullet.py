import pygame, os
from utils.utils import load_image
from components.enemy import Enemy
from components_templates.sprite import SpriteTemplate

class Bullet(SpriteTemplate):

    def __init__(self, *, image_path: str, rect, player,
        all_sprites_render_plain: pygame.sprite.RenderPlain,
        object_to_fire_from: pygame.sprite.Sprite, movement_speed=10):
        super().__init__(image_path=image_path, rect=rect)

        self.rect.move_ip(
            object_to_fire_from.rect.centerx - (self.image.get_size()[0] / 2), 
            object_to_fire_from.rect.top - self.image.get_size()[1])

        # Game variables
        self.movement_speed = movement_speed

        # Supporting variables
        self.all_sprites_render_plain = all_sprites_render_plain
        self.player = player

    def _check_if_exited_screen(self):
        if self.rect.bottom <= 0:
            self.kill()

    def _check_if_hit_anybody(self):
        collided_objects = \
            pygame.sprite.spritecollide(self, self.all_sprites_render_plain, False)
        
        for collided_object in collided_objects:
            if isinstance(collided_object, Enemy):
                is_dead = collided_object.hit()

                if is_dead:
                    self.player.enemy_killed(
                        collided_object.given_exp_min,
                        collided_object.given_exp_max)

                self.kill()

    def update(self):
        self._check_if_exited_screen()
        self._check_if_hit_anybody()
        self.rect.move_ip(0, -self.movement_speed)