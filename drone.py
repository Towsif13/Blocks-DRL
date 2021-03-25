class Drone:
    def __init__(self, size, color):
        self.size = size
        self.color = color

    def place_drone(self, screen_width, screen_height):
        x = 0 + self.size + 20
        y = screen_height - self.size - 20

        return x, y

    def drone_move(self, x, y, move_distace, choice):
        if choice == 0:  # left
            x -= move_distace
        if choice == 1:  # right
            x += move_distace
        if choice == 2:  # up
            y += move_distace
        if choice == 3:  # down
            y -= move_distace

        return x, y

        # if direction == pygame.K_LEFT:
        #     self.x -= move_distace
        # if direction == pygame.K_RIGHT:
        #     self.x += move_distace
        # if direction == pygame.K_DOWN:
        #     self.y += move_distace
        # if direction == pygame.K_UP:
        #     self.y -= move_distace
