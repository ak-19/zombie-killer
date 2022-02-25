import pygame

class Game:
    def __init__(self, display) -> None:
        self.display = display
        self.run = True

    def run_game_loop(self):

        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.run = False