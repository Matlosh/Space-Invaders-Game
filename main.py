import pygame
from components.gameplay import Gameplay
from utils.utils import load_image

def main():
    pygame.init()

    # Initializing screen
    screen = pygame.display.set_mode((640, 480), flags=pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption('Space Invaders')
    # Setting game icon
    icon = load_image('data/sprites/enemy_1.png', max_size=(32, 32))
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    gameplay = Gameplay(screen=screen)

    # Game loop
    while True:
        # Makes sure game doesn't run on more than 60fps
        clock.tick(60)
        gameplay.update()
        pygame.display.flip()

if __name__ == '__main__':
    main()