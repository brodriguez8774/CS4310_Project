"""
Core/Start of program.
"""

# System Imports.
import random

# User Class Imports.
from resources import graph, logging, randomized_grapher
import algorithm as alg
import data_mapping


# Initialize logging.
logger = logging.get_logger(__name__)


def main():
    # # Test a "test_result" level log message.
    # logger.testresult('Test Result level test.')

    # Core program here.
    logger.info('Starting program.')

    # draw_manual_test_graphs()
    # draw_random_graphs()
    draw_full_algorithm()

    # Program termination and clean up.
    logger.info('Terminating program.')

def draw_manual_test_graphs():
    """
    Manually create small graphs and test out all possible mapping displays.
    """
    # Create test graph 1.
    test_graph_1 = graph.Graph('Test Graph')
    node_0 = test_graph_1.add_node()
    node_1 = test_graph_1.add_node(edges_in=[node_0, ])
    node_2 = test_graph_1.add_node(edges_in=[node_1, ])
    node_3 = test_graph_1.add_node(edges_in=[node_2, ])
    node_4 = test_graph_1.add_node(edges_in=[node_3, ], edges_out=[node_0, ])
    test_graph_1.sort_node_edge_lists()

    # Create test graph 2.
    test_graph_2 = graph.Graph()
    node_0 = test_graph_2.add_node()
    node_1 = test_graph_2.add_node(edges_in=[node_0, ])
    node_2 = test_graph_2.add_node(edges_in=[node_1, ])
    node_3 = test_graph_2.add_node(edges_in=[node_1, node_2, ], edges_out=[node_2, ])
    node_4 = test_graph_2.add_node(edges_in=[node_3, ], edges_out=[node_0, node_2, ])

    # node_5 = test_graph_2.add_node(edges_in=[node_4], edges_out=[node_0, node_3], )
    # node_6 = test_graph_2.add_node(edges_in=[node_4, node_5], edges_out=[node_1], )

    # node_5 = test_graph_2.add_node(edges_in=[node_4, ], )
    # node_6 = test_graph_2.add_node(edges_in=[node_5, ], )
    # node_7 = test_graph_2.add_node(edges_in=[node_6, ], )

    # node_7 = test_graph_2.add_node()

    # Map graph to visual representation.
    test_graph_2.sort_node_edge_lists()
    mapper = data_mapping.DataMapping(test_graph_1, test_graph_2)

    # Single maps.
    mapper.draw_bw_map(1, vis_labels=False, show=True, key=True)
    mapper.draw_color_map(1, vis_labels=False, show=True, key=True)
    mapper.draw_bw_map(2, vis_labels=False, show=True)
    mapper.draw_color_map(2, vis_labels=False, show=True)

    # Side by side maps.
    mapper.draw_side_by_side_bw_maps(vis_labels=False, key=True)
    mapper.draw_side_by_side_color_maps(vis_labels=False, key=True)

def draw_random_graphs():
    """
    Test randomly generated graphs.
    """
    # Test standard, randomly generated graph.
    random_grapher = randomized_grapher.RandomizedGrapher()

    a_graph = random_grapher.create_graph()
    # a_graph = random_grapher.create_graph(min_nodes=2, max_nodes=10, min_edges=0, max_edges=3)
    # a_graph = random_grapher.create_graph(min_nodes=2, max_nodes=10, edge_complete=True)
    a_graph.sort_node_edge_lists()

    mapper = data_mapping.DataMapping(a_graph, None)
    mapper.draw_color_map(1, vis_labels=True, show=True)

    # Test randomly generated graph that was copied from an original.
    a_graph_1 = random_grapher.create_graph(min_nodes=2, max_nodes=10, min_edges=0, max_edges=3)
    a_graph_2 = graph.Graph()
    for key, value in a_graph_1.nodes.items():
        a_graph_2.add_node(node=value)
    a_graph_1.sort_node_edge_lists()
    a_graph_2.sort_node_edge_lists()

    mapper = data_mapping.DataMapping(a_graph_2, None)
    mapper.draw_color_map(1, vis_labels=True, show=True)

def draw_full_algorithm():
    """
    Full algorithm test.
    """
    random_grapher = randomized_grapher.RandomizedGrapher()
    algorithm = alg.Algorithm()

    # Create graph 1.
    graph_orig = random_grapher.create_graph(min_nodes=2, max_nodes=10, min_edges=1, max_edges=5)

    # Create graph 2. Done via copying graph one, with random nodes removed.
    graph_copy = random_grapher.copy_graph(graph_orig, remove_nodes=True)

    # # Extra values for graph 2.
    # a_node = graph_copy.get_node(0)
    # graph_copy.add_node(edges_in=[a_node, ])
    # graph_copy.add_node()

    graph_orig.sort_node_edge_lists()
    graph_copy.sort_node_edge_lists()

    # Compute first half of algorithm.
    graph_orig_ranking = algorithm.greatest_constraints_first(graph_orig.edge_count_list)
    graph_copy_ranking = algorithm.greatest_constraints_first(graph_copy.edge_count_list)

    # Format list values.
    graph_orig_ranking = algorithm.condense_list(graph_orig_ranking)
    graph_copy_ranking = algorithm.condense_list(graph_copy_ranking)

    # logger.info('Formatted Graph Orig Ranking: {0}'.format(graph_orig_ranking))
    # logger.info('Formatted Graph Copy Ranking: {0}'.format(graph_copy_ranking))

    # Compute second half of algorithm.
    match_list = algorithm.matching(graph_orig_ranking, graph_copy_ranking)

    # logger.info('Match List: {0}'.format(match_list))

    # Draw data.
    mapper = data_mapping.DataMapping(graph_orig, graph_copy)
    mapper.draw_side_by_side_color_maps(vis_labels=True, key=True)
    mapper.draw_matching_comparison(match_list)


    # Switch which graph is the "subgraph" to compare with.
    match_list = algorithm.matching(graph_copy_ranking, graph_orig_ranking)
    # logger.info('Match List: {0}'.format(match_list))

    # Draw data again.
    mapper = data_mapping.DataMapping(graph_copy, graph_orig)
    mapper.draw_side_by_side_color_maps(vis_labels=True, key=True)
    mapper.draw_matching_comparison(match_list)
    # This should always match at least one node, proving that input order does matter.
    # IE: Which graph is considered "the subgraph" does make a difference.

if __name__ == '__main__':
    main()
