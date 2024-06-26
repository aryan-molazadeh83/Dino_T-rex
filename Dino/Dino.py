import pygame
from random import randint as rnd

class Dino:
    dino_walk1 = pygame.image.load("./Assets/DinoRun1.png")
    dino_walk2 = pygame.image.load("./Assets/DinoRun2.png")
    dino_duck1 = pygame.image.load("./Assets/DinoDuck1.png")
    dino_duck2 = pygame.image.load("./Assets/DinoDuck2.png")
    dino_dead = pygame.image.load("./Assets/DinoDead.png")
    dino_jump = pygame.image.load("./Assets/DinoJump.png")
    revive_img = pygame.image.load("./Assets/revive_potion.png")
    rect_vals = [[40, 0, 48, 30],
                 [0, 30, 12, 28],
                 [30, 30, 50, 8],
                 [24, 38, 48, 16],
                 [12, 42, 12, 28],
                 [23, 54, 40, 16],
                 [16, 70, 40, 19]]

    def __init__(self, location, fps):
        self.die_sound = pygame.mixer.Sound("./sounds/die.mp3")
        self.speed_sound = pygame.mixer.Sound("./sounds/speed_potion.mp3")
        self.revive_sound = pygame.mixer.Sound("./sounds/revive_potion.mp3")
        self.font = pygame.font.Font(None, 30)
        self.hint_text = self.font.render("Press H to revive", True, (0, 0, 0))

        self.location = location
        self.x_loc, self.y_loc = location
        self.Y_Loc = self.y_loc
        self.fps = fps


        self.score = 0
        self.immunity_counter = 0

        self.w_img = True
        self.w_slicer = 10
        self.w_counter = 0

        self.state = 1

        self.max_jump = self.y_loc - 250
        self.Y_Direction = 8
        self.y_direction = self.Y_Direction
        self.rects = self.creat_rect()

    def creat_rect(self):
        rects = []
        for rect in self.rect_vals:
            rects.append(pygame.Rect(rect[0] + self.x_loc, rect[1] + self.y_loc, rect[2], rect[3]))
        return rects

    def update_rects(self):
        if self.state == 3:
            for i in range(len(self.rects)):
                self.rects[i].y -= self.y_direction


    def update(self, Surface, objs, speed_obj, state, revive_state, immunity_state):
        self.immunity_state = immunity_state
        if self.score % 4000 == 0:
            self.immunity_counter = 0
        if self.immunity_state:
            self.immunity_counter += 1
        if self.immunity_counter >= 900:
            self.immunity_state = False
        if self.score >= 4000 and not self.immunity_state and self.immunity_counter == 0:
            Surface.blit(self.hint_text, (900, 500))

        self.revive_state = revive_state
        self.score += 1
        if self.score % 1000 == 0:
            self.revive_sound.play()
            self.revive_state = True
        if self.revive_state:
            Surface.blit(self.revive_img, (1100, 520))

        self.speed_state = rnd(1, 2)


        if state == "Dead":
            Surface.blit(self.dino_dead, (self.x_loc, self.y_loc))

            if not revive_state:
                self.score = 0
                self.Y_Direction = 8
            return ["Dead", "Normal", self.revive_state, self.immunity_state]
        if state == "Pause":
            Surface.blit(self.dino_walk1, (self.x_loc, self.y_loc))
            return ["Pause", "Normal", self.revive_state, self.immunity_state]
        self.rect = self.dino_duck1.get_rect(topleft=(self.x_loc, self.y_loc + 34))
        if self.state != 2:
            #for rect in self.rects:
                #pygame.draw.rect(Surface, 'red', rect)
            if not immunity_state:
                for i in range(len(objs.obs_list)):
                    for obj_rects in objs.obs_list[i].rects:
                        for dino_rects in self.rects:
                            if dino_rects.colliderect(obj_rects):
                                self.die_sound.play()
                                if not revive_state:
                                    self.score = 0
                                return ["Dead", "Normal", self.revive_state, self.immunity_state]

            for dino_rects in self.rects:
                if dino_rects.colliderect(speed_obj.rect):
                    self.speed_sound.play()
                    if self.speed_state == 1:
                        self.Y_Direction += 4
                        return ["Run", "Fast", self.revive_state, self.immunity_state]
                    elif self.speed_state == 2:
                        self.Y_Direction -= 4
                        return ["Run", "Slow", self.revive_state, self.immunity_state]

        else:
            #pygame.draw.rect(Surface, 'red', self.rect)
            if not immunity_state:
                for i in range(len(objs.obs_list)):
                    for obj_rects in objs.obs_list[i].rects:
                        if self.rect.colliderect(obj_rects):
                            self.die_sound.play()
                            if not revive_state:
                                self.score = 0
                            return ["Dead", "Normal", self.revive_state, self.immunity_state]
            for dino_rects in self.rects:
                if dino_rects.colliderect(speed_obj.rect):
                    self.speed_sound.play()
            for dino_rects in self.rects:
                if dino_rects.colliderect(speed_obj.rect):
                    self.speed_sound.play()
                    if self.speed_state == 1:
                        self.Y_Direction += 4
                        return ["Run", "Fast", self.revive_state, self.immunity_state]
                    elif self.speed_state == 2:
                        self.Y_Direction -= 4
                        if self.Y_Direction <= 0:
                            self.Y_Direction = 2
                        return ["Run", "Slow", self.revive_state, self.immunity_state]



        if self.state == 1:
            if self.w_counter < self.fps:
                if self.w_counter % self.w_slicer == 0:
                    self.w_img = not self.w_img
                self.w_counter += 1

            else:
                self.w_counter = 0
            if self.w_img == True:
                Surface.blit(self.dino_walk1, self.location)
            else:
                Surface.blit(self.dino_walk2, self.location)

        elif self.state == 3:

            if self.y_direction > 0:
                if self.y_loc < self.max_jump:
                    self.y_direction *= -1
            else:
                if self.y_loc > self.Y_Loc:
                    self.state = 1
                    for i in range(len(self.rects)): #تنظیم مکان چهارضلعی ها
                        self.rects[i].y -= 8
                    self.y_direction = self.Y_Direction
            self.y_loc -= self.y_direction
            Surface.blit(self.dino_jump, (self.x_loc, self.y_loc))
            self.rect.topleft = (self.x_loc, self.y_loc)

        elif self.state == 2:
            #self.rect = self.dino_duck1.get_rect(topleft=(self.x_loc, self.y_loc + 34))
            if self.w_counter < 0.2 * self.fps:
                if self.w_counter % self.w_slicer == 0:
                    self.w_img = not self.w_img
                self.w_counter += 1

            else:
                #self.rect = self.dino_walk1.get_rect(topleft=self.location)
                self.w_counter = 0
                self.state = 1
            if self.w_img == True:
                Surface.blit(self.dino_duck1, (self.x_loc, self.y_loc + 34))
            else:
                Surface.blit(self.dino_duck2, (self.x_loc, self.y_loc + 34))
        self.update_rects()
        return ["Run", "Normal", self.revive_state, self.immunity_state]



    def jump(self):
        self.state = 3

    def duck(self):
        if self.state != 3:
            self.state = 2

    def walk(self):
        self.state = 1


