"""
Tests for algorithm.
"""

# System Imports.
import unittest

# User Class Imports.
from resources import graph, logging
import algorithm


# Initialize logging.
logger = logging.get_logger(__name__)


class AlgorithmMatching(unittest.TestCase):
    def setUp(self):
        self.algorithm = algorithm.Algorithm()
        self.graph_1 = graph.Graph()
        self.graph_2 = graph.Graph()

    #region One Node Tests

    def test_one_node_equal(self):
        # Create node with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        # logger.info('Graph 1 Rank: {0}'.format(str(graph_1_ranking[0])))
        # logger.info('Graph 2 Rank: {0}'.format(str(graph_2_ranking[0])))

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        # logger.info('Match List: {0}'.format(str(match_list[0])))
        self.assertEqual(len(match_list), 1)
        self.assertIn(graph_1_node_0, match_list[0])
        self.assertIn(graph_2_node_0, match_list[0])

    def test_one_node_bad_name(self):
        # Create node with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node', data=0)

        # Create node with different name and identical data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        self.assertEqual(len(match_list), 0)
        self.assertEqual([], match_list)

    def test_one_node_bad_data(self):
        # Create node with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)

        # Create node with identical name and different data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=1)

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        self.assertEqual(len(match_list), 0)
        self.assertEqual([], match_list)

    #endregion One Node Tests

    #region Two Node Tests

    def test_two_nodes_equal_no_edge(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node_1', data=1)

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1)

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # logger.info('Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        # logger.info('Formatted Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Formatted Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        # logger.info('Match List: {0}'.format(str(match_list)))

        self.assertEqual(len(match_list), 2)
        self.assertIn(graph_1_node_0, match_list[0])
        self.assertIn(graph_2_node_0, match_list[0])
        self.assertIn(graph_1_node_1, match_list[1])
        self.assertIn(graph_2_node_1, match_list[1])

    def test_two_nodes_equal_with_edge_in(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node_1', data=1, edges_in=[graph_1_node_0, ])

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1, edges_in=[graph_2_node_0, ])

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        self.assertEqual(len(match_list), 2)
        self.assertIn(graph_1_node_0, match_list[0])
        self.assertIn(graph_2_node_0, match_list[0])
        self.assertIn(graph_1_node_1, match_list[1])
        self.assertIn(graph_2_node_1, match_list[1])

    def test_two_nodes_equal_with_edge_out(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node_1', data=1, edges_out=[graph_1_node_0, ])

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1, edges_out=[graph_2_node_0, ])

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        self.assertEqual(len(match_list), 2)
        self.assertIn(graph_1_node_0, match_list[0])
        self.assertIn(graph_2_node_0, match_list[0])
        self.assertIn(graph_1_node_1, match_list[1])
        self.assertIn(graph_2_node_1, match_list[1])

    def test_two_nodes_equal_with_all_edge(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node_1', data=1, edges_in=[graph_1_node_0, ], edges_out=[graph_1_node_0, ])

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1, edges_in=[graph_2_node_0, ], edges_out=[graph_2_node_0, ])

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # logger.info('Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        # logger.info('Formatted Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Formatted Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        # logger.info('Match List: {0}'.format(str(match_list)))

        self.assertEqual(len(match_list), 2)
        self.assertIn(graph_1_node_0, match_list[0])
        self.assertIn(graph_2_node_0, match_list[0])
        self.assertIn(graph_1_node_1, match_list[1])
        self.assertIn(graph_2_node_1, match_list[1])

    def test_two_nodes_bad_name(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node', data=1, edges_in=[graph_1_node_0, ], edges_out=[graph_1_node_0, ])

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1, edges_in=[graph_2_node_0, ], edges_out=[graph_2_node_0, ])

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        self.assertEqual(len(match_list), 1)
        self.assertIn(graph_1_node_0, match_list[0])
        self.assertIn(graph_2_node_0, match_list[0])

    def test_two_nodes_bad_data(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node_1', data=10, edges_in=[graph_1_node_0, ], edges_out=[graph_1_node_0, ])

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1, edges_in=[graph_2_node_0, ], edges_out=[graph_2_node_0, ])

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        self.assertEqual(len(match_list), 1)
        self.assertIn(graph_1_node_0, match_list[0])
        self.assertIn(graph_2_node_0, match_list[0])

    def test_two_nodes_bad_edges_in(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node_1', data=1, edges_in=[graph_1_node_0, ], edges_out=[graph_1_node_0, ])

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1, edges_in=[], edges_out=[graph_2_node_0, ])

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # logger.info('Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        # logger.info('Formatted Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Formatted Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        # logger.info('Match List: {0}'.format(str(match_list[0])))

        self.assertEqual(len(match_list), 0)

    def test_two_nodes_bad_edges_out(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node_1', data=1, edges_in=[graph_1_node_0, ], edges_out=[graph_1_node_0, ])

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1, edges_in=[graph_2_node_0, ], edges_out=[])

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        self.assertEqual(len(match_list), 0)

    #endregion Two Node Tests

    #region Three Node Tests

    def test_three_nodes_equal_no_edge(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node_1', data=1)
        graph_1_node_2 = self.graph_1.add_node(name='Node_2', data=2)

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1)
        graph_2_node_2 = self.graph_2.add_node(name='Node_2', data=2)

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # logger.info('Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        # logger.info('Formatted Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Formatted Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        # logger.info('Match List: {0}'.format(str(match_list)))

        self.assertEqual(len(match_list), 3)
        self.assertIn(graph_1_node_0, match_list[0])
        self.assertIn(graph_2_node_0, match_list[0])
        self.assertIn(graph_1_node_1, match_list[1])
        self.assertIn(graph_2_node_1, match_list[1])
        self.assertIn(graph_1_node_2, match_list[2])
        self.assertIn(graph_2_node_2, match_list[2])

    def test_three_nodes_equal_with_edge_in(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node_1', data=1, edges_in=[graph_1_node_0, ])
        graph_1_node_2 = self.graph_1.add_node(name='Node_2', data=2, edges_in=[graph_1_node_1, ])

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1, edges_in=[graph_2_node_0, ])
        graph_2_node_2 = self.graph_2.add_node(name='Node_2', data=2, edges_in=[graph_2_node_1, ])

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # logger.info('Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        # logger.info('Formatted Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Formatted Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        # logger.info('Match List: {0}'.format(str(match_list)))

        self.assertEqual(len(match_list), 3)
        self.assertIn(graph_1_node_0, match_list[0])
        self.assertIn(graph_2_node_0, match_list[0])
        self.assertIn(graph_1_node_1, match_list[1])
        self.assertIn(graph_2_node_1, match_list[1])
        self.assertIn(graph_1_node_2, match_list[2])
        self.assertIn(graph_2_node_2, match_list[2])

    def test_three_nodes_equal_with_edge_out(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node_1', data=1, edges_out=[graph_1_node_0, ])
        graph_1_node_2 = self.graph_1.add_node(name='Node_2', data=2, edges_out=[graph_1_node_1, ])

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1, edges_out=[graph_2_node_0, ])
        graph_2_node_2 = self.graph_2.add_node(name='Node_2', data=2, edges_out=[graph_2_node_1, ])

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # logger.info('Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        # logger.info('Formatted Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Formatted Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        # logger.info('Match List: {0}'.format(str(match_list)))

        self.assertEqual(len(match_list), 3)
        self.assertIn(graph_1_node_0, match_list[0])
        self.assertIn(graph_2_node_0, match_list[0])
        self.assertIn(graph_1_node_1, match_list[1])
        self.assertIn(graph_2_node_1, match_list[1])
        self.assertIn(graph_1_node_2, match_list[2])
        self.assertIn(graph_2_node_2, match_list[2])

    def test_three_nodes_equal_with_all_edge(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node_1', data=1, edges_in=[graph_1_node_0, ], edges_out=[graph_1_node_0, ])
        graph_1_node_2 = self.graph_1.add_node(name='Node_2', data=2, edges_in=[graph_1_node_1, ], edges_out=[graph_1_node_1, ])

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1, edges_in=[graph_2_node_0, ], edges_out=[graph_2_node_0, ])
        graph_2_node_2 = self.graph_2.add_node(name='Node_2', data=2, edges_in=[graph_2_node_1, ], edges_out=[graph_2_node_1, ])

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # logger.info('Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        # logger.info('Formatted Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Formatted Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        # logger.info('Match List: {0}'.format(str(match_list)))

        self.assertEqual(len(match_list), 3)
        self.assertIn(graph_1_node_0, match_list[0])
        self.assertIn(graph_2_node_0, match_list[0])
        self.assertIn(graph_1_node_1, match_list[1])
        self.assertIn(graph_2_node_1, match_list[1])
        self.assertIn(graph_1_node_2, match_list[2])
        self.assertIn(graph_2_node_2, match_list[2])

    def test_three_nodes_bad_name(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node_1', data=1, edges_in=[graph_1_node_0, ], edges_out=[graph_1_node_0, ])
        graph_1_node_2 = self.graph_1.add_node(name='Node', data=2, edges_in=[graph_1_node_1, ], edges_out=[graph_1_node_1, ])

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1, edges_in=[graph_2_node_0, ], edges_out=[graph_2_node_0, ])
        graph_2_node_2 = self.graph_2.add_node(name='Node_2', data=2, edges_in=[graph_2_node_1, ], edges_out=[graph_2_node_1, ])

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        self.assertEqual(len(match_list), 2)
        self.assertIn(graph_1_node_0, match_list[0])
        self.assertIn(graph_2_node_0, match_list[0])
        self.assertIn(graph_1_node_1, match_list[1])
        self.assertIn(graph_2_node_1, match_list[1])

    def test_three_nodes_bad_data(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node_1', data=1, edges_in=[graph_1_node_0, ], edges_out=[graph_1_node_0, ])
        graph_1_node_2 = self.graph_1.add_node(name='Node_2', data=20, edges_in=[graph_1_node_1, ], edges_out=[graph_1_node_1, ])

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1, edges_in=[graph_2_node_0, ], edges_out=[graph_2_node_0, ])
        graph_2_node_2 = self.graph_2.add_node(name='Node_2', data=2, edges_in=[graph_2_node_1, ], edges_out=[graph_2_node_1, ])

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        self.assertEqual(len(match_list), 2)
        self.assertIn(graph_1_node_0, match_list[0])
        self.assertIn(graph_2_node_0, match_list[0])
        self.assertIn(graph_1_node_1, match_list[1])
        self.assertIn(graph_2_node_1, match_list[1])

    def test_three_nodes_bad_edges_in(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node_1', data=1, edges_in=[graph_1_node_0, ], edges_out=[graph_1_node_0, ])
        graph_1_node_2 = self.graph_1.add_node(name='Node_2', data=2, edges_in=[graph_1_node_1, ], edges_out=[graph_1_node_1, ])

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1, edges_in=[graph_2_node_0, ], edges_out=[graph_2_node_0, ])
        graph_2_node_2 = self.graph_2.add_node(name='Node_2', data=2, edges_in=[], edges_out=[graph_2_node_1, ])

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # logger.info('Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        # logger.info('Formatted Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Formatted Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        # logger.info('Match List: {0}'.format(str(match_list[0])))

        self.assertEqual(len(match_list), 1)
        self.assertIn(graph_1_node_0, match_list[0])
        self.assertIn(graph_2_node_0, match_list[0])

    def test_three_nodes_bad_edges_out(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node_1', data=1, edges_in=[graph_1_node_0, ], edges_out=[graph_1_node_0, ])
        graph_1_node_2 = self.graph_1.add_node(name='Node_2', data=2, edges_in=[graph_1_node_1, ], edges_out=[graph_1_node_1, ])

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1, edges_in=[graph_2_node_0, ], edges_out=[graph_2_node_0, ])
        graph_2_node_2 = self.graph_2.add_node(name='Node_2', data=2, edges_in=[graph_2_node_1, ], edges_out=[])

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        self.assertEqual(len(match_list), 1)
        self.assertIn(graph_1_node_0, match_list[0])
        self.assertIn(graph_2_node_0, match_list[0])

    def test_uneven_node_count(self):
        # Create nodes with name and data for graph 1.
        graph_1_node_0 = self.graph_1.add_node(name='Node_0', data=0)
        graph_1_node_1 = self.graph_1.add_node(name='Node_1', data=1, edges_in=[graph_1_node_0, ], edges_out=[graph_1_node_0, ])
        graph_1_node_2 = self.graph_1.add_node(name='Node_2', data=2, edges_in=[graph_1_node_1, ], edges_out=[graph_1_node_1, ])

        # Create node with identical name and data for graph 2.
        graph_2_node_0 = self.graph_2.add_node(name='Node_0', data=0)
        graph_2_node_1 = self.graph_2.add_node(name='Node_1', data=1, edges_in=[graph_2_node_0, ], edges_out=[graph_2_node_0, ])
        graph_2_node_2 = self.graph_2.add_node(name='Node_2', data=2, edges_in=[graph_2_node_1, ], edges_out=[graph_2_node_1, ])
        graph_2_node_3 = self.graph_2.add_node(name='Node_3', data=3, edges_in=[graph_2_node_1, ], edges_out=[graph_2_node_2, ])
        graph_2_node_4 = self.graph_2.add_node(name='Node_4', data=4, edges_in=[graph_2_node_3, ], edges_out=[graph_2_node_3, ])

        # Get graph rankings.
        graph_1_ranking = self.algorithm.greatest_constraints_first(self.graph_1.edge_count_list)
        graph_2_ranking = self.algorithm.greatest_constraints_first(self.graph_2.edge_count_list)

        # logger.info('Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        # Format ranking list for matching.
        graph_1_ranking = self.algorithm.condense_list(graph_1_ranking)
        graph_2_ranking = self.algorithm.condense_list(graph_2_ranking)

        # logger.info('Formatted Graph 1 Rank: {0}'.format(str(graph_1_ranking)))
        # logger.info('Formatted Graph 2 Rank: {0}'.format(str(graph_2_ranking)))

        match_list = self.algorithm.matching(graph_1_ranking, graph_2_ranking)

        logger.info('Match List: {0}'.format(str(match_list)))

        self.assertEqual(len(match_list), 3)
        self.assertIn(graph_1_node_0, match_list[0])
        self.assertIn(graph_2_node_0, match_list[0])
        self.assertIn(graph_1_node_1, match_list[1])
        self.assertIn(graph_2_node_1, match_list[1])
        self.assertIn(graph_1_node_2, match_list[2])
        self.assertIn(graph_2_node_2, match_list[2])

    #endregion Three Node Tests
