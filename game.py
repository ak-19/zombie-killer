import pygame
from background import Background

from colors import Colors
from screen import Screen

class Game:
    def __init__(self, display) -> None:
        self.display = display
        self.run = True
        self.clock = pygame.time.Clock()
        self.background = Background(display)

    def run_game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): return
            
            self.update()

            self.draw()
            
            pygame.display.update()
            
            self.clock.tick(60)


    def draw(self): self.background.draw()

    def update(self): pass    
    def add_zombie(self): pass    
    def check_collissions(self): pass    
    def check_round_completion(self): pass    
    def check_game_over(self): pass    
    def start_new_round(self): pass    

    def pause_game(self): pass    
    def reset_game(self): pass    