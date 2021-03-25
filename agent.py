import torch
import random
import numpy as np
from collections import deque

from torch._C import dtype
from game import GameAI
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
num_episode = 50000
SHOW_EVERY = 200


class Agent:
    def __init__(self):
        self.epsilion = 0.999
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(2, 256, 4)
        self.trainer = QTrainer(self.model, LR, self.gamma)
        self.epsilion_decay_value = 0.998

    def get_state(self, game):
        # drone = game.drone
        # [game.drone_x, game.drone_y, game.man_x, game.man_y]
        state = [game.drone_x, game.drone_y]

        return np.array(state, dtype=int)

    def get_action(self, state, episode):
        self.epsilion *= self.epsilion_decay_value

        if np.random.random() < self.epsilion:
            # take random action
            move = np.random.randint(0, 4)
            return move
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            return move

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)


def train():

    agent = Agent()
    game = GameAI()

    for episode in range(num_episode):

        state_old = agent.get_state(game)

        final_move = agent.get_action(state=state_old, episode=episode)

        reward, done = game.play_step(final_move)

        state_new = agent.get_state(game)

        agent.train_short_memory(
            state=state_old, action=final_move, reward=reward, next_state=state_new, done=done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.train_long_memory()

        print(
            f'Episode: {episode} Reward: {reward} Epsilon: {agent.epsilion:.4f}')


if __name__ == '__main__':
    train()
# # %%
# import torch
# pred = torch.tensor([133, 16, 7, 18])
# move = torch.argmax(pred).item()
# print(move)
