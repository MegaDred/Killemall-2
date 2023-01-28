import time

from utils import width_in_characters, height_in_characters


class Navigate:
    def __init__(self):

        self.area_top_border = 0
        self.area_bottom_border = height_in_characters
        self.area_right_border = width_in_characters
        self.area_left_border = 0

        self.x = 0
        self.y = 0

    def up(self):
        if self.y - 1 >= self.area_top_border:
            self.y -= 1

    def down(self):
        if self.y + 1 <= self.area_bottom_border:
            self.y += 1 

    def right(self):
        if self.x + 1 <= self.area_right_border:
            self.x += 1 

    def left(self):
        if self.x - 1 >= self.area_left_border:
            self.x -= 1

    def tp(self, x, y):
        if x in range(self.area_left_border, self.area_right_border) and y in range(self.area_top_border, self.area_bottom_border):
            self.x = x
            self.y = y
