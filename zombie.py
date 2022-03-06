import pygame
from random import choice, randint

from screen import Screen

vector = pygame.math.Vector2

class Zombie(pygame.sprite.Sprite):
    def generate_sprites(self, gender, flip, state):
        sprites = []

        for i in range(1, 11):
            image = pygame.transform.scale(pygame.image.load(f'assets/images/zombie/{gender}/{state}/{state.capitalize()} ({i}).png'), (32, 32))
            if flip: image = pygame.transform.flip(image, True, False)
            sprites.append(image)

        return sprites

    def __init__(self, platform_group, portal_group, min_speed, max_speed):
        super().__init__()
        self.VERTICAL_ACCELERATION = 3
        self.RISE_TIME = 2
        
        gender = choice(['boy','girl'])        

        self.walk_right_sprite = self.generate_sprites(gender, False, 'walk')
        self.walk_left_sprite = self.generate_sprites(gender, True, 'walk')

        self.die_right_sprite = self.generate_sprites(gender, False, 'dead')
        self.die_left_sprite = self.generate_sprites(gender, True, 'dead')

        self.rise_right_sprite = self.generate_sprites(gender, False, 'walk')
        self.rise_left_sprite = self.generate_sprites(gender, True, 'walk')

        self.direction = choice([-1, 1])
        self.current_sprite = 0
        if self.direction > 0:
            self.image = self.walk_right_sprite[self.current_sprite]
        else:
            self.image = self.walk_left_sprite[self.current_sprite]            

        self.rect = self.image.get_rect()

        self.rect.bottomleft = (randint(100, Screen.WIDTH), -100)

        self.platform_group, self.portal_group, self.min_speed, self.max_speed = platform_group, portal_group, min_speed, max_speed

        self.animate_death = False
        self.animate_rise = False

        self.hit_sound = pygame.mixer.Sound('assets/sounds/zombie_hit.wav')
        self.kick_sound = pygame.mixer.Sound('assets/sounds/zombie_kick.wav')
        self.portal_sound = pygame.mixer.Sound('assets/sounds/portal_sound.wav')

        self.position = vector(self.rect.x, self.rect.y)
        self.velocity = vector(self.direction * randint(min_speed, max_speed), 0)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        self.is_dead = False
        self.round_time = 0
        self.frame_count = 0


    def update(self): pass
    def move(self): pass
    def check_collission(self): pass
    def check_animations(self): pass

    def animate(self): pass

