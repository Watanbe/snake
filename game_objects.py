import pygame as pg
from random import randrange


vec2 = pg.math.Vector2

class Snake:
    def __init__(self, game) -> None:
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.rect.center = self.get_random_position()
        self.direction = vec2(0, 0)
        self.step_delay = 100
        self.time = 0
        self.length = 1
        self.segments = []
        self.directions = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
        self.current_event = None
        self.touch_border = False
        self.eat_itself = False
        self.ate_food = False
        self.delta_time_return = True

    def control(self, event):
        if event.type == pg.KEYDOWN:
            self.current_event = event
            if event.key == pg.K_w and self.directions[pg.K_w]:
                self.direction = vec2(0, -self.size)
                self.directions = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}

            if event.key == pg.K_s and self.directions[pg.K_s]:
                self.direction = vec2(0, self.size)
                self.directions = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
            
            if event.key == pg.K_a and self.directions[pg.K_a]:
                self.direction = vec2(-self.size, 0)
                self.directions = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
            
            if event.key == pg.K_d and self.directions[pg.K_d]:
                self.direction = vec2(self.size, 0)
                self.directions = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}

            if event.key == pg.K_l:
                if self.delta_time_return:
                    self.delta_time_return = False
                else:
                    self.delta_time_return = True

    def segments_xy(self):
        return [((self.rect.centerx//self.size) + 1, (self.rect.centery//self.size) + 1)]

    def delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time > self.step_delay:
            self.time = time_now
            return True
        return self.delta_time_return

    def get_random_position(self):
        return [randrange(self.size // 2, self.game.WINDOW_SIZE - self.size // 2, self.size)] * 2

    def check_borders(self):
        if self.rect.left < 0 or self.rect.right > self.game.WINDOW_SIZE:
            self.touch_border = True
        if self.rect.top < 0 or self.rect.bottom > self.game.WINDOW_SIZE:
            self.touch_border = True

    def check_food(self):
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
            self.length += 1
            self.ate_food = True

    def check_selfeating(self):
        if len(self.segments) != len(set(segment.center for segment in self.segments)):
            self.eat_itself = True

    def move(self):
        if self.delta_time():
            self.rect.move_ip(self.direction)
            self.segments.append(self.rect.copy())
            self.segments = self.segments[-self.length:]

    def update(self) -> None:
        self.check_selfeating()
        self.check_borders()
        self.check_food()
        self.move()
        self.segments_xy()

    def draw(self) -> None:
        [pg.draw.rect(self.game.screen, 'green', segment) for segment in self.segments]

    def calc_reward(self):
        if (self.touch_border or self.eat_itself):
            return -10
        elif self.ate_food:
            self.ate_food = False
            return 1
        return 0
    
    def calc_is_done(self):
        return self.touch_border or self.eat_itself
    
    def can_go_left(self):
        if (self.rect.left <= 0):
            return False
        return True
    
    def can_go_right(self):
        if (self.rect.right >= self.game.WINDOW_SIZE):
            return False
        return True
    
    def can_go_up(self):
        if (self.rect.top <= 0):
            return False
        return True
    
    def can_go_down(self):
        if (self.rect.bottom >= self.game.WINDOW_SIZE):
            return False
        return True


class Food:
    def __init__(self, game) -> None:
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.rect.center = self.game.snake.get_random_position()

    def update(self) -> None:
        self.segments_xy()

    def draw(self) -> None:
        pg.draw.rect(self.game.screen, 'red', self.rect)

    def segments_xy(self):
        return ((self.rect.centerx//self.size) + 1, (self.rect.centery//self.size) + 1)