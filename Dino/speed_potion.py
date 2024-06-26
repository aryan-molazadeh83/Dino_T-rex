import pygame

class SpeedPotion:
    image = pygame.image.load(("./Assets/speed.png"))


    def __init__(self, speed):
        self.speed = speed
        self.loc = [-70, 380]
        self.rect = self.image.get_rect(topleft=(self.loc[0], self.loc[1]))
        self.x_loc, self.y_loc = self.loc

    def update(self, Surface, game_state, game_speed_state):
        if game_speed_state != "Normal":
            self.loc[0] = -70
            self.rect.x = -70
        if game_speed_state == "Fast":
            self.speed += 4
        elif game_speed_state == "Slow":
            self.speed -= 4
            if self.speed <= 0:
                self.speed = 2


        if game_state == "Run":
            if game_speed_state == "Normal":
                self.loc[0] -= self.speed
                if self.loc[0] <= -100:
                    self.loc[0] = 5900
                self.rect.x -= self.speed
                if self.rect.x <= -100:
                    self.rect.x = 5900
            elif game_speed_state == "Fast":
                self.loc[0] -= self.speed
                if self.loc[0] <= -100:
                    self.loc[0] = 11900
                self.rect.x -= self.speed
                if self.rect.x <= -100:
                    self.rect.x = 11900
            elif game_speed_state == "Slow":
                self.loc[0] -= self.speed
                if self.loc[0] <= -100:
                    self.loc[0] = 2900
                self.rect.x -= self.speed
                if self.rect.x <= -100:
                    self.rect.x = 2900
            #pygame.draw.rect(Surface, 'red', self.rect)
        elif game_state == "Dead":
            self.loc[0] = -70
            self.rect.x = -70
            self.speed = 8

        Surface.blit(self.image, self.loc)

