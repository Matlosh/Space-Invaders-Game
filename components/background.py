import pygame, random, os
from utils.utils import load_image

class Background(pygame.sprite.Sprite):
    
    def __init__(self, move_speed=1, *used_tiles: list):
        super().__init__()

        self.window_size = pygame.display.get_surface().get_size()
        self.image = pygame.Surface(self.window_size)
        self.rect = self.image.get_rect()

        self.TILE_SIZE = (48, 48)

        # Creates dict containing all available sprites in the data/sprites 
        # folder
        # Name of the key (in the dict) corresponds to the name of the file
        # (without extension)
        self.TILES = {}
        sprites_path = 'data/sprites'
        files_paths_list = [x for x in os.listdir(sprites_path)
            if os.path.isfile(f'{sprites_path}/{x}')]
        
        for file_path in files_paths_list:
            file_name = file_path.split('.')[0]
            self.TILES[file_name] = load_image(f'{sprites_path}/{file_path}',
                max_size=self.TILE_SIZE)

        self.available_tiles = {}
        
        for tile in used_tiles:
            if tile in list(self.TILES.keys()):
                self.available_tiles[tile] = self.TILES.get(tile)

        self.map = []
        for y in range(-1, self.window_size[1] // self.TILE_SIZE[1]):
            map_row = self._generate_map_row(y=y * self.TILE_SIZE[1])
            self.map.extend(map_row)

        self.move_speed = move_speed
        self.move_position = 0

    def _generate_map_row(self, *, y=0):
        generated_map_row = []
        for x in range(0, self.window_size[0] // self.TILE_SIZE[0] + 1):
            tiles = list(self.available_tiles.values())
            rand_title_num = random.randint(0, len(tiles) - 1)

            generated_map_row.append([tiles[rand_title_num],
                (x * self.TILE_SIZE[0], y)])

        return generated_map_row

    def update(self):
        if self.move_position > self.TILE_SIZE[1]:
            self.move_position = 0
            self.map.extend(self._generate_map_row(y=-48))
            
            # Clears unused tiles (the ones that went out of the screen)
            for tile in self.map:
                if tile[1][1] > self.window_size[1]:
                    self.map.remove(tile)

        self.move_position += self.move_speed

        for map_tile in self.map:
            self.image.blit(map_tile[0], map_tile[1])
            map_tile[1] = (map_tile[1][0], map_tile[1][1] + self.move_speed)