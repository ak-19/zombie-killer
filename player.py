import pygame

vector = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def populate_sprite_list(self, what, flip):
        sprite_list = []
        for i in range(1, 11):
            image = pygame.transform.scale(pygame.image.load(f'assets/images/player/{what}/{what.capitalize()} ({1}).png') ,(64, 64))
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

        self.rect.bottomleft = (x, y)

        self.platform_group, self.portal_group, self.bullet_group = platform_group, portal_group, bullet_group

        self.animate_jump = False
        self.animate_fire = False

        self.set_sounds()

        self.start_position = (x, y)
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        self.health = self.STARTING_HEALTH

    def update(self): pass
    def move(self): pass
    def check_collission(self): pass
    def check_animations(self): pass

    def jump(self): 
        self.jump_sound.play()

    def shoot(self): pass
    def reset(self): pass
    def animate(self): pass

