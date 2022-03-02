import pygame

class RubyMaker(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_group):
        super().__init__()

        self.sprites = []

        for i in range(7):
            self.sprites.append(pygame.transform.scale(pygame.image.load(f'assets/images/ruby/tile00{i}.png'), (64, 64)))

        self.sprite_index = 0

        self.image = self.sprites[self.sprite_index]

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        tile_group.add(self)


    def update(self):
        self.animate(.25)

    def animate(self, speed):
        self.sprite_index += speed
        if self.sprite_index >= len(self.sprites):
            self.sprite_index = 0
        self.image = self.sprites[int(self.sprite_index)]

