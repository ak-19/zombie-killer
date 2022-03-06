import pygame
from random import choice, randint

from screen import Screen

vector = pygame.math.Vector2

class Zombie(pygame.sprite.Sprite):
    def generate_sprites(self, gender, flip, state):
        sprites = []

        for i in range(1, 11):
            image = pygame.transform.scale(pygame.image.load(f'assets/images/zombie/{gender}/{state}/{state.capitalize()} ({i}).png'), (64, 64))
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

        self.sprite_index = 0

    def update(self): 
        self.move()
        self.check_collissions()
        self.check_animations()

    def move(self): 
        if self.is_dead: return

        if self.direction < 0: self.animate(self.walk_left_sprite, .5)
        else: self.animate(self.walk_right_sprite, .5)

        self.velocity += self.acceleration
        self.position += self.velocity + .5*self.acceleration

        if self.position.x < 0: self.position.x = Screen.WIDTH
        elif self.position.x > Screen.WIDTH: self.position.x = 0           

        self.rect.bottomleft = self.position

    def check_collissions(self): 
        collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collided_platforms:
            self.position.y = collided_platforms[0].rect.top + 1
            self.velocity.y = 0
            
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            if self.position.x > Screen.WIDTH // 2:
                self.position.x = 86
            else:
                self.position.x = Screen.WIDTH - 150

            if self.position.y > Screen.HEIGHT // 2:                
                self.position.y = 64
            else:
                self.position.y = Screen.HEIGHT - 132

    def check_animations(self): 
        if self.animate_death:
            if self.direction < 0: self.animate(self.die_left_sprite, .5)
            else: self.animate(self.die_right_sprite, .5)

    def animate(self, sprites, speed):
        self.sprite_index += speed
        if self.sprite_index >= len(sprites):
            self.sprite_index = 0
            if self.animate_death:
                self.animate_death = False
                self.sprite_index = len(sprites) - 1

        self.image = sprites[int(self.sprite_index)]

