import pygame
from background import Background

from colors import Colors
from rubymaker import RubyMaker
from screen import Screen
from tile import Tile
from tilemap import TileMap

class Game:
    def __init__(self, display) -> None:
        self.display = display
        self.run = True
        self.clock = pygame.time.Clock()
        self.background = Background(display)


        self.main_tile_group = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()

        self.player_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()

        self.zombie_group = pygame.sprite.Group()

        self.portal_group = pygame.sprite.Group()

        self.rubie_group = pygame.sprite.Group()

        self.tile_map = TileMap().get_map()

        for i in range(len(self.tile_map)):
            for j in range(len(self.tile_map[i])):
                tile_id = self.tile_map[i][j]
                if 0 < tile_id < 6:
                    Tile(j*32, i*32, tile_id, self.main_tile_group, self.platform_group)
                elif tile_id == 6:
                    RubyMaker(j*32, i*32, self.main_tile_group)


    def run_game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): return
            
            self.update()

            self.draw()
            
            pygame.display.update()
            
            self.clock.tick(60)


    def draw(self): 
        self.background.draw()
        self.main_tile_group.draw(self.display)

    def update(self): 
        self.main_tile_group.update()  
    def add_zombie(self): pass    
    def check_collissions(self): pass    
    def check_round_completion(self): pass    
    def check_game_over(self): pass    
    def start_new_round(self): pass    

    def pause_game(self): pass    
    def reset_game(self): pass    