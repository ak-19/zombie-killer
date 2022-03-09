import pygame
from background import Background

from colors import Colors
from player import Player
from portal import Portal
from ruby import Ruby
from rubymaker import RubyMaker
from screen import Screen
from tile import Tile
from tilemap import TileMap
from text import Text
from zombie import Zombie

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
                    self.player = Player(j*32 - 32, i*32 + 32, self.platform_group, self.portal_group, self.bullet_group)
                    self.player_group.add(self.player)
        
        self.text = Text(display)

        self.lost_ruby_sound = pygame.mixer.Sound('assets/sounds/lost_ruby.wav')
        self.pickup_ruby_sound = pygame.mixer.Sound('assets/sounds/ruby_pickup.wav')

        pygame.mixer.music.load('assets/sounds/level_music.wav')        
        pygame.mixer.music.set_volume(.5)
        pygame.mixer.music.play(-1, 0.0)

        self.setup_stats()

    def setup_stats(self):
        self.STARTING_ROUND_TIME = 30
        self.STARTING_ZOMBIE_CREATION_TIME = 5
        self.score = 0
        self.round_number = 0
        self.round_time = self.STARTING_ROUND_TIME
        self.frame_count = 0
        self.zombie_createion_time = self.STARTING_ZOMBIE_CREATION_TIME

    def run_game_loop(self):
        self.pause_game('Zombie killer',  "Press 'Enter' to start")        
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player.jump()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.player.shoot()  

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.create_zombie()                                        
            
            self.update()

            self.draw()
            
            pygame.display.update()
            
            self.clock.tick(60)


    def draw(self): 
        self.background.draw()
        self.main_tile_group.draw(self.display)
        self.portal_group.draw(self.display)

        self.player_group.draw(self.display)
        self.bullet_group.draw(self.display)
        self.zombie_group.draw(self.display)
        self.rubie_group.draw(self.display)
        self.text.draw(self.score, self.round_number, self.round_time, self.player.health)

    def update(self): 
        self.frame_count += 1
        if self.frame_count % 60 == 0:
            self.round_time -= 1
            self.frame_count = 0

        self.check_collissions()

        self.main_tile_group.update() 
        self.portal_group.update() 
        self.player_group.update()
        self.bullet_group.update()
        self.zombie_group.update()
        self.rubie_group.update()

        self.add_zombies()

        self.check_round_completion()

    def add_zombies(self):
        if self.frame_count % 60 == 0:
            if self.round_time % self.zombie_createion_time == 0:
                 self.create_zombie()


    def check_collissions(self):
        collisions = pygame.sprite.groupcollide(self.bullet_group, self.zombie_group, True, False)

        if collisions:
            for zombies in collisions.values():
                for zombie in zombies:
                    zombie.hit_sound.play()
                    zombie.animate_death = zombie.is_dead = True


        player_zombie_collisions = pygame.sprite.spritecollide(self.player, self.zombie_group, False)

        if player_zombie_collisions:
            for zombie in player_zombie_collisions:
                if zombie.is_dead:
                    zombie.kick_sound.play()
                    zombie.kill()
                    self.score += 25
                    self.rubie_group.add(Ruby(self.platform_group, self.portal_group))
                else:                    
                    self.player.health -= 20
                    self.player.hit_sound.play()
                    self.player.position.x -= 256 * zombie.direction
                    self.player.rect.bottomleft = self.player.position

        if pygame.sprite.spritecollide(self.player, self.rubie_group, True):
            self.lost_ruby_sound.play()
            self.player.health += 10
            self.score += 100
            self.player.health = min(self.player.STARTING_HEALTH, self.player.health)

        for zombie in self.zombie_group:
            if not zombie.is_dead:
                if pygame.sprite.spritecollide(zombie, self.rubie_group, True):
                    self.lost_ruby_sound.play()
                    self.create_zombie()

    def check_round_completion(self):
        if self.round_time <= 0:
            self.start_new_round()

    def start_new_round(self):
        self.round_number += 1

        if self.round_number < self.STARTING_ZOMBIE_CREATION_TIME:
            self.zombie_createion_time -= 1

        self.frame_count = 0
        self.round_time = self.STARTING_ROUND_TIME

        self.zombie_group.empty()
        self.bullet_group.empty()        
        self.rubie_group.empty()
        self.player.reset()

        self.pause_game('You survived the night', "Press 'Enter' to continue")
        
    def pause_game(self, main_text, helper_text):
        pygame.mixer.music.pause()
        pause = True

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
                    self.run  = pause = False
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    pause = False

            self.display.fill(Colors.BLACK)
            self.text.pause_text(main_text, helper_text)
            pygame.display.update()
            self.clock.tick(60)

        pygame.mixer.music.unpause()


    def check_game_over(self): pass    


    def reset_game(self): pass    

    def create_zombie(self):
        self.zombie_group.add(Zombie(self.platform_group, self.portal_group, self.round_number + 1, self.round_number + 5))