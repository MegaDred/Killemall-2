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
        if not self.is_in_permitted_area() or (self.top_border is None or self.y - 1 >= self.top_border):
            self.y -= 1

    def down(self):
        if not self.is_in_permitted_area() or (self.bottom_border is None or self.y + 1 <= self.bottom_border):
            self.y += 1

    def right(self):
        if not self.is_in_permitted_area() or (self.right_border is None or self.x + 1 <= self.right_border):
            self.x += 1

    def left(self):
        if not self.is_in_permitted_area() or (self.left_border is None or self.x - 1 >= self.left_border):
            self.x -= 1

    def tp(self, x, y):
        if x in range(self.left_border, self.right_border) and y in range(self.top_border, self.bottom_border):
            self.x = x
            self.y = y

    def is_in_permitted_area(self):
        if not (self.top_border is None or self.y >= self.top_border): return False
        if not (self.bottom_border is None or self.y <= self.bottom_border): return False
        if not (self.right_border is None or self.x <= self.right_border): return False
        if not (self.left_border is None or self.x >= self.left_border): return False
        return True