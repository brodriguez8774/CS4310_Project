"""
Tests for core Graph classes.
"""

# System Imports.
import unittest

# User Class Imports.
from resources import graph


class Graph(unittest.TestCase):
    def setUp(self):
        self.test_graph = graph.Graph()

    def test_add_node(self):
        # Test empty graph.
        self.assertEqual(str(self.test_graph.get_node_keys()), 'dict_keys([])')

        # Test graph with one node.
        self.test_graph.add_node()
        node_0 = self.test_graph.get_node(0)
        self.assertIn(node_0.identifier, self.test_graph.get_node_keys())

        # Test graph with two nodes.
        self.test_graph.add_node('ANode')
        node_1 = self.test_graph.get_node('ANode')
        self.assertIn(node_0.identifier, self.test_graph.get_node_keys())
        self.assertIn(node_1.identifier, self.test_graph.get_node_keys())

        # Test graph with three nodes.
        self.test_graph.add_node()
        node_2 = self.test_graph.get_node(1)
        self.assertIn(node_0.identifier, self.test_graph.get_node_keys())
        self.assertIn(node_1.identifier, self.test_graph.get_node_keys())
        self.assertIn(node_2.identifier, self.test_graph.get_node_keys())

    def test_remove_node(self):
        # First check that graph is as expected with 3 fully connected nodes.
        self.test_graph.add_node()
        node_0 = self.test_graph.get_node(0)
        self.test_graph.add_node(edges_in=[node_0, ], edges_out=[node_0, ])
        node_1 = self.test_graph.get_node(1)
        self.test_graph.add_node(edges_in=[node_0, node_1, ], edges_out=[node_0, node_1, ])
        node_2 = self.test_graph.get_node(2)
        self.assertEqual(node_0.edges_in, [node_1, node_2, ])
        self.assertEqual(node_0.edges_out, [node_1, node_2, ])
        self.assertEqual(node_1.edges_in, [node_0, node_2, ])
        self.assertEqual(node_1.edges_out, [node_0, node_2, ])
        self.assertEqual(node_2.edges_in, [node_0, node_1, ])
        self.assertEqual(node_2.edges_out, [node_0, node_1, ])

        # Test removing node.
        self.test_graph.remove_node(node_2.identifier)
        self.assertNotIn(node_2, self.test_graph.get_node_keys())
        self.assertIsNone(self.test_graph.get_node(str(node_2)))
        self.assertEqual(node_0.edges_in, [node_1, ])
        self.assertEqual(node_0.edges_out, [node_1, ])
        self.assertEqual(node_1.edges_in, [node_0, ])
        self.assertEqual(node_1.edges_out, [node_0, ])

        # Test removing node.
        self.test_graph.remove_node(node_1.identifier)
        self.assertNotIn(node_1.identifier, self.test_graph.get_node_keys())
        self.assertIsNone(self.test_graph.get_node(str(node_1)))
        self.assertEqual(node_0.edges_in, [])
        self.assertEqual(node_0.edges_out, [])

        # Test removing node.
        self.test_graph.remove_node(node_0.identifier)
        self.assertNotIn(node_0.identifier, self.test_graph.get_node_keys())
        self.assertIsNone(self.test_graph.get_node(str(node_0)))
        self.assertEqual(str(self.test_graph.get_node_keys()), 'dict_keys([])')

        # Test removing nonexistent node.
        self.test_graph.remove_node(node_0)
        self.assertEqual(str(self.test_graph.get_node_keys()), 'dict_keys([])')

    def test_get_node(self):
        # Test with name.
        self.test_graph.add_node('Test')
        node = self.test_graph.get_node('Test')
        self.assertEqual(node.identifier, 'Test')

        # Test with identifier.
        self.test_graph.add_node()
        node = self.test_graph.get_node(0)
        self.assertEqual(node.identifier, 0)

    def test_edge_count_list(self):
        # Test with no edges.
        self.assertEqual(self.test_graph.edge_count_list, [])

        # Test with one node.
        node_0 = self.test_graph.add_node()
        self.assertIn(node_0, self.test_graph.edge_count_list)
        self.assertEqual(1, len(self.test_graph.edge_count_list))

        # Test multiple nodes.
        node_1 = self.test_graph.add_node(edges_in=[node_0])
        self.assertIn(node_1, self.test_graph.edge_count_list)
        self.assertEqual(2, len(self.test_graph.edge_count_list))
        node_2 = self.test_graph.add_node(edges_in=[node_1, ], edges_out=[node_1, ])
        self.assertIn(node_2, self.test_graph.edge_count_list)
        self.assertEqual(3, len(self.test_graph.edge_count_list))
        node_3 = self.test_graph.add_node()
        self.assertIn(node_3, self.test_graph.edge_count_list)
        self.assertEqual(4, len(self.test_graph.edge_count_list))
        node_4 = self.test_graph.add_node()
        self.assertIn(node_4, self.test_graph.edge_count_list)
        self.assertEqual(5, len(self.test_graph.edge_count_list))
        node_5 = self.test_graph.add_node(edges_out=[node_4])
        self.assertIn(node_5, self.test_graph.edge_count_list)
        self.assertEqual(6, len(self.test_graph.edge_count_list))

        node_6 = self.test_graph.add_node(edges_in=[node_2, ], edges_out=[node_1, node_2, ])
        self.assertIn(node_6, self.test_graph.edge_count_list)
        self.assertEqual(7, len(self.test_graph.edge_count_list))

        # Test actual list sorting.
        self.assertEqual(self.test_graph.edge_count_list, [node_0, node_1, node_2, node_3, node_4, node_5, node_6, ])
        self.test_graph.sort_node_edge_lists()
        self.assertEqual(self.test_graph.edge_count_list, [node_1, node_2, node_6, node_0, node_4, node_5, node_3, ])


