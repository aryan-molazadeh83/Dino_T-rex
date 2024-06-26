import pygame
from random import randint as rnd

def load_obj_rects_details(name):
    with open(name) as file:
        lines = file.readlines()
        lines = [i.strip() for i in lines]
        lines = [i.split(',') for i in lines]
        lines = [[int(j) for j in i] for i in lines]
    return lines
class Obstacles:
    def __init__(self, y, gap, speed, fps):
        self.obs_list = []
        self.y = y
        self.gap = gap
        self.speed = speed
        self.fps = fps
        self.init_obstacles()

    def init_obstacles(self):
        self.obs_list.append(Obstacle((rnd(700, 1000), self.y), self.speed, self.fps))
        self.obs_list.append(Obstacle((rnd(1700, 2000), self.y), self.speed, self.fps))
        #self.obs_list.append(Obstacle((rnd(2000, 2300), self.y), self.speed, self.fps))

    def remove_obstacles(self, state):
        if state == 1:
            self.obs_list.pop(0)
        else:
            self.obs_list.clear()

    def gen_obstacles(self):
        self.obs_list.append(Obstacle((rnd(1700, 2000), self.y), self.speed, self.fps))

    def check(self):
        if self.obs_list[0].x_loc + self.obs_list[0].width < 0:
            self.remove_obstacles(1)
        if self.obs_list[-1].x_loc + self.obs_list[-1].width + self.gap < 1700:
            self.gen_obstacles()


    def update(self, Surface, game_state, game_speed_state):
        if game_state == "Dead":
            self.speed = 8
        if game_speed_state == "Fast":
            self.speed += 4
        elif game_speed_state == "Slow":
            self.speed -= 4
            if self.speed <= 0:
                self.speed = 2
        for obs in self.obs_list:
            obs.update(Surface, game_state,)

class Obstacle:

    Bird1 = pygame.image.load("./Assets/Bird1.png")
    Bird2 = pygame.image.load("./Assets/Bird2.png")



    images_cactus = [
        ["./Assets/LargeCactus1.png", load_obj_rects_details('./Assets/Largecactus1.txt')],
        ["./Assets/LargeCactus2.png", load_obj_rects_details('./Assets/Largecactus2.txt')],
        ["./Assets/LargeCactus3.png", load_obj_rects_details('./Assets/Largecactus3.txt')],
        ["./Assets/SmallCactus1.png", load_obj_rects_details('./Assets/Smallcactus1.txt')],
        ["./Assets/SmallCactus2.png", load_obj_rects_details('./Assets/Smallcactus2.txt')],
        ["./Assets/SmallCactus3.png", load_obj_rects_details('./Assets/Smallcactus3.txt')],
    ]
    def __init__(self, location, speed, fps):
        self.location = location
        self.x_loc, self.y_loc = location
        self.fps = fps
        self.speed = speed

        self.type = rnd(0, len(self.images_cactus) + 1)
        self.bird_loc = rnd(0, 2)
        if self.type >= len(self.images_cactus):
            self.image = self.Bird1
            self.b_state = True
            self.b_counter = 0

            if self.bird_loc == 1:
                self.y_loc -= 55
            elif self.bird_loc == 2:
                self.y_loc -= 100
            else:
                self.y_loc += 4

        else:
            self.image = pygame.image.load(self.images_cactus[self.type][0])
        self.width = self.image.get_width()
        if self.image.get_height() == 95:
            self.y_loc -= 24
        self.rects = self.create_rects()

    def create_rects(self):
        rects = []
        if self.type >= len(self.images_cactus):


            rects.append(pygame.Rect(self.x_loc,
                                    self.y_loc, 92, 62))
        else:
            for rect_details in self.images_cactus[self.type][1:]:
                for rect in range(len(rect_details)):
                    rects.append(pygame.Rect(rect_details[rect][0] + self.x_loc,
                                             rect_details[rect][1] + self.y_loc,
                                             *rect_details[rect][2:]))
        return rects

    def update(self, Surface, game_state):

        if self.type >= len(self.images_cactus):
            if game_state == "Run":
                self.x_loc -= self.speed
                if self.b_counter < self.fps:
                    if self.b_counter % 30 == 0:
                        self.b_state = not self.b_state
                    self.b_counter += 1

                else:
                    self.b_counter = 0
            if self.b_state:
                Surface.blit(self.Bird1, (self.x_loc, self.y_loc))
            else:
                Surface.blit(self.Bird2, (self.x_loc, self.y_loc))
        else:
            if game_state == "Run":
                self.x_loc -= self.speed
            Surface.blit(self.image, (self.x_loc, self.y_loc))
        if game_state == "Run":
            for i in range(len(self.rects)):
                self.rects[i].x -= self.speed
                #pygame.draw.rect(Surface, 'purple', self.rects[i])
