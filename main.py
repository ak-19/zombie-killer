from game import Game
from setup import Setup

setup = Setup()

Game(setup.create_display()).run_game_loop()

setup.quit()