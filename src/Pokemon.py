import json
from src.GraphAlgo import GraphAlgo
from src.Node import Node
class Pokemon:

    def __init__(self, value, type, edge: list, pos: list):
        self.value = value
        self.type = type
        self.edge = edge
        self.pos = pos
        # self.available = False

    def __repr__(self) -> str:
        return "{{'Pokemon': value:{} type:{} pos:{}}}" \
            .format(self.value, self.type, self.pos)



