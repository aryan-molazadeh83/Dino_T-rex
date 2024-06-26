import pygame


class Day_or_night:
    def __init__(self, fps, length):
        self.threshold = fps * length
        self.counter = 0
        self.state = 'Day'
        self.c = 255
        self.transition_speed = 3
        self.transition_time = False
    def update(self, Surface, game_state):
        if self.transition_time:
            self.c += self.transition_speed
        if self.c >= 255 - self.transition_speed or self.c < 0 - self.transition_speed:
            self.transition_speed *= -1
            self.transition_time = False
        Surface.fill((self.c, self.c, self.c))
        self._update(game_state)
        return (255, 255, 255) if self.transition_speed >= 0 else (0, 0, 0)

    def _update(self, game_state):
        if game_state == "Run":
            if not self.transition_time:
                if self.counter >= self.threshold:
                    self.transition_time = True
                    self.counter = 0
                else:
                    self.counter += 1
        else:
            self.counter = 0