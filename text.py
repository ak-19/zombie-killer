import pygame
from colors import Colors
from screen import Screen

class Text:
    def __init__(self, display) -> None:
        self.title_font = pygame.font.Font('assets/fonts/Poultrygeist.ttf', 36)
        self.bottom_bar_font = pygame.font.Font('assets/fonts/Pixel.ttf', 24)
        self.display = display

    def draw(self, score, round_number, round_time):
        score_text = self.bottom_bar_font.render(f'Score: {score}', True, Colors.WHITE)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (10, Screen.HEIGHT - 50)
        self.display.blit(score_text, score_text_rect)

        health_text = self.bottom_bar_font.render(f'Health: {100}', True, Colors.WHITE)
        health_text_rect = health_text.get_rect()
        health_text_rect.topleft = (10, Screen.HEIGHT - 25)
        self.display.blit(health_text, health_text_rect) 

        title_text = self.title_font.render('Zombie killer', True, Colors.GREEN)
        title_text_rect = title_text.get_rect()
        title_text_rect.center = (Screen.WIDTH // 2, Screen.HEIGHT - 25)
        self.display.blit(title_text, title_text_rect)         


        round_text = self.bottom_bar_font.render(f'Killer: {round_number}', True, Colors.WHITE)
        round_text_rect = round_text.get_rect()
        round_text_rect.topright = (Screen.WIDTH - 10, Screen.HEIGHT - 50)
        self.display.blit(round_text, round_text_rect)

        time_text = self.bottom_bar_font.render(f'Sunrise in: {round_time}', True, Colors.WHITE)
        time_text_rect = time_text.get_rect()
        time_text_rect.topright = (Screen.WIDTH - 10, Screen.HEIGHT - 25)
        self.display.blit(time_text, time_text_rect)                                
