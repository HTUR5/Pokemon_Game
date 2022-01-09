from typing import Any
import math

class Node:

    def __init__(self, i, pos: tuple = None):
        self._id = i
        self.pos = pos
        self.tag = 0
        self.size_of_out = 0
        self.size_of_into = 0

    def get_pos(self):
        return self.pos

    def set_pos(self, pos: tuple):
        self.pos = pos

    def distance(self, pos: list):
        return math.sqrt(math.pow(self.pos[0]- pos[0],2) + math.pow(self.pos[1]- pos[1],2) + math.pow(self.pos[2]- pos[2],2))


    def __repr__(self):
        return f'{self._id}: |edges_out| {self.size_of_out} |edges in| {self.size_of_into}'





