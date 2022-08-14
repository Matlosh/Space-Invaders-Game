import pygame, os, math, random
from utils.utils import load_image
from components_templates.sprite import SpriteTemplate

class Enemy(SpriteTemplate):

    def __init__(self, *, image_path='data/sprites/enemy_1.png', 
        rect=(32, 32), max_hp=3, dmg_dealt=1, movement_type='stand',
        movement_speed=5, given_exp_min=1, given_exp_max=3,
        start_min_position=(0, 0), start_max_position=(600, 200),
        movement_func_rand_min=(1, 1), movement_func_rand_max=(50, 5),
        fall_movement_speed=1):
        super().__init__(image_path=image_path, rect=rect)

        # Draws start position
        start_x = random.randint(start_min_position[0], start_max_position[0])
        start_y = random.randint(start_min_position[1], start_max_position[1])
        self.rect.move_ip(start_x, start_y)

        # Game variables
        self.hp = max_hp
        self.dmg = dmg_dealt
        self.movement_speed = movement_speed
        self.given_exp_min = given_exp_min
        self.given_exp_max = given_exp_max
        self.fall_movement_speed = fall_movement_speed

        self.movement_type = movement_type
        self.screen_size = pygame.display.get_surface().get_size()

        # Below variable (tuple) is used only when movement_types is sin, etc.
        self.movement_func_rand = (
            random.randint(
                movement_func_rand_min[0], movement_func_rand_max[0]),
            random.randint(
                movement_func_rand_min[1], movement_func_rand_max[1]))
        self.movement_types = {
            'stand': lambda: self._movement(0, 0),
            'left_right': lambda: self._movement(self.movement_speed, 0),
            'sin': lambda: self._movement(
                self.movement_speed, 
                math.sin(self.rect.centerx / self.movement_func_rand[0]) 
                    * self.movement_func_rand[1]),
            'cos': lambda: self._movement(
                self.movement_speed,
                math.cos(self.rect.centerx / self.movement_func_rand[0])
                    * self.movement_func_rand[1])
        }

        self.clock = pygame.time.Clock()
        self.counter = 0
        self.y_additional_pos = 0

    def hit(self):
        """Executes enemy on hit situation and returns whether enemy was
        killed."""
        self.hp -= 1

        if self.hp <= 0:
            self.kill()
            return True
        return False

    def suicide(self):
        """Enemy commits suicide - and deals damage to his enemy."""
        self.kill()
        return self.dmg

    def _movement_control_borders(self):
        if self.rect.centerx <= 0 or self.rect.centerx >= self.screen_size[0]:
            self.movement_speed = -self.movement_speed
        if self.rect.centery <= 0 and self.fall_movement_speed < 0:
            # repair above code, because fall_movement_speed is changed (from minus to plus
            # and similar) too fast and enemies can't get out of the bottom of the screen
            self.fall_movement_speed = -self.fall_movement_speed
        if self.rect.centery >= self.screen_size[1] and self.fall_movement_speed > 0:
            self.fall_movement_speed = -self.fall_movement_speed

    def _movement(self, x, y):
        self.rect.move_ip(x, y + self.y_additional_pos)

    def update(self):
        self.clock.tick()
        self.counter += self.clock.get_time()

        # Below code smells bad, check that y_additional_pos
        if self.counter >= 100:
            self.counter = 0
            self.y_additional_pos = self.fall_movement_speed
        else:
            self.y_additional_pos = 0

        self._movement_control_borders()
        for movement_type, movement_func in self.movement_types.items():
            if self.movement_type == movement_type:
                movement_func()