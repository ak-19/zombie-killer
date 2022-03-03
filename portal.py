import pygame

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, color, portal_group):
        super().__init__()

        self.sprites = []

        for i in range(22):
            self.sprites.append(pygame.transform.scale(pygame.image.load(f'assets/images/portals/{color}/tile{str(i).zfill(3)}.png'), (72, 72)))

        self.sprite_index = 0

        self.image = self.sprites[self.sprite_index]
        self.rect = self.image.get_rect()

        self.rect.bottomleft = (x, y)

        portal_group.add(self)

    def update(self):
        self.animate(.25)

    def animate(self, speed):
        self.sprite_index += speed
        if self.sprite_index >= len(self.sprites):
            self.sprite_index = 0
        self.image = self.sprites[int(self.sprite_index)]

