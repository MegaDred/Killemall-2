import time

from utils import width_in_characters, height_in_characters


class Navigate:

    top_border = 0
    bottom_border = height_in_characters
    right_border = width_in_characters
    left_border = 0 

    def __init__(self):
        self.x = 0
        self.y = 0

    def up(self):
        if not self.is_in_permitted_area() or self.y - 1 >= self.top_border:
            self.y -= 1

    def down(self):
        if not self.is_in_permitted_area() or self.y + 1 <= self.bottom_border:
            self.y += 1

    def right(self):
        if not self.is_in_permitted_area() or self.x + 1 <= self.right_border:
            self.x += 1

    def left(self):
        if not self.is_in_permitted_area() or self.x - 1 >= self.left_border:
            self.x -= 1

    def tp(self, x, y):
        if x in range(self.left_border, self.right_border) and y in range(self.top_border, self.bottom_border):
            self.x = x
            self.y = y

    def is_in_permitted_area(self):
        return all((self.y in range(self.top_border, self.bottom_border+1), self.x in range(self.left_border, self.right_border+1)))