class Node(unittest.TestCase):
    def setUp(self):
        self.test_node = graph.Node(name='Test Node')
        self.test_node_with_name = graph.Node(name='Test Name')
        self.test_node_without_name = graph.Node()

    def test_creation(self):
        self.assertEqual(self.test_node_with_name.name, 'Test Name')
        self.assertEqual(self.test_node_with_name.identifier, 'Test Name')
        self.assertFalse(self.test_node_with_name.edges_in)
        self.assertFalse(self.test_node_with_name.edges_out)

        self.assertEqual(self.test_node_without_name.name, None)
        self.assertEqual(self.test_node_without_name.identifier, None)

    def test_add_edges(self):
        # Test with 0 edges added.
        self.assertEqual(self.test_node.edges_in, [])
        self.assertEqual(self.test_node.edges_out, [])
        self.assertEqual(self.test_node_with_name.edges_in, [])
        self.assertEqual(self.test_node_with_name.edges_out, [])
        self.assertEqual(self.test_node_without_name.edges_in, [])
        self.assertEqual(self.test_node_without_name.edges_out, [])

        # Test with 1 edge added.
        self.test_node.add_edge(edges_in=[self.test_node_with_name, ])
        self.assertEqual(self.test_node.edges_in, [self.test_node_with_name, ])
        self.assertEqual(self.test_node.edges_out, [])
        self.assertEqual(self.test_node_with_name.edges_in, [])
        self.assertEqual(self.test_node_with_name.edges_out, [self.test_node, ])
        self.assertEqual(self.test_node_without_name.edges_in, [])
        self.assertEqual(self.test_node_without_name.edges_out, [])

        # Test with 2 edges added.
        self.test_node.add_edge(edges_in=[self.test_node_without_name, ])
        self.assertEqual(self.test_node.edges_in, [self.test_node_with_name, self.test_node_without_name, ])
        self.assertEqual(self.test_node.edges_out, [])
        self.assertEqual(self.test_node_with_name.edges_in, [])
        self.assertEqual(self.test_node_with_name.edges_out, [self.test_node, ])
        self.assertEqual(self.test_node_without_name.edges_in, [])
        self.assertEqual(self.test_node_without_name.edges_out, [self.test_node, ])

        # Test edge_from part of function.
        self.test_node.add_edge(edges_out=[self.test_node_with_name, ])
        self.assertEqual(self.test_node.edges_in, [self.test_node_with_name, self.test_node_without_name, ])
        self.assertEqual(self.test_node.edges_out, [self.test_node_with_name, ])
        self.assertEqual(self.test_node_with_name.edges_in, [self.test_node, ])
        self.assertEqual(self.test_node_with_name.edges_out, [self.test_node, ])
        self.assertEqual(self.test_node_without_name.edges_in, [])
        self.assertEqual(self.test_node_without_name.edges_out, [self.test_node, ])

        # Test attempt to add duplicate edges and attempt to add self.
        self.test_node.add_edge(edges_in=[self.test_node, ])
        self.test_node.add_edge(edges_out=[self.test_node, ])
        self.test_node.add_edge(edges_in=[self.test_node_without_name, ])
        self.test_node.add_edge(edges_out=[self.test_node_with_name, ])
        self.assertEqual(self.test_node.edges_in, [self.test_node_with_name, self.test_node_without_name, ])
        self.assertEqual(self.test_node.edges_out, [self.test_node_with_name, ])
        self.assertEqual(self.test_node_with_name.edges_in, [self.test_node, ])
        self.assertEqual(self.test_node_with_name.edges_out, [self.test_node, ])
        self.assertEqual(self.test_node_without_name.edges_in, [])
        self.assertEqual(self.test_node_without_name.edges_out, [self.test_node, ])

        # Test adding multiple at once.
        self.test_node.drop_all_edges()
        self.test_node_with_name.drop_all_edges()
        self.test_node_without_name.drop_all_edges()
        self.test_node.add_edge(
            edges_in=[self.test_node_with_name, self.test_node_without_name, ],
            edges_out=[self.test_node_with_name, ]
        )
        self.assertEqual(self.test_node.edges_in, [self.test_node_with_name, self.test_node_without_name, ])
        self.assertEqual(self.test_node.edges_out, [self.test_node_with_name, ])
        self.assertEqual(self.test_node_with_name.edges_in, [self.test_node, ])
        self.assertEqual(self.test_node_with_name.edges_out, [self.test_node, ])
        self.assertEqual(self.test_node_without_name.edges_in, [])
        self.assertEqual(self.test_node_without_name.edges_out, [self.test_node, ])

    def test_remove_edges(self):
        self.test_node.add_edge(edges_in=[self.test_node_with_name, ])
        self.test_node.add_edge(edges_in=[self.test_node_without_name, ])
        self.test_node.add_edge(edges_out=[self.test_node_with_name, ])

        # Check expected with 3 nodes.
        self.assertEqual(self.test_node.edges_in, [self.test_node_with_name, self.test_node_without_name, ])
        self.assertEqual(self.test_node.edges_out, [self.test_node_with_name, ])
        self.assertEqual(self.test_node_with_name.edges_in, [self.test_node, ])
        self.assertEqual(self.test_node_with_name.edges_out, [self.test_node, ])
        self.assertEqual(self.test_node_without_name.edges_in, [])
        self.assertEqual(self.test_node_without_name.edges_out, [self.test_node, ])

        # Remove edge.
        self.test_node.remove_edge(edges_in=[self.test_node_with_name, ])
        self.assertEqual(self.test_node.edges_in, [self.test_node_without_name, ])
        self.assertEqual(self.test_node.edges_out, [self.test_node_with_name, ])
        self.assertEqual(self.test_node_with_name.edges_in, [self.test_node, ])
        self.assertEqual(self.test_node_with_name.edges_out, [])
        self.assertEqual(self.test_node_without_name.edges_in, [])
        self.assertEqual(self.test_node_without_name.edges_out, [self.test_node, ])

        # Remove edge.
        self.test_node.remove_edge(edges_in=[self.test_node_without_name, ])
        self.assertEqual(self.test_node.edges_in, [])
        self.assertEqual(self.test_node.edges_out, [self.test_node_with_name, ])
        self.assertEqual(self.test_node_with_name.edges_in, [self.test_node, ])
        self.assertEqual(self.test_node_with_name.edges_out, [])
        self.assertEqual(self.test_node_without_name.edges_in, [])
        self.assertEqual(self.test_node_without_name.edges_out, [])

        # Remove edge.
        self.test_node.remove_edge(edges_out=[self.test_node_with_name, ])
        self.assertEqual(self.test_node.edges_in, [])
        self.assertEqual(self.test_node.edges_out, [])
        self.assertEqual(self.test_node_with_name.edges_in, [])
        self.assertEqual(self.test_node_with_name.edges_out, [])
        self.assertEqual(self.test_node_without_name.edges_in, [])
        self.assertEqual(self.test_node_without_name.edges_out, [])

        # Test removing nonexistant edge.
        self.test_node.remove_edge(edges_in=[self.test_node_with_name, ])
        self.test_node.remove_edge(edges_out=[self.test_node_with_name, ])
        self.assertEqual(self.test_node.edges_in, [])
        self.assertEqual(self.test_node.edges_out, [])
        self.assertEqual(self.test_node_with_name.edges_in, [])
        self.assertEqual(self.test_node_with_name.edges_out, [])
        self.assertEqual(self.test_node_without_name.edges_in, [])
        self.assertEqual(self.test_node_without_name.edges_out, [])

        # Test removing multiple at once.
        self.test_node.add_edge(edges_in=[self.test_node_with_name, ])
        self.test_node.add_edge(edges_in=[self.test_node_without_name, ])
        self.test_node.add_edge(edges_out=[self.test_node_with_name, ])

        self.test_node.remove_edge(
            edges_in=[self.test_node_with_name, self.test_node_without_name,],
            edges_out=[self.test_node_with_name]
        )

    def test_info_string(self):
        # Test node with no edges.
        self.assertEqual(self.test_node.info_string(), 'Node: Test Node')
        self.test_node.add_edge(edges_in=[self.test_node_with_name, ])

        # Test node with edge_to.
        self.assertEqual(self.test_node.info_string(), 'Node: Test Node | Edges To: [ Test Name, ]')

        # Test node with multiple edge_to's.
        self.test_node.add_edge(edges_in=[self.test_node_without_name, ])
        self.assertEqual(self.test_node.info_string(), 'Node: Test Node | Edges To: [ Test Name, None, ]')

        # Test node with all values.
        self.test_node.add_edge(edges_out=[self.test_node_with_name, ])
        self.assertEqual(
            self.test_node.info_string(),
            'Node: Test Node | Edges To: [ Test Name, None, ] | Edges From: [ Test Name, ]'
        )

        # Test printing only specific values.
        self.assertEqual(
            self.test_node.info_string(only_name=True),
            'Node: Test Node'
        )
        self.assertEqual(
            self.test_node.info_string(only_edges_in=True),
            'Edges To: [ Test Name, None, ]'
        )
        self.assertEqual(
            self.test_node.info_string(only_edges_out=True),
            'Edges From: [ Test Name, ]'
        )
