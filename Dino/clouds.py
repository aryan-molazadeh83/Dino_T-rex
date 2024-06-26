import pygame
from random import randint as rnd

class Clouds:
    Cloud = pygame.image.load("./Assets/Cloud.png")

    def __init__(self, speed):
        self.speed = speed
        self.main_dot = 1500
        self.locations = [[rnd(1000, 1500), rnd(50, 300)],
                          [rnd(1500, 2000), rnd(50, 300)],
                          [rnd(2000, 2500), rnd(50, 300)],
                          [rnd(2500, 3000), rnd(50, 300)]
                          ]
    def loc_update(self):
        self.locations.append([rnd(1500, 2000), rnd(50, 300)])

    def update(self, Surface, game_state):
        if game_state == "Run":
            self.locations[0][0] -= self.speed - 3
            self.locations[1][0] -= self.speed - 3
            self.locations[2][0] -= self.speed - 3
            self.locations[3][0] -= self.speed - 3
            self.main_dot -= self.speed - 3
            if self.main_dot == 0:
                self.locations.pop(0)
                self.loc_update()
                self.main_dot += 500

        Surface.blit(self.Cloud, self.locations[0])
        Surface.blit(self.Cloud, self.locations[1])
        Surface.blit(self.Cloud, self.locations[2])
        Surface.blit(self.Cloud, self.locations[3])




