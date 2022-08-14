import pygame

class Menu(pygame.surface.Surface):

    def __init__(self, *, size: tuple, background_color: tuple,
        screen: pygame.surface.Surface, options: list, text_size=20):
        super().__init__(size)

        self.background_color = background_color
        self.screen = screen
        self.window_size = pygame.display.get_window_size()
        self.options = options

        self.font = pygame.font.Font('data/fonts/Trispace-Bold.ttf',
            text_size)

        self.BUTTONS = {
            'start_button': {
                'surface': self.font.render('  Start', True, (255, 255, 255)),
                'on_hover': self.font.render('> Start', True, (255, 0, 0)),
                'on_choose': lambda: self._start_choose()
            },
            'exit_button': {
                'surface': self.font.render('  Exit', True, (255, 255, 255)),
                'on_hover': self.font.render('> Exit', True, (255, 0, 0)),
                'on_choose': lambda: self._exit_choose()
            }
        }
        self.hovered_pos = 0
        self.is_menu_closed = False

    def _start_choose(self):
        self.is_menu_closed = True

    def _exit_choose(self):
        exit()

    def move_up(self):
        if self.hovered_pos > 0:
            self.hovered_pos -= 1

    def move_down(self):
        if self.hovered_pos < len(self.options) - 1:
            self.hovered_pos += 1

    def choose_option(self):
        button = self.BUTTONS[self.options[self.hovered_pos]]
        button['on_choose']()

    def check_if_menu_is_closed(self):
        return self.is_menu_closed

    def update(self):
        self.fill(self.background_color)
        options = pygame.surface.Surface(self.window_size)
        options.set_colorkey((0, 0, 0))

        for i, option in enumerate(self.options):
            button_key = 'surface'
            if self.hovered_pos == i:
                button_key = 'on_hover'

            button = self.BUTTONS[option]
            button_size = button[button_key].get_size()

            options.blit(button[button_key],
                (self.window_size[0] / 2 - button_size[0] / 2,
                button_size[1] * i))

        one_button_size = self.BUTTONS[self.options[0]]['surface'].get_size()
        self.blit(options, (0,
            (self.window_size[1] - one_button_size[1] *
                len(self.options)) / 2))
        self.screen.blit(self, (0, 0))