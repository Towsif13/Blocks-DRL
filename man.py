class Man:
    def __init__(self, size, color):
        self.size = size
        self.color = color

    def place_man(self, drone_x, drone_y, screen_width, screen_height):
        x = screen_width - self.size - 20
        y = 0 + self.size + 20

        return x, y

    def move_man(self, man_x, man_y, pixel_per_step, direction):
        if direction == 'left':
            man_x -= pixel_per_step
        if direction == 'right':
            man_x += pixel_per_step
        if direction == 'down':
            man_y += pixel_per_step
        if direction == 'up':
            man_y -= pixel_per_step

        return man_x, man_y
