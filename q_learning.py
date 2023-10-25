import numpy as np
import pygame as pg

class QLearning:
    def __init__(self, game):
        self.game = game
        self.square_size = (self.game.WINDOW_SIZE//self.game.TILE_SIZE) + 2
        self.possible_actions = 4
        self.q_values = np.zeros((self.square_size, self.square_size, self.possible_actions))
        self.minimun_reward = -1000
        self.normal_reward = -1
        self.current_x = None
        self.current_y = None
        self.old_x = None
        self.old_y = None

        self.action = None

        self.epsilon = 0.9
        self.discount_factor = 0.7
        self.learning_rate = 0.2

        # actions = [up, down, left, right]
        self.actions = [pg.K_w, pg.K_s, pg.K_a, pg.K_d]

    def temporal_difference(self):
        return self.rewards[
            self.old_x, 
            self.old_y
        ] + (self.discount_factor * np.max(self.q_values[self.old_x, self.old_y])) - self.q_values[self.old_x, self.old_y, self.action_index]
    
    def calc_new_q_value(self):
        self.get_current_xy()
        self.q_values[self.old_x, self.old_y, self.action_index] = self.q_values[self.old_x, self.old_y, self.action_index] + (self.learning_rate*self.temporal_difference())

    def get_current_xy(self):
        self.old_x = self.current_x
        self.old_y = self.current_y
        self.current_x = self.snake_xy[0][0]
        self.current_y = self.snake_xy[0][1]

    def create_rewards(self):
        food_xy = self.game.food.segments_xy()
        self.snake_xy = self.game.snake.segments_xy()

        self.rewards = np.full((self.square_size, self.square_size), self.normal_reward)
        self.rewards[food_xy[0], food_xy[1]] = 1000000
        self.rewards[0, :] = self.minimun_reward
        self.rewards[-1, :] = self.minimun_reward
        self.rewards[:, 0] = self.minimun_reward
        self.rewards[:, -1] = self.minimun_reward

        for xy in self.snake_xy:
            self.rewards[xy[0], xy[1]] = self.minimun_reward
        
    def get_next_action(self):
        if np.random.random() < self.epsilon:
            self.action_index = np.argmax(self.q_values[self.snake_xy[0][0], self.snake_xy[0][1]])
        else:
            self.action_index = np.random.randint(4)
    
    def get_next_location(self):
        self.get_current_xy()
        if self.actions[self.action_index] == pg.K_w and self.current_x > 1 and self.game.snake.directions[pg.K_w] == 1:
            self.action = self.actions[self.action_index]
        
        elif self.actions[self.action_index] == pg.K_s and self.current_x > 1 and self.game.snake.directions[pg.K_s] == 1:
            self.action = self.actions[self.action_index]

        elif self.actions[self.action_index] == pg.K_a and self.current_x > 1 and self.game.snake.directions[pg.K_a] == 1:
            self.action = self.actions[self.action_index]

        elif self.actions[self.action_index] == pg.K_d and self.current_x > 1 and self.game.snake.directions[pg.K_d] == 1:
            self.action = self.actions[self.action_index]
