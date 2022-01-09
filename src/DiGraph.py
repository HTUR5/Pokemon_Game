from GraphInterface import GraphInterface
from random import random as rnd
from Node import Node

class DiGraph(GraphInterface):

    def __init__(self):
        self.nodes = dict()
        self.edgesInto = dict()
        self.edgesOut = dict()
        self.countEdge = 0
        self.mc = 0

    def v_size(self) -> int:
        return len(self.nodes)

    def e_size(self) -> int:
        return self.countEdge

    def get_all_v(self) -> dict:
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.edgesInto[id1]

    def all_out_edges_of_node(self, id1: int) -> dict:
        if id1 in self.edgesOut.keys():
            return self.edgesOut[id1]
        return None

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 in self.nodes.keys() and id2 in self.nodes.keys():
            self.nodes[id1].size_of_out =  self.nodes[id1].size_of_out + 1
            self.nodes[id2].size_of_into = self.nodes[id2].size_of_into + 1
            if not bool(self.edgesOut.get(id1)):
                self.edgesOut[id1] = {}
            self.edgesOut[id1][id2] = weight
            if not bool(self.edgesInto.get(id2)):
                self.edgesInto[id2] = {}
            self.edgesInto[id2][id1] = weight
            self.countEdge = self.countEdge + 1
            self.mc = self.mc+1
            return True
        return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        node = Node(node_id, pos)
        # if pos == None:
            # pos = tuple(map(float, random(), random(), random()))
        if node_id in self.nodes.keys():
            return False
        self.nodes[node_id] = node
        self.mc = self.mc + 1
        return True

    def remove_node(self, node_id: int) -> bool:
        if node_id in self.nodes.keys():
            if node_id in self.edgesOut.keys():
                for i in dict(self.edgesOut[node_id]).keys():
                    self.remove_edge(node_id,i)
            if node_id in self.edgesInto.keys():
                for i in dict(self.edgesInto[node_id]).keys():
                    self.remove_edge(i,node_id)
            del self.nodes[node_id]
            self.mc = self.mc+1
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 in self.edgesOut.keys() and node_id2 in self.edgesOut[node_id1].keys():
            self.nodes[node_id1].size_of_out = self.nodes[node_id1].size_of_out - 1
            self.nodes[node_id2].size_of_into = self.nodes[node_id2].size_of_into - 1
            del self.edgesOut[node_id1][node_id2]
            self.countEdge = self.countEdge - 1
            if not self.edgesOut[node_id1]:
                del self.edgesOut[node_id1]
            del self.edgesInto[node_id2][node_id1]
            if not self.edgesInto[node_id2]:
                del self.edgesInto[node_id2]
            self.mc = self.mc + 1
            return True
        return False

    def __repr__(self):
        return f'|V| = {self.v_size()} |E| = {self.e_size()}'



