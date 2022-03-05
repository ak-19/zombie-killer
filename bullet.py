import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_group, player):
        super().__init__()

        self.velocity = 20
        self.range = 500

        if player.velocity.x > 0:
            self.image = pygame.transform.scale(pygame.image.load('assets/images/player/slash.png'), (32, 32))
        else:
            self.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load('assets/images/player/slash.png'), True, False), (32, 32))            
            self.velocity *= -1
            
        self.rect = self.image.get_rect()

        self.rect.bottomleft = (x, y)

        bullet_group.add(self)

        self.start_x = x

    def update(self):
        self.rect.x += self.velocity

        if abs(self.rect.x - self.start_x) > self.range:
            self.kill()

