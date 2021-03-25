import pygame
from drone import Drone
from man import Man

pygame.init()

# COLOR CODES
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

# VARIABLES
BLOCK_SIZE = 20
SPEED = 20  # pixels per step
WIDTH = 200
HEIGHT = 200


class GameAI:
    def __init__(self, w=WIDTH, h=HEIGHT):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('BLOCKS_AI')
        self.drone = Drone(20, RED)
        self.man = Man(20, BLUE1)
        self.reset()

        self.clock = pygame.time.Clock()
        self.time = 0

    def reset(self):
        self.drone_x, self.drone_y = self.drone.place_drone(self.h, self.w)
        self.man_x, self.man_y = self.man.place_man(
            self.drone_x, self.drone_y, self.h, self.w)
        self.frame_iteration = 0
        #print(self.drone_x, self.drone_y, self.man_x, self.man_y)

        # return drone_x, drone_y, man_x, man_y

    def play_step(self, action):

        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #print(self.drone_x, self.drone_y)
        self.drone_x, self.drone_y = self.drone.drone_move(self.drone_x, self.drone_y,
                                                           move_distace=20, choice=action)
        #print(self.drone_x, self.drone_y)
        # TODO move man

        game_over = False
        self.reward, game_over = self.get_reward(game_over)

        self.update_ui()

        self.clock.tick(60)

        return self.reward, game_over

    def is_drone_outside(self, drone_x, drone_y):
        if drone_x > self.w - BLOCK_SIZE or drone_x < 0 or drone_y > self.h - BLOCK_SIZE or drone_y < 0:
            return True
        return False

    def is_man_outside(self, man_x, man_y):
        if man_x > self.w - BLOCK_SIZE or man_x < 0 or man_y > self.h - BLOCK_SIZE or man_y < 0:
            return True
        return False

    def get_reward(self, game_over):
        # print(self.drone_x, self.drone_y, self.man_x,
        #       self.man_y, self.frame_iteration, game_over)
        if self.is_drone_outside(self.drone_x, self.drone_y) or self.is_man_outside(self.man_x, self.man_y) or self.frame_iteration > 200:
            game_over = True
            self.reward = -300
            return self.reward, game_over
        elif self.drone_x == self.man_x and self.drone_y == self.man_y:
            game_over = True
            self.reward = 1000
            return self.reward, game_over
        else:
            game_over = False
            self.reward = -1
            return self.reward, game_over

    def update_ui(self):
        self.clock.tick(10)
        self.display.fill(BLACK)

        pygame.draw.rect(self.display, self.man.color, pygame.Rect(
            self.man_x, self.man_y, self.man.size, self.man.size))

        pygame.draw.rect(self.display, self.drone.color, pygame.Rect(
            self.drone_x, self.drone_y, self.drone.size, self.drone.size))

        pygame.display.flip()


# GameAI().get_reward(False)
# GameAI().play_step(3)
