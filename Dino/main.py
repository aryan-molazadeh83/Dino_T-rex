import pygame
import sys

from Dino import Dino
from colors import *
from track import Track
from obstacles import Obstacles
from clouds import Clouds
from day_changer import Day_or_night
from speed_potion import SpeedPotion

class Game:
    fps = 60
    game_speed = 8
    DinoStart = pygame.image.load("./Assets/DinoStart.png")
    Game_over = pygame.image.load("./Assets/GameOver.png")
    Game_reset = pygame.image.load("./Assets/Reset.png")
    Game_pause = pygame.image.load("./Assets/pause.png")
    immunity_img = pygame.image.load("./Assets/immunity_potion.png")

    Game_story1 = pygame.transform.scale(pygame.image.load("./story/1.png"), (600, 600))
    Game_story2 = pygame.transform.scale(pygame.image.load("./story/2.png"), (600, 600))
    Game_story3 = pygame.transform.scale(pygame.image.load("./story/3.png"), (850, 550))
    Game_story4 = pygame.transform.scale(pygame.image.load("./story/4.png"), (840, 600))
    Game_story5 = pygame.transform.scale(pygame.image.load("./story/5.png"), (1000, 540))
    Game_story6 = pygame.transform.scale(pygame.image.load("./story/6.png"), (600, 600))

    def __init__(self):
        pygame.init()

        self.jump_sound = pygame.mixer.Sound("./sounds/jump.mp3")
        self.immunity_sound = pygame.mixer.Sound("./sounds/immunity_potion.mp3")


        self.game_display = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("Dino T-Rex")
        self.start_font = pygame.font.Font(None, 70)
        self.restart_font = pygame.font.Font(None, 40)
        self.start_text = self.start_font.render("Press any Key to Start", True, BLACK)
        self.font = pygame.font.Font(None, 30)
        self.pause_text = self.font.render("Press any Key to continue", True, BLACK)


        self.score = 0
        self.day = Day_or_night(self.fps, 33)
        self.obss = Obstacles(400, 700, self.game_speed, 60)
        self.track = Track(self.game_speed, 450)
        self.speed_potion = SpeedPotion(self.game_speed)
        self.high_score = self.load_high_score()
        self.high_score_int = int(self.high_score)
        self.main_character = Dino((100, 380), self.fps)
        self.clock = pygame.time.Clock()
        self.clouds = Clouds(5)

        self.story()

    def score_board(self):
        score = str(int(self.score))
        _score = self.font.render((5 - len(score)) * '0' + score, True, self.cur_color)
        _high_score = self.font.render('HI   ' + self.high_score, True, self.cur_color)
        self.game_display.blit(_score, (1050, 40))
        self.game_display.blit(_high_score, (900, 40))


    def load_high_score(self):
        with open("save_high_score.txt", 'r') as file:
            high_score = file.read()
            return high_score

    def new_high_score(self):
        if self.score > int(self.high_score):
            with open("save_high_score.txt", 'w') as file:
                _str = (5 - len(str(self.score))) * '0' + str(self.score)
                file.write(_str)

    def story(self):
        pic_num = 1
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    pic_num += 1
            self.game_display.fill(WHITE)
            if pic_num == 1:
                self.game_display.blit(self.Game_story1, (300, 0))

            elif pic_num == 2:
                self.game_display.blit(self.Game_story2, (300, 0))

            elif pic_num == 3:
                self.game_display.blit(self.Game_story3, (175, 25))

            elif pic_num == 4:
                self.game_display.blit(self.Game_story4, (180, 0))

            elif pic_num == 5:
                self.game_display.blit(self.Game_story5, (100, 30))

            elif pic_num == 6:
                self.game_display.blit(self.Game_story6, (300, 0))
            else:
                self.pre_run()
            pygame.display.update()


    def pre_run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.run()

            self.game_display.fill((255, 255, 255))

            self.game_display.blit(self.font.render('HI   ' + self.high_score, True, BLACK), (1000, 40))
            self.game_display.blit(self.start_text, (330, 370))
            self.game_display.blit(self.DinoStart, (551, 230))
            self.clock.tick(self.fps)
            pygame.display.update()
    def run(self):
        game_state = "Run"
        game_speed_state = "Normal"
        revive_state = False
        immunity_state = False

        while True:
            self.cur_color = self.day.update(self.game_display, game_state)
            self.restart_text = self.restart_font.render("Press R to Restart", True, self.cur_color)
            self.score_board()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        if game_state == "Run" and self.score >= 4000:
                            self.immunity_sound.play()
                            immunity_state = True
                    if game_state == "Pause":
                        game_state = "Run"
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.main_character.jump()
                        if game_state == "Run":
                            self.jump_sound.play()
                    #elif event.key == pygame.K_DOWN:
                        #self.main_character.duck()

                    if event.key == pygame.K_r:
                        if game_state == "Run":
                            pass
                        elif game_state == "Dead":
                            #self.restart_game()
                            game_state = "Run"
                            self.score = 0
                            self.obss.remove_obstacles(2)
                            self.obss.init_obstacles()

                    if event.key == pygame.K_p:
                        if game_state == "Run":
                            game_state = "Pause"

            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                self.main_character.duck()


            self.track.update(self.game_display, game_state, game_speed_state)
            self.speed_potion.update(self.game_display, game_state, game_speed_state)
            self.clouds.update(self.game_display, game_state)


            states = self.main_character.update(self.game_display, self.obss, self.speed_potion, game_state, revive_state, immunity_state)
            game_state = states[0]
            game_speed_state = states[1]
            revive_state = states[2]
            immunity_state = states[3]

            if immunity_state:
                self.game_display.blit(self.immunity_img, (1000, 520))

            if game_state == "Dead":
                if revive_state:
                    self.obss.remove_obstacles(2)
                    self.obss.init_obstacles()
                    revive_state = False
                    game_state = "Run"
                else:
                    self.new_high_score()
                    self.high_score = self.load_high_score()
                    self.game_display.blit(self.Game_over, (407, 240))
                    self.game_display.blit(self.Game_reset, (562, 280))
                    self.game_display.blit(self.restart_text, (475, 360))
            self.obss.update(self.game_display, game_state, game_speed_state)
            self.obss.check()
            if game_speed_state != "Normal":
                self.obss.remove_obstacles(2)
                self.obss.init_obstacles()
            if game_state == "Run":
                self.score += 1

            if game_state == "Pause":
                self.game_display.blit(self.Game_pause, (550, 240))
                self.game_display.blit(self.pause_text, (470, 350))






            pygame.display.update()
            self.clock.tick(self.fps)

    #def restart_game(self):

new_game = Game()