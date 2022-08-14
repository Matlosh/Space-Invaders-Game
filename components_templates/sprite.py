import pygame, os
from utils.utils import load_image

class SpriteTemplate(pygame.sprite.Sprite):
    """Template for each sprite in the game (contains sprite creation, 
    etc.)."""

    def __init__(self, *, image_path: str, rect):
        pygame.sprite.Sprite.__init__(self)

        # Loading sprite
        sprite_image = load_image(
            os.path.join(*image_path.split('/')), max_size=rect)
        self.image = sprite_image

        self.rect = self.image.get_rect()