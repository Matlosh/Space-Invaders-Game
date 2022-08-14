from pygame.mixer import music
import os

class MusicManager:
    
    def __init__(self, *, music_folder_path: str):
        super().__init__()
        self.music_folder_path = music_folder_path

        self.SOUNDTRACKS_LIST = {}

        # Loads soundtracks from the folder
        if os.path.isdir(self.music_folder_path):
            music_filenames = [x for x in os.listdir(self.music_folder_path)
                if os.path.isfile(f'{self.music_folder_path}/{x}')]
            
            for music_filename in music_filenames:
                filename = music_filename.split('.', 1)[0]
                self.SOUNDTRACKS_LIST[filename] = \
                    f'{self.music_folder_path}/{music_filename}'
        

    def is_currently_playing(self):
        return music.get_busy()

    def play(self, soundtrack_name, fadein_time=1500):
        music.unload()
        try:
            music.load(self.SOUNDTRACKS_LIST.get(soundtrack_name))
            # Plays infinitely (will loop)
            music.play(-1, fade_ms=fadein_time)
        except TypeError:
            pass

    def stop(self, fadeout_time=1500):
        music.fadeout(fadeout_time)