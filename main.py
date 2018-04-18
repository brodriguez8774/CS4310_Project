"""
Core/Start of program.
"""

# System Imports.
import time

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
    # run_algorithm_with_result_log(min_nodes=90, max_nodes=110, min_edges=0, max_edges=33, remove_nodes=False, min_percent_removal=0, max_percent_removal=0)

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
    Full algorithm and comparison drawing test.
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

    logger.info('Formatted Graph Orig Ranking: {0}'.format(graph_orig_ranking))
    logger.info('Formatted Graph Copy Ranking: {0}'.format(graph_copy_ranking))

    graph_1 = random_grapher.copy_graph(graph_orig)
    graph_2 = random_grapher.copy_graph(graph_copy)
    list_1 = list(graph_orig_ranking)
    list_2 = list(graph_copy_ranking)

    # Compute second half of algorithm with 'loose' edge matching.
    match_list = algorithm.matching(list_1, list_2, edge_strictness='loose')
    logger.info('Match List: {0}'.format(match_list))

    # Draw data.
    mapper_1 = data_mapping.DataMapping(graph_1, graph_2)
    mapper_1.draw_side_by_side_color_maps(vis_labels=True, key=True)
    mapper_1.draw_matching_comparison(match_list)


    # Try again with 'strict' edge matching.
    logger.info('Formatted Graph Orig Ranking: {0}'.format(graph_orig_ranking))
    logger.info('Formatted Graph Copy Ranking: {0}'.format(graph_copy_ranking))

    match_list = algorithm.matching(graph_orig_ranking, graph_copy_ranking, edge_strictness='strict')
    logger.info('Match List: {0}'.format(match_list))

    # Draw data again.
    mapper_2 = data_mapping.DataMapping(graph_orig, graph_copy)
    mapper_2.draw_side_by_side_color_maps(vis_labels=True, key=True)
    mapper_2.draw_matching_comparison(match_list)

def run_algorithm_with_result_log(min_nodes=2, max_nodes=10, min_edges=1, max_edges=5, remove_nodes=False,
                                  min_percent_removal=10, max_percent_removal=90):
    """
    Actually runs iterations of algorithm and logs results.
    """
    # Initialize necessary classes.
    random_grapher = randomized_grapher.RandomizedGrapher()
    algorithm = alg.Algorithm()

    # Do 100 iterations of current values.
    index = 0
    while index < 100:

        # Start Timer
        start_time = time.time()



        # Create graphs and sort edge lists.
        # First graph.
        graph_orig = random_grapher.create_graph(
            min_nodes=min_nodes,
            max_nodes=max_nodes,
            min_edges=min_edges,
            max_edges=max_edges
        )
        first_graph_creation_time = time.time()

        # Second graph.
        graph_copy = random_grapher.copy_graph(
            graph_orig,
            remove_nodes=remove_nodes,
            min_percent_removal=min_percent_removal,
            max_percent_removal=max_percent_removal
        )
        second_graph_creation_time = time.time()



        # Sort graph edges for algorithm.
        graph_orig.sort_node_edge_lists()
        graph_copy.sort_node_edge_lists()
        graph_edge_sort_time = time.time()



        # Run first half of algorithm and format for second half.
        graph_orig_ranking = algorithm.greatest_constraints_first(graph_orig.edge_count_list)
        graph_copy_ranking = algorithm.greatest_constraints_first(graph_copy.edge_count_list)
        graph_orig_ranking = algorithm.condense_list(graph_orig_ranking)
        graph_copy_ranking = algorithm.condense_list(graph_copy_ranking)
        greatest_constraints_time = time.time()



        # Run second half of algorithm.
        match_list = algorithm.matching(graph_copy_ranking, graph_orig_ranking)
        matching_time = time.time()



        # Record info.
        # logger.info(match_list)
        algorithm_results = {
            'start_time': start_time,
            'first_graph_creation_time': first_graph_creation_time,
            'second_graph_creation_time': second_graph_creation_time,
            'graph_edge_sort_time': graph_edge_sort_time,
            'greatest_constraints_time': greatest_constraints_time,
            'matching_time': matching_time,
            'number_of_matches': len(match_list),
        }
        logger.testresult(algorithm_results)
        index += 1


if __name__ == '__main__':
    main()
