from abc import ABC, abstractmethod
from typing import List
# import matplotlib.pyplot as plt
from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface
from DiGraph import DiGraph
import json
from random import Random as rnd
from heapq import heappush, heappop
import random
from Node import Node
import sys


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph = None):
        self.graph = DiGraph()
        if graph is not None:
            self.graph = graph

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, graph1: str) -> bool:
        dict = json.loads(graph1)
        self.graph = DiGraph()
        for node in dict['Nodes']:
            pos = None
            if 'pos' in node:
                pos = tuple(map(float, node['pos'].split(',')))
            self.graph.add_node(int(node['id']), pos)

        for edge in dict['Edges']:
            self.graph.add_edge(int(edge['src']), int(edge['dest']), float(edge['w']))

        return True

    def save_to_json(self, file_name: str) -> bool:
        dict = {'Edges': [], 'Nodes': []}
        for key, node in self.graph.get_all_v().items():
            dict['Nodes'].append({'pos': str(node.pos)[1:-1].replace(' ', ''), 'id': key})

        for src in self.graph.get_all_v().keys():
            if src in self.graph.edgesOut.keys():
                for dest, w in self.graph.all_out_edges_of_node(src).items():
                    dict['Edges'].append({'src': src, 'w': w, 'dest': dest})

        with open(file_name, 'w') as to_save:
            json.dump(dict, to_save)

        return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        nodes = self.graph.get_all_v().keys()
        paths = {id1: [id1]}
        push = heappush
        pop = heappop
        dist = {}
        visited = {}
        q = []
        if id1 not in nodes:
            return float('inf'), []
        visited[id1] = 0
        push(q, (0, id1))
        while q:
            (d, src) = pop(q)
            if src in dist:
                continue
            dist[src] = d
            if src == id2:
                break
            if src in  self.graph.edgesOut.keys():
                for dest, w in self.graph.all_out_edges_of_node(src).items():
                    sToD = dist[src] + w
                    if dest in dist:
                        if sToD < dist[dest]:
                            raise ValueError("")
                    elif dest not in visited or sToD < visited[dest]:
                        visited[dest] = sToD
                        push(q, (sToD, dest))
                        if src not in paths:
                            paths[src] = [src]
                        paths[dest] = paths[src] + [dest]
        if id2 in dist and id2 in paths:
            return dist[id2], paths[id2]
        return float('inf'), []

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        addNode = node_lst[0]
        minList = []
        if len(node_lst) == 0:
            return minList, 0
        minList.append(node_lst[0])
        finall_weight = 0
        while len(node_lst) > 0:
            min = float('inf')
            cur_node = minList[len(minList) - 1]
            if cur_node in node_lst:
                node_lst.remove(cur_node)
            for i in node_lst:
                if i in self.graph.all_out_edges_of_node(cur_node).keys():
                    weight = self.graph.all_out_edges_of_node(cur_node)[i]
                    toMerge = None

                else:
                    # there is no edge
                    (weight, toMerge) = self.shortest_path(cur_node, i)
                if (weight != float('inf')):
                    if weight < min:
                        min = weight
                        node = i
                        addNode = toMerge

            finall_weight = finall_weight + min
            if addNode != None:
                for k in range(1, len(addNode) - 1):
                    item = addNode.__getitem__(k)
                    minList.append(item)
            minList.append(node)
            node_lst.remove(node)
        return minList, finall_weight

    def centerPoint(self) -> (int, float):
        min = float('inf')
        centerOfGraph = None
        for node in self.graph.nodes.keys():
            max = -float('inf')
            for i in self.graph.nodes.keys():
                if (node != i):
                    (temp, toMerge) = self.shortest_path(node, i);
                    if temp == float('inf'):
                        return None, float('inf')
                    if (temp > max):
                        max = temp;
            if (max < min):
                min = max;
                centerOfGraph = node;
        return centerOfGraph, min;

    def plot_graph(self) -> None:
        for v in self.graph.nodes.values():
            if v.get_pos() != None:
                x, y, z = v.get_pos()
            else:
                x = random.randrange(0, 100)
                y = random.randrange(0, 100)
                z = random.randrange(0, 100)
                v.set_pos((x, y, z))
            plt.plot(float(x), float(y), markersize=6, marker="o", color="yellow")
            plt.text(float(x), float(y), str(v._id), color="red", fontsize=6)
        for src in self.get_graph().get_all_v().keys():
            if src in self.get_graph().edgesOut.keys():
                for dest in self.get_graph().all_out_edges_of_node(src).keys():
                    srcX = self.get_graph().nodes[src].get_pos()[0]
                    srcY = self.get_graph().nodes[src].get_pos()[1]
                    destX = self.get_graph().nodes[dest].get_pos()[0]
                    destY = self.get_graph().nodes[dest].get_pos()[1]
                    plt.annotate("", xy=(float(srcX), float(srcY)), xytext=(float(destX), float(destY)), arrowprops=dict(arrowstyle="<-", edgecolor="black", lw=1.0))
        plt.show()



