import pygame
class Track:
    img = pygame.image.load("./Assets/Track.png")

    def __init__(self, speed, y):
        self.speed = speed
        self.locs = [[0, y], [2404, y]]
    def update(self, Surface, game_state, game_speed_state):

        if game_state == "Run":
            if game_speed_state == "Fast":
                self.speed += 4
            elif game_speed_state == "Slow":
                self.speed -= 4
                if self.speed <= 0:
                    self.speed = 2
            self.locs[0][0] -= self.speed
            self.locs[1][0] -= self.speed
            if self.locs[0][0] <= -2404:
                self.locs[0][0] = 2404
            if self.locs[1][0] <= -2404:
                self.locs[1][0] = 2404
        if game_state == "Dead":
            self.speed = 8

        Surface.blit(self.img, self.locs[0])
        Surface.blit(self.img, self.locs[1])
