import numpy as np
import pygame as pg
import random
import pickle
import time
class QLearning:
    def __init__(self, game):
        self.env = game
        self.q_values = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4))

        self.epsilon = 1
        self.epsilon_discount = 0.592
        self.min_epsilon = 0.001

        self.discount_factor = 0.83
        self.learning_rate = 0.001

        # actions = [up, down, left, right]
        self.actions = [pg.K_w, pg.K_s, pg.K_a, pg.K_d]

        self.num_episodes = 10001

    def get_action(self, state):
        if random.random() < self.epsilon:
            return random.choice([0, 1, 2, 3])
        return np.argmax(self.q_values[state])
    
    def update_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_discount, self.min_epsilon)

    def train(self):
        max_tam = 0
        # for i in range(1, self.num_episodes):
        while max_tam < 15:
            counter = 0
            current_state = self.env.get_state()
            self.update_epsilon()
            done = False
            snake_size = 1

            while not done:
                action = self.get_action(current_state)
                new_state, reward, done = self.env.step(self.actions[action])

                self.q_values[current_state][action] = (1 - self.learning_rate)\
                    * self.q_values[current_state][action] + self.learning_rate\
                    * (reward + self.discount_factor * max(self.q_values[new_state]))

                counter += 1

                if (snake_size%15 == 0 and snake_size > max_tam):
                    with open(f'pickle/{snake_size}.pickle', 'wb') as file:
                        pickle.dump(self.q_values, file)

                current_state = new_state

                if snake_size != self.env.snake.length:
                    counter = 0
                
                if (counter == 1000):
                    counter = 0
                    # self.epsilon = 0.7
                    done = True

                snake_size = self.env.snake.length

            max_tam = max(max_tam, snake_size)
            # print(f"Iteração {i}, tamanho: {snake_size}, tamanho máximo: {max_tam}")
            print(f"tamanho: {snake_size}, tamanho máximo: {max_tam}, epsilon: {self.epsilon}")
            self.env.new_game()


    def test(self):
        file = open('pickle/70.pickle', 'rb')
        self.q_values = pickle.load(file)

        current_state = self.env.get_state()
        done = False
        self.epsilon = 0

        while not done:
            action = self.get_action(current_state)
            new_state, _, done = self.env.step(self.actions[action])                
            current_state = new_state

            time.sleep(0.1)
        print(self.env.snake.length)