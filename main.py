import pygame as pg
from game_objects import *
import sys
from q_learning import *
import datetime

class Game:
    def __init__(self) -> None:
        pg.init()
        self.WINDOW_SIZE = 500
        self.TILE_SIZE = 50
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.new_game()
        self.learning = QLearning(self)
        self.begin_time = None
        
    def draw_grid(self):
        [
            pg.draw.line(
                self.screen, 
                [50] * 3, 
                (x, 0), 
                (x, self.WINDOW_SIZE)
            ) 
            for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE)
        ]

        [
            pg.draw.line(
                self.screen, 
                [50] * 3, 
                (0, y), 
                (self.WINDOW_SIZE, y)
            ) 
            for y in range(0, self.WINDOW_SIZE, self.TILE_SIZE)
        ]
    
    def new_game(self) -> None:
        self.begin_time = datetime.datetime.now()
        self.snake = Snake(self)
        self.food = Food(self)

    def update(self) -> None:
        self.snake.update()
        self.food.update()
        pg.display.flip()
        # self.clock.tick(60)

    def draw(self) -> None:
        self.screen.fill('black')
        self.draw_grid()
        self.food.draw()
        self.snake.draw()

    def check_event(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print(self.learning.q_values)
                print(self.learning.rewards)
                pg.quit()
                sys.exit()
            
            self.snake.control(event)

    def create_event(self, key):
        new_event = pg.event.Event(pg.KEYDOWN, key=key)
        pg.event.post(new_event)

    def run(self) -> None:
        maxSegements = -1
        while True:
            self.learning.create_rewards()
            self.learning.get_next_action()
            self.learning.get_next_location()
            if self.learning.action != None:
                self.create_event(self.learning.action)

            self.check_event()
            self.update()
            self.learning.calc_new_q_value()
            self.draw()
            if maxSegements < max(maxSegements, len(self.snake.segments)):
                maxSegements = max(maxSegements, len(self.snake.segments))
                print(maxSegements)

if __name__ == '__main__':
    game = Game()
    game.run()