#!/usr/bin/python
# -*- coding: utf-8 -*-

# Maciej Wieloch, 303080

import unittest
import networkx as nx
import graphs_2


class GraphsTest(unittest.TestCase):

    def test_find_min_trail(self):
        graph = nx.MultiDiGraph()
        graph.add_weighted_edges_from([(1, 2, 0.5), (2, 3, 0.4), (2, 3, 0.3), (1, 3, 1.0)])

        trail = graphs_2.find_min_trail(graph, 1, 3)

        weight_expected = nx.dijkstra_path_length(graph, 1, 3)
        weight_actual = sum(i for (_, _, _, i) in trail)

        self.assertEqual(weight_actual, weight_expected)


if __name__ == '__main__':
    unittest.main()
