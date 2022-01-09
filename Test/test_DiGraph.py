from unittest import TestCase
from DiGraph import DiGraph
from Node import Node
from GraphAlgo import GraphAlgo


class TestGraph(TestCase):

    def test_v_size(self):
        g = DiGraph()
        for n in range(4):
            g.add_node(n)
        self.assertEqual(g.v_size(), 4)
        g1 = GraphAlgo()
        g1.load_from_json('A0.json')
        self.assertEqual(g1.get_graph().v_size(), 11)

    def test_e_size(self):
        g = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 0, 2)
        g.add_edge(1, 2, 3)
        g.add_edge(2, 3, 4)
        g.add_edge(1, 3, 5)
        self.assertEqual(g.e_size(), 5)
        g1 = GraphAlgo()
        g1.load_from_json('T0.json')
        self.assertEqual(g1.get_graph().e_size(), 5)

    def test_get_all_v(self):
        g = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 0, 2)
        g.add_edge(1, 2, 3)
        g.add_edge(2, 3, 4)
        g.add_edge(1, 3, 5)
        for i in g.get_all_v().keys():
            self.assertEquals(g.get_all_v().get(i), g.nodes[i])

    def test_all_in_edges_of_node(self):
        g = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 0, 1.1)
        g.add_edge(1, 2, 1.3)
        g.add_edge(2, 3, 1.1)
        g.add_edge(1, 3, 1.9)
        g.add_edge(2, 1, 4)
        self.assertEquals({0: 1, 2: 4}, g.all_in_edges_of_node(1))

    def test_all_out_edges_of_node(self):
        g = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 0, 1.1)
        g.add_edge(1, 2, 1.3)
        g.add_edge(2, 3, 1.1)
        g.add_edge(1, 3, 1.9)
        self.assertEquals({0: 1.1, 2: 1.3, 3: 1.9}, g.all_out_edges_of_node(1))

    def test_get_mc(self):
        g = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 0, 1.1)
        g.add_edge(1, 2, 1.3)
        g.add_edge(2, 3, 1.1)
        g.add_edge(1, 3, 1.9)
        self.assertEquals(g.get_mc(),9)

    def test_add_edge(self):
        g1 = DiGraph()
        g1.add_node(0, (1, 1, 1))
        g1.add_node(1, (2, 2, 2))
        g1.add_node(2, (3, 3, 3))
        g1.add_node(3, (4, 4, 4))
        g1.add_edge(0,1,9)
        g1.add_edge(0, 3, 4)
        g1.add_edge(2, 3, 4)
        self.assertEqual( g1.add_edge(2, 3, 4), True)
        self.assertEqual(g1.add_edge(2, 8, 4), False)

    def test_add_node(self):
        g1 = DiGraph()
        g1.add_node(0,(1,1,1))
        self.assertEqual(g1.add_node(0), False)
        self.assertEqual(g1.add_node(4), True)
        self.assertEqual(g1.add_node(3, (4, 4, 4)), True)

    def test_remove_node(self):
        g1 = DiGraph()
        g1.add_node(0)
        g1.add_node(1, (2, 2, 2))
        g1.add_node(2, (3, 3, 3))
        g1.add_node(3, (4, 4, 4))
        g1.add_edge(0, 1, 9)
        g1.add_edge(2, 3, 9)
        g1.add_edge(1, 3, 9)
        g1.add_edge(1, 2, 9)
        self.assertEqual(g1.remove_node(1), True)
        self.assertEqual(g1.remove_node(8), False)
        g1.add_node(4, (2, 3, 3))

    def test_remove_edge(self):
        g1 = DiGraph()
        g1.add_node(0, (1, 1, 1))
        g1.add_node(1, (2, 2, 2))
        g1.add_node(2, (3, 3, 3))
        g1.add_node(3, (4, 4, 4))
        g1.add_edge(0, 1, 9)
        g1.add_edge(2, 3, 9)
        g1.remove_edge(2, 3)
        self.assertEqual(g1.remove_edge(2, 3), False)
        self.assertEqual(g1.remove_edge(0, 1), True)

