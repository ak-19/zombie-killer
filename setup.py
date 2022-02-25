import pygame

from screen import Screen

class Setup:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Zombie killer')

    def create_display(self):
        return pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))

    def quit(self):        
        pygame.quit()