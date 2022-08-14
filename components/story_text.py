import pygame
from components.music_manager import MusicManager

class StoryText(pygame.font.Font):
    
    def __init__(self, *, file_name, size=16, space_between=10,
        music_manager: MusicManager):
        super().__init__(file_name, size)

        self.window_size = pygame.display.get_window_size()
        self.space_between = space_between
        self.music_manager = music_manager
        # self.clock = pygame.time.Clock()
        # self.counter = 0

    def render_text(self, *, background_color: tuple, text: str,
        text_color: tuple, screen: pygame.surface.Surface,
        padding: tuple=(0, 0), soundtrack_name=None, showing_words_delay=0):
        """Creates text window and prints it on the screen."""
        # self.clock.tick()
        # self.counter += self.clock.get_time()
        # showing words delay isn't implemented yet

        background = pygame.Surface(self.window_size)
        background.fill(background_color)

        text_container = pygame.Surface(self.window_size)
        text_container.set_colorkey((0, 0, 0))

        text_cursor_pos = padding
        words = text.split(' ')

        for word in words:
            word_to_render = self.render(word, True, text_color)
            word_to_render_size = word_to_render.get_size()

            # Moves word to the next line if it's too long
            # (goes out of the window)
            if text_cursor_pos[0] + word_to_render_size[0] + \
                padding[0] * 2 >= self.window_size[0]:
                text_cursor_pos = (
                    padding[0],
                    text_cursor_pos[1] + word_to_render_size[1])

            # background.blit(word_to_render, text_cursor_pos)
            text_container.blit(word_to_render, text_cursor_pos)

            if text_cursor_pos[0] + word_to_render_size[0] + \
                (self.space_between * words.index(word)) + padding[0] >= \
                    self.window_size[0]:
                text_cursor_pos = (padding[0], text_cursor_pos[1] +
                    word_to_render_size[1])
            else:
                text_cursor_pos = (
                    text_cursor_pos[0] + word_to_render_size[0] +
                        self.space_between,
                    text_cursor_pos[1])

        if soundtrack_name != None and \
            not self.music_manager.is_currently_playing():
            self.music_manager.play(soundtrack_name)

        background.blit(text_container, 
            (0, (self.window_size[1] - text_cursor_pos[1]) / 2))
        screen.blit(background, (0, 0))