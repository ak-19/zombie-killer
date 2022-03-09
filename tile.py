import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_id, tile_group, platform_group) -> None:
        super().__init__()
        self.start = (x, y)

        self.image = pygame.transform.scale(pygame.image.load(f'assets/images/tiles/Tile ({tile_id}).png'), (32, 32))
        self.rect = self.image.get_rect()

        if tile_id > 1: platform_group.add(self)    

        tile_group.add(self)

        self.rect.topleft = (x, y)

        self.mask = pygame.mask.from_surface(self.image)        
        