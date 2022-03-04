import pygame
from background import Background

from colors import Colors
from player import Player
from portal import Portal
from rubymaker import RubyMaker
from screen import Screen
from tile import Tile
from tilemap import TileMap
from text import Text

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
                elif tile_id == 7:
                    Portal(j*32, i*32, 'green', self.portal_group)                    
                elif tile_id == 8:
                    Portal(j*32, i*32, 'purple', self.portal_group)  
                elif tile_id == 9:                                                          
                    self.player = Player(j*32, i*32 + 32, self.platform_group, self.portal_group, self.bullet_group)
                    self.player_group.add(self.player)
        
        self.text = Text(display)


        self.setup_stats()

    def setup_stats(self):
        self.STARTING_ROUND_TIME = 30
        self.score = 0
        self.round_number = 0
        self.round_time = self.STARTING_ROUND_TIME
        self.frame_count = 0

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
        self.portal_group.draw(self.display)

        self.player_group.draw(self.display)

        self.text.draw(self.score, self.round_number, self.round_time)

    def update(self): 
        self.frame_count += 1
        if self.frame_count % 60 == 0:
            self.round_time -= 1
            self.frame_count = 0

        self.main_tile_group.update() 
        self.portal_group.update() 

    def add_zombie(self): pass    
    def check_collissions(self): pass    
    def check_round_completion(self): pass    
    def check_game_over(self): pass    
    def start_new_round(self): pass    

    def pause_game(self): pass    
    def reset_game(self): pass    