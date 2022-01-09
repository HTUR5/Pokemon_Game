import json

class Agent:

    def __init__(self, _id: int, value, src, dest, speed, pos: list = []):
        self._id = _id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos

    def __repr__(self) -> str:
        return "{{'Agent': id:{} value:{} src:{} dest:{} speed:{} pos:{}}}" \
            .format(self.id,self.value, self.src, self.dest, self.speed, self.pos)

