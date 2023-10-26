import pygame as pg
from game_objects import *
import sys
from q_learning import *
import datetime

class Game:
    def __init__(self) -> None:
        pg.init()
        self.WINDOW_SIZE = 500
        self.TILE_SIZE = 10
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.new_game()
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
                pg.quit()
                sys.exit()
            
            self.snake.control(event)

    def create_event(self, key):
        new_event = pg.event.Event(pg.KEYDOWN, key=key)
        pg.event.post(new_event)

    def get_state(self):
        food_xy = self.food.segments_xy()
        snake_xy = self.snake.segments_xy()[0]

        state = []

        state.append(int(food_xy[0] < snake_xy[0]))
        state.append(int(food_xy[0] > snake_xy[0]))
        state.append(int(food_xy[1] < snake_xy[1]))
        state.append(int(food_xy[1] > snake_xy[1]))

        state.append(int(self.snake.current_event == pg.K_w))
        state.append(int(self.snake.current_event == pg.K_a))
        state.append(int(self.snake.current_event == pg.K_s))
        state.append(int(self.snake.current_event == pg.K_d))

        state.append(int(self.snake.can_go_left()))
        state.append(int(self.snake.can_go_right()))
        state.append(int(self.snake.can_go_up()))
        state.append(int(self.snake.can_go_down()))

        return tuple(state)

    def step(self, action):
        self.create_event(action)
        self.check_event()
        self.update()
        self.draw()
        return self.get_state(), self.snake.calc_reward(), self.snake.calc_is_done()

if __name__ == '__main__':
    game = Game()
    agent = QLearning(game)
    agent.train()
    # agent.test()