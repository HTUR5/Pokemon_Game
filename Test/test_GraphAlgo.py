from unittest import TestCase
from GraphAlgo import GraphAlgo
from DiGraph import DiGraph



class TestAlgo(TestCase):

    def test_get_graph(self):
        g_algo = GraphAlgo()
        self.assertEqual(g_algo.graph, g_algo.get_graph())

    def test_load_from_json(self):
        algo = GraphAlgo()
        algo.load_from_json('A0.json')
        self.assertEqual(algo.load_from_json('A0.json'), True)

    def test_save_to_json(self):
        g = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 0, 1.1)
        g.add_edge(1, 2, 1.3)
        g.add_edge(2, 3, 1.1)
        g.add_edge(1, 3, 1.9)
        g_algo = GraphAlgo(g)
        # self.assertEqual(g_algo.save_to_json('C:\Users\hoday\PycharmProjects\Ex4' + '_saved'), True)

    def test_shortest_path(self):
        g = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 0, 1.1)
        g.add_edge(1, 2, 1.3)
        g.add_edge(2, 3, 1.1)
        g.add_edge(1, 3, 1.9)
        g_algo = GraphAlgo(g)
        self.assertEqual(g_algo.shortest_path(0, 3),(2.9, [0, 1, 3]))

    def test_tsp(self):
        g = DiGraph()  # creates an empty directed graph
        for n in range(5):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 4, 5)
        g.add_edge(1, 0, 1.1)
        g.add_edge(1, 2, 1.3)
        g.add_edge(1, 3, 1.9)
        g.add_edge(2, 3, 1.1)
        g.add_edge(3, 4, 2.1)
        g.add_edge(4, 2, .5)
        g_algo = GraphAlgo(g)
        self.assertEqual(g_algo.TSP([1, 2, 4]), ([1, 2, 3, 4], 4.5))

    def test_center_point(self):
        algo = GraphAlgo()
        algo.load_from_json('T0.json')
        self.assertEqual(algo.centerPoint(), (None, float('inf')))

    def test_plot_graph(self):
        algo = GraphAlgo()
        algo.load_from_json('A1.json')
        algo.plot_graph()

    def test_load_from_json_1000(self):
        g_algo = GraphAlgo()
        self.assertEqual( g_algo.load_from_json('1000Nodes.json'), True)

    def test_save_to_json_1000(self):
        g_algo = GraphAlgo()
        g_algo.load_from_json('1000Nodes.json')
        self.assertEqual(g_algo.save_to_json('C:\\Users\hoday\PycharmProjects\Ex4\Scripts' + '_saved1'), True)

    def test_shortest_path_1000(self):
        g_algo = GraphAlgo()
        g_algo.load_from_json('1000Nodes.json')
        self.assertEqual(g_algo.shortest_path(5,36), (940.3449339640827, [5, 626, 796, 334, 787, 56, 900, 629, 731, 145, 36]))

    def test_centerPoint_1000(self):
        g_algo = GraphAlgo()
        g_algo.load_from_json('1000Nodes.json')
        node, min = 362, 1185.9594924690523
        self.assertEqual(g_algo.centerPoint(), (node, min))

    def test_TSP_1000(self):
        g_algo = GraphAlgo()
        g_algo.load_from_json('1000Nodes.json')
        self.assertEqual(g_algo.TSP([23,34,45,506,780]), ([23, 480, 328, 98, 780, 186, 544, 896, 166, 448, 374, 497, 922, 506, 220, 45, 123, 692, 674, 870, 683, 940, 2, 590, 34], 2470.258401060781))

    def test_load_from_json_10000(self):
       g_algo = GraphAlgo()
       self.assertEqual(g_algo.load_from_json('10000Nodes.json'), True)

    def test_save_to_json_10000(self):
        g_algo = GraphAlgo()
        self.assertEqual(g_algo.load_from_json('10000Nodes.json'), True)
        self.assertEqual(g_algo.save_to_json('C:\\Users\hoday\PycharmProjects\Ex4\Scripts' + '_saved1'), True)

    def test_shortest_path_10000(self):
        g_algo = GraphAlgo()
        g_algo.load_from_json('10000Nodes.json')
        self.assertEqual(g_algo.shortest_path(5,36), (1316.0296563362544, [5, 3900, 4164, 858, 8143, 5768, 3707, 6141, 23, 5922, 7740, 36]))

    def test_centerPoint_10000(self):
        g_algo = GraphAlgo()
        g_algo.load_from_json('10000Nodes.json')
        node, min = 362, 1185.9594924690523
        self.assertEqual(g_algo.centerPoint(), (node, min))

    def test_TSP_10000(self):
        g_algo = GraphAlgo()
        g_algo.load_from_json('10000Nodes.json')
        g_algo.TSP([23, 34, 45, 506, 780])

    def test_load_from_json_100000(self):
        g_algo = GraphAlgo()
        self.assertEqual(g_algo.load_from_json('100000.json'), True)

    def test_save_to_json_100000(self):
        g_algo = GraphAlgo()
        self.assertEqual(g_algo.load_from_json('100000.json'), True)
        self.assertEqual(g_algo.save_to_json('C:\\Users\hoday\PycharmProjects\Ex4\Scripts' + '_saved1'), True)

    def test_shortest_path_100000(self):
        g_algo = GraphAlgo()
        g_algo.load_from_json('100000.json')
        self.assertEqual(g_algo.shortest_path(5, 36), ((644.3856577225355, [5, 53431, 83558, 7667, 57721, 27555, 51626, 68739, 75107, 26985, 36])))

    def test_centerPoint_100000(self):
        g_algo = GraphAlgo()
        g_algo.load_from_json('100000.json')
        node, min = 362, 1185.9594924690523
        self.assertEqual(g_algo.centerPoint(), (node, min))

    def test_TSP_100000(self):
        g_algo = GraphAlgo()
        g_algo.load_from_json('100000.json')
        g_algo.TSP([23, 34, 45, 506, 780])























