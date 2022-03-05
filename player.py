import pygame
from bullet import Bullet

vector = pygame.math.Vector2

from screen import Screen

class Player(pygame.sprite.Sprite):
    def populate_sprite_list(self, what, flip):
        sprite_list = []
        for i in range(1, 11):
            image = pygame.transform.scale(pygame.image.load(f'assets/images/player/{what}/{what.capitalize()} ({i}).png') ,(64, 64))
            if flip:
                image = pygame.transform.flip(image, True, False)
            sprite_list.append(image)

        return sprite_list

    def generate_sprites(self):
        self.move_right_sprites = self.populate_sprite_list('run', False)
        self.move_left_sprites = self.populate_sprite_list('run', True)

        self.idle_right_sprites = self.populate_sprite_list('idle', False)
        self.idle_left_sprites = self.populate_sprite_list('idle', True)

        self.jump_right_sprites = self.populate_sprite_list('jump', False)
        self.jump_left_sprites = self.populate_sprite_list('jump', True)

        self.attack_right_sprites = self.populate_sprite_list('attack', False)
        self.attack_left_sprites = self.populate_sprite_list('attack', True)

    def setup_constants(self):
        self.HORIZONTAL_ACCELERATION = 2
        self.HORIZONTAL_FRICTION = .15
        self.VERTICAL_ACCELERATION = .8
        self.VERTICAL_JUMP_SPEED = 18
        self.STARTING_HEALTH = 100

    def set_sounds(self):
        self.jump_sound = pygame.mixer.Sound('assets/sounds/jump_sound.wav')
        self.slash_sound = pygame.mixer.Sound('assets/sounds/slash_sound.wav')
        self.portal_sound = pygame.mixer.Sound('assets/sounds/portal_sound.wav')
        self.hit_sound = pygame.mixer.Sound('assets/sounds/zombie_hit.wav')

    def __init__(self, x, y, platform_group, portal_group, bullet_group):        
        super().__init__()

        self.setup_constants()
        
        self.generate_sprites()

        self.sprite_index = 0

        self.image = self.idle_right_sprites[self.sprite_index]
        self.rect = self.image.get_rect()
        
        self.platform_group, self.portal_group, self.bullet_group = platform_group, portal_group, bullet_group

        self.animate_jump = False
        self.animate_fire = False

        self.set_sounds()

        self.start_position = (x, y)
        self.reset()

        self.health = self.STARTING_HEALTH

    def update(self):
        self.move()
        self.check_collission()
        self.check_animations()

    def move(self):
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.acceleration.x = -self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, .5)
        elif keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites, .5)
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, .5)
            else:
                self.animate(self.idle_left_sprites, .5)
        
        
        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION 

        self.velocity += self.acceleration

        self.position += self.velocity + .5*self.acceleration

        if self.position.x < 0:
            self.position.x = Screen.WIDTH

        elif self.position.x > Screen.WIDTH:
            self.position.x = 0           

        self.rect.bottomleft = self.position


    def check_collission(self):
        if self.velocity.y > 0:
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
            if collided_platforms:
                self.position.y = collided_platforms[0].rect.top + 1
                self.velocity.y = 0
            

        if self.velocity.y < 0:
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
            if collided_platforms:
                self.velocity.y = 0
                while pygame.sprite.spritecollide(self, self.platform_group, False):
                    self.position.y += 1
                    self.rect.bottomleft = self.position


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
        if self.animate_jump:
            if self.velocity.x > 0:
                self.animate(self.jump_right_sprites, .1)
            else:
                self.animate(self.jump_left_sprites, .1)

        if self.animate_fire:
            if self.velocity.x > 0:
                self.animate(self.attack_right_sprites, .25)
            else:
                self.animate(self.attack_left_sprites, .25)                


    def jump(self): 
        if pygame.sprite.spritecollide(self, self.platform_group, False):
            self.jump_sound.play()
            self.velocity.y = -self.VERTICAL_JUMP_SPEED
            self.animate_jump = True



    def shoot(self): 
        self.slash_sound.play()
        x, y = self.rect.center
        Bullet(x, y, self.bullet_group, self)
        self.animate_fire = True
        

    def reset(self):
        self.position = vector(self.start_position[0], self.start_position[1])
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)
        self.rect.bottomleft = self.position 

    def animate(self, sprites, speed):
        self.sprite_index += speed
        if self.sprite_index >= len(sprites):
            self.sprite_index = 0
            self.animate_jump = False
            self.animate_fire = False
        self.image = sprites[int(self.sprite_index)]

