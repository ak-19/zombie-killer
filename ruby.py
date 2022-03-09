from secrets import choice
import pygame
from screen import Screen

vector = pygame.math.Vector2

class Ruby(pygame.sprite.Sprite):
    def __init__(self, platform_group, portal_group):
        super().__init__()

        self.VERTICAL_ACCELERATION = 3
        self.HORIZONTAL_VELOCITY = 5
        self.sprites = []

        for i in range(7):
            self.sprites.append(pygame.transform.scale(pygame.image.load(f'assets/images/ruby/tile00{i}.png'), (64, 64)))

        self.sprite_index = 0

        self.image = self.sprites[self.sprite_index]        
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (Screen.WIDTH // 2, 100)

        self.platform_group, self.portal_group = platform_group, portal_group

        self.portal_sound = pygame.mixer.Sound('assets/sounds/portal_sound.wav')

        self.position = vector(self.rect.x, self.rect.y)
        self.velocity = vector(choice([-1, 1])*self.HORIZONTAL_VELOCITY, self.HORIZONTAL_VELOCITY)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

    def update(self): 
        self.animate(.25)
        self.move()
        self.check_collissions()

    def move(self): 
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

    def animate(self, speed):
        self.sprite_index += speed
        if self.sprite_index >= len(self.sprites):
            self.sprite_index = 0
        self.image = self.sprites[int(self.sprite_index)]



