import pygame
from components.player import Player

class GUI(pygame.sprite.Sprite):
    
    def __init__(self, *, rect, player: Player):
        pygame.sprite.Sprite.__init__(self)

        self.player = player
        # Below variable must be changed to the current level
        self.current_level = None

        self.image = pygame.Surface(rect)
        self.image.set_colorkey((0, 0, 0))

        # GUI elements (while playing)
        health_bar_container = pygame.Surface((rect[0], 10))
        health_bar_container.fill((0, 0, 1))

        exp_bar_container = pygame.Surface((rect[0], 3))
        exp_bar_container.fill((0, 0, 1))

        time_bar_container = pygame.Surface((rect[0], 3))
        exp_bar_container.fill((0, 0, 1))

        self.gui_elements = {
            health_bar_container: {
                'type': 'bar',
                'value': lambda: self.player.hp,
                'max_value': lambda: self.player.max_hp,
                'default_color': (0, 0, 1),
                'fill_color': (205, 200, 176),
                'image_position': (0, 0)
            },
            exp_bar_container: {
                'type': 'bar',
                'value': lambda: self.player.exp,
                'max_value': lambda: self.player.max_exp,
                'default_color': (0, 0, 1),
                'fill_color': (205, 200, 176),
                'image_position': (
                    0, health_bar_container.get_rect().bottom + 1),
                'on_full': lambda: self.player.level_up()
            },
            time_bar_container: {
                'type': 'bar',
                'value': lambda: self.current_level.time_left,
                'max_value': lambda: self.current_level.level_max_time,
                'default_color': (0, 0, 1),
                'fill_color': (0, 255, 143),
                'image_position': (0, 
                    health_bar_container.get_rect().bottom +
                    exp_bar_container.get_rect().bottom + 2)
            }
        }

        self.rect = self.image.get_rect()
        self.rect.move_ip(20, 20)

    def update_gui_element(self):
        for container, values in self.gui_elements.items():
            if values['type'] == 'bar':
                # Executes when bar is full
                if 'on_full' in values.keys() and \
                    values['value']() >= values['max_value']():
                    values['on_full']()

                # Clears bar (container)
                container.fill(values['default_color'])
                new_bar = None

                # Creates bar content
                if values['value']() >= 0:
                    new_bar = pygame.Surface((self.rect.size[0] * 
                        (values['value']() / values['max_value']()),
                        container.get_size()[1]))
                else:
                    new_bar = pygame.Surface((0, container.get_size()[1]))

                new_bar.fill(values['fill_color'])
                # Updates view
                container.blit(new_bar, (0, 0))
                self.image.blit(container, values['image_position'])

    def update(self):
        self.update_gui_element()