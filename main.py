"""
Core/Start of program.
"""

# System Imports.
from matplotlib import patches, pyplot
import ast, time

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

    # draw_full_algorithm()

    # run_algorithm_with_result_log(
    #     min_nodes=90, max_nodes=110, min_edges=0, max_edges=33, remove_nodes=False, min_percent_removal=0,
    #     max_percent_removal=0, edge_strictness='loose'
    # )

    # read_and_compute_results()

    plot_results()

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
    mapper.draw_bw_map(1, vis_labels=False, show=True, key=False)
    mapper.draw_color_map(1, vis_labels=False, show=True, key=False)
    mapper.draw_bw_map(2, vis_labels=False, show=True)
    mapper.draw_color_map(2, vis_labels=False, show=True, key=True)

    # Side by side maps.
    mapper.draw_side_by_side_bw_maps(vis_labels=False, key=False)
    mapper.draw_side_by_side_color_maps(vis_labels=False, key=True)

def draw_random_graphs():
    """
    Test randomly generated graphs.
    """
    # Test standard, randomly generated graph.
    random_grapher = randomized_grapher.RandomizedGrapher()

    a_graph = random_grapher.create_graph()
    # a_graph = random_grapher.create_graph(min_nodes=5, max_nodes=10, min_edges=0, max_edges=2)
    # a_graph = random_grapher.create_graph(min_nodes=2, max_nodes=10, edge_complete=True)
    a_graph.sort_node_edge_lists()

    mapper = data_mapping.DataMapping(a_graph, None)
    mapper.draw_color_map(1, vis_labels=False, show=True)

    # # Test randomly generated graph that was copied from an original.
    # a_graph_1 = random_grapher.create_graph(min_nodes=2, max_nodes=10, min_edges=0, max_edges=3)
    # a_graph_2 = graph.Graph()
    # for key, value in a_graph_1.nodes.items():
    #     a_graph_2.add_node(node=value)
    # a_graph_1.sort_node_edge_lists()
    # a_graph_2.sort_node_edge_lists()
    #
    # mapper = data_mapping.DataMapping(a_graph_2, None)
    # mapper.draw_color_map(1, vis_labels=True, show=True)

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
                                  min_percent_removal=10, max_percent_removal=90, edge_strictness='loose'):
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
        node_count = len(graph_orig.nodes)

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
        match_list = algorithm.matching(graph_copy_ranking, graph_orig_ranking, edge_strictness=edge_strictness)
        matching_time = time.time()



        # Record info.
        # logger.info(match_list)
        algorithm_results = {
            'node_count': node_count,
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


def read_and_compute_results():
    """
    Reads in from given file and computes human-readable averages from all 100 iterations.
    """
    # Open file.
    result_read_in = '0500_Dense_Many_Strict.log'
    read_file = open('documents/results/sets/' + result_read_in, 'r')

    total_first_graph_creation = 0
    total_second_graph_creation = 0
    total_edge_sort_time = 0
    total_greatest_constraints_time = 0
    total_match_time = 0
    total_time = 0
    total_nodes_handled = 0
    total_matches = 0

    # Read line.
    read_line = read_file.readline()


    while (read_line != ''):
        values = ast.literal_eval(read_line)
        if isinstance(values, dict):
            logger.info('Dict: {0}'.format(values))

            first_graph_creation = values['first_graph_creation_time'] - values['start_time']
            second_graph_creation = values['second_graph_creation_time'] - values['first_graph_creation_time']
            edge_sort = values['graph_edge_sort_time'] - values['second_graph_creation_time']
            g_c = values['greatest_constraints_time'] - values['graph_edge_sort_time']
            matching = values['matching_time'] - values['greatest_constraints_time']
            overall_time = values['matching_time'] - values['start_time']
            node_count = values['node_count']
            number_of_matches = values['number_of_matches']

            # logger.info('Overall: {0}s, First Graph: {1}s, Second Graph: {2}s, Edge Sort: {3}s, GC: {4}s, Match: {5}s, {6} Total Nodes'.format(
            #     overall_time, first_graph_creation, second_graph_creation, edge_sort, g_c, matching, node_count))

            total_first_graph_creation += first_graph_creation
            total_second_graph_creation += second_graph_creation
            total_edge_sort_time += edge_sort
            total_greatest_constraints_time += g_c
            total_match_time += matching
            total_time += overall_time
            total_nodes_handled += node_count
            total_matches += number_of_matches

            read_line = read_file.readline()

    # Close file.
    read_file.close()

    # Average results.
    total_first_graph_creation = total_first_graph_creation / 100
    total_second_graph_creation = total_second_graph_creation / 100
    total_edge_sort_time = total_edge_sort_time / 100
    total_greatest_constraints_time = total_greatest_constraints_time / 100
    total_match_time = total_match_time / 100
    total_time = total_time / 100
    total_nodes_handled = total_nodes_handled / 100
    total_matches = total_matches / 100

    # Save results.
    logger.info('\n\nAverage of Results for {0}:\n'.format(result_read_in))

    result_avg_dict = {
        'first_graph_creation': total_first_graph_creation,
        'second_graph_creation': total_second_graph_creation,
        'edge_sort_time': total_edge_sort_time,
        'greatest_constraints_time': total_greatest_constraints_time,
        'match_time': total_match_time,
        'total_time': total_time,
        'nodes_handled': total_nodes_handled,
        'node_matches': total_matches,
    }

    # logger.info('Overall: {0}s, First Graph: {1}s, Second Graph: {2}s, Edge Sort: {3}s, GC: {4}s, Match: {5}s, {6} Total Nodes'.format(
    #         total_time, total_first_graph_creation, total_second_graph_creation, total_edge_sort_time, total_greatest_constraints_time, total_match_time, total_nodes_handled))

    logger.testresult(result_avg_dict)

def plot_results():
    """
    Reads in values from result_averages and plots results.
    """
    # First read in all result average values.
    file_0100_avg = open('documents/results/0100_Set_Averages.log', 'r')
    file_0200_avg = open('documents/results/0200_Set_Averages.log', 'r')
    file_0300_avg = open('documents/results/0300_Set_Averages.log', 'r')
    file_0400_avg = open('documents/results/0400_Set_Averages.log', 'r')
    file_0500_avg = open('documents/results/0500_Set_Averages.log', 'r')

    set_0100 = []
    set_0200 = []
    set_0300 = []
    set_0400 = []
    set_0500 = []

    read_line = file_0100_avg.readline()
    while read_line != '':
        if read_line != '\n':
            set_0100.append(ast.literal_eval(read_line))
        read_line = file_0100_avg.readline()

    read_line = file_0200_avg.readline()
    while read_line != '':
        if read_line != '\n':
            set_0200.append(ast.literal_eval(read_line))
        read_line = file_0200_avg.readline()

    read_line = file_0300_avg.readline()
    while read_line != '':
        if read_line != '\n':
            set_0300.append(ast.literal_eval(read_line))
        read_line = file_0300_avg.readline()

    read_line = file_0400_avg.readline()
    while read_line != '':
        if read_line != '\n':
            set_0400.append(ast.literal_eval(read_line))
        read_line = file_0400_avg.readline()

    read_line = file_0500_avg.readline()
    while read_line != '':
        if read_line != '\n':
            set_0500.append(ast.literal_eval(read_line))
        read_line = file_0500_avg.readline()


    file_0100_avg.close()
    file_0200_avg.close()
    file_0300_avg.close()
    file_0400_avg.close()
    file_0500_avg.close()


    # Use result values.
    plot_total_time_vs_node_count(set_0100, set_0200, set_0300, set_0400, set_0500)
    plot_creation_time_vs_node_count(set_0100, set_0200, set_0300, set_0400, set_0500)
    plot_algorithm_time_vs_node_count(set_0100, set_0200, set_0300, set_0400, set_0500)
    plot_sparse_node_matches_vs_node_count(set_0100, set_0200, set_0300, set_0400, set_0500)
    plot_middle_node_matches_vs_node_count(set_0100, set_0200, set_0300, set_0400, set_0500)
    plot_dense_node_matches_vs_node_count(set_0100, set_0200, set_0300, set_0400, set_0500)


def plot_total_time_vs_node_count(set_0100, set_0200, set_0300, set_0400, set_0500):
    pyplot.plot(
        [
            set_0100[0]['nodes_handled'],
            set_0200[0]['nodes_handled'],
            set_0300[0]['nodes_handled'],
            set_0400[0]['nodes_handled'],
            set_0500[0]['nodes_handled'],
        ],
        [
            set_0100[0]['total_time'],
            set_0200[0]['total_time'],
            set_0300[0]['total_time'],
            set_0400[0]['total_time'],
            set_0500[0]['total_time'],
        ]
    )
    pyplot.plot(
        [
            set_0100[8]['nodes_handled'],
            set_0200[8]['nodes_handled'],
            set_0300[8]['nodes_handled'],
            set_0400[8]['nodes_handled'],
            set_0500[8]['nodes_handled'],
        ],
        [
            set_0100[8]['total_time'],
            set_0200[8]['total_time'],
            set_0300[8]['total_time'],
            set_0400[8]['total_time'],
            set_0500[8]['total_time'],
        ],
        'r',
    )
    pyplot.plot(
        [
            set_0100[16]['nodes_handled'],
            set_0200[16]['nodes_handled'],
            set_0300[16]['nodes_handled'],
            set_0400[16]['nodes_handled'],
            set_0500[16]['nodes_handled'],
        ],
        [
            set_0100[16]['total_time'],
            set_0200[16]['total_time'],
            set_0300[16]['total_time'],
            set_0400[16]['total_time'],
            set_0500[16]['total_time'],
        ],
        'g',
    )
    pyplot.title('Node Count Vs Average Total Time')
    pyplot.xlabel('Average Node Count')
    pyplot.ylabel('Average Total Time\nIn Seconds')
    label_1 = patches.Patch(color='blue', label='Sparse-Connectivity Graph Sets')
    label_2 = patches.Patch(color='red', label='Middle-Connectivity Graph Sets')
    label_3 = patches.Patch(color='green', label='Dense-Connectivity Graph Sets')
    pyplot.legend(handles=[label_1, label_2, label_3])
    pyplot.show()

def plot_creation_time_vs_node_count(set_0100, set_0200, set_0300, set_0400, set_0500):
    pyplot.plot([
        set_0100[0]['nodes_handled'],
        set_0200[0]['nodes_handled'],
        set_0300[0]['nodes_handled'],
        set_0400[0]['nodes_handled'],
        set_0500[0]['nodes_handled'],
    ], [
        (set_0100[0]['first_graph_creation'] + set_0100[0]['second_graph_creation']),
        (set_0200[0]['first_graph_creation'] + set_0200[0]['second_graph_creation']),
        (set_0300[0]['first_graph_creation'] + set_0300[0]['second_graph_creation']),
        (set_0400[0]['first_graph_creation'] + set_0400[0]['second_graph_creation']),
        (set_0500[0]['first_graph_creation'] + set_0500[0]['second_graph_creation']),
    ])
    pyplot.plot(
        [
            set_0100[8]['nodes_handled'],
            set_0200[8]['nodes_handled'],
            set_0300[8]['nodes_handled'],
            set_0400[8]['nodes_handled'],
            set_0500[8]['nodes_handled'],
        ],
        [
            (set_0100[8]['first_graph_creation'] + set_0100[8]['second_graph_creation']),
            (set_0200[8]['first_graph_creation'] + set_0200[8]['second_graph_creation']),
            (set_0300[8]['first_graph_creation'] + set_0300[8]['second_graph_creation']),
            (set_0400[8]['first_graph_creation'] + set_0400[8]['second_graph_creation']),
            (set_0500[8]['first_graph_creation'] + set_0500[8]['second_graph_creation']),
        ],
        'r',
    )
    pyplot.plot(
        [
            set_0100[16]['nodes_handled'],
            set_0200[16]['nodes_handled'],
            set_0300[16]['nodes_handled'],
            set_0400[16]['nodes_handled'],
            set_0500[16]['nodes_handled'],
        ],
        [
            (set_0100[16]['first_graph_creation'] + set_0100[16]['second_graph_creation']),
            (set_0200[16]['first_graph_creation'] + set_0200[16]['second_graph_creation']),
            (set_0300[16]['first_graph_creation'] + set_0300[16]['second_graph_creation']),
            (set_0400[16]['first_graph_creation'] + set_0400[16]['second_graph_creation']),
            (set_0500[16]['first_graph_creation'] + set_0500[16]['second_graph_creation']),
        ],
        'g',
    )
    pyplot.title('Node Count Vs Average Graph Creation Time')
    pyplot.xlabel('Average Node Count')
    pyplot.ylabel('Average Graph Creation Time\nIn Seconds')
    label_1 = patches.Patch(color='blue', label='Sparse-Connectivity Graph Sets')
    label_2 = patches.Patch(color='red', label='Middle-Connectivity Graph Sets')
    label_3 = patches.Patch(color='green', label='Dense-Connectivity Graph Sets')
    pyplot.legend(handles=[label_1, label_2, label_3])
    pyplot.show()

def plot_algorithm_time_vs_node_count(set_0100, set_0200, set_0300, set_0400, set_0500):
    pyplot.plot([
        set_0100[0]['nodes_handled'],
        set_0200[0]['nodes_handled'],
        set_0300[0]['nodes_handled'],
        set_0400[0]['nodes_handled'],
        set_0500[0]['nodes_handled'],
    ], [
        (set_0100[0]['edge_sort_time'] + set_0100[0]['greatest_constraints_time'] + set_0100[0]['match_time']),
        (set_0200[0]['edge_sort_time'] + set_0200[0]['greatest_constraints_time'] + set_0200[0]['match_time']),
        (set_0300[0]['edge_sort_time'] + set_0300[0]['greatest_constraints_time'] + set_0300[0]['match_time']),
        (set_0400[0]['edge_sort_time'] + set_0400[0]['greatest_constraints_time'] + set_0400[0]['match_time']),
        (set_0500[0]['edge_sort_time'] + set_0500[0]['greatest_constraints_time'] + set_0500[0]['match_time']),
    ])
    pyplot.plot(
        [
            set_0100[8]['nodes_handled'],
            set_0200[8]['nodes_handled'],
            set_0300[8]['nodes_handled'],
            set_0400[8]['nodes_handled'],
            set_0500[8]['nodes_handled'],
        ],
        [
            (set_0100[8]['edge_sort_time'] + set_0100[8]['greatest_constraints_time'] + set_0100[8]['match_time']),
            (set_0200[8]['edge_sort_time'] + set_0200[8]['greatest_constraints_time'] + set_0200[8]['match_time']),
            (set_0300[8]['edge_sort_time'] + set_0300[8]['greatest_constraints_time'] + set_0300[8]['match_time']),
            (set_0400[8]['edge_sort_time'] + set_0400[8]['greatest_constraints_time'] + set_0400[8]['match_time']),
            (set_0500[8]['edge_sort_time'] + set_0500[8]['greatest_constraints_time'] + set_0500[8]['match_time']),
        ],
        'r',
    )
    pyplot.plot(
        [
            set_0100[16]['nodes_handled'],
            set_0200[16]['nodes_handled'],
            set_0300[16]['nodes_handled'],
            set_0400[16]['nodes_handled'],
            set_0500[16]['nodes_handled'],
        ],
        [
            (set_0100[16]['edge_sort_time'] + set_0100[16]['greatest_constraints_time'] + set_0100[16]['match_time']),
            (set_0200[16]['edge_sort_time'] + set_0200[16]['greatest_constraints_time'] + set_0200[16]['match_time']),
            (set_0300[16]['edge_sort_time'] + set_0300[16]['greatest_constraints_time'] + set_0300[16]['match_time']),
            (set_0400[16]['edge_sort_time'] + set_0400[16]['greatest_constraints_time'] + set_0400[16]['match_time']),
            (set_0500[16]['edge_sort_time'] + set_0500[16]['greatest_constraints_time'] + set_0500[16]['match_time']),
        ],
        'g',
    )
    pyplot.title('Node Count Vs Average Algorithm Time')
    pyplot.xlabel('Average Node Count')
    pyplot.ylabel('Average Algorithm Time\nIn Seconds')
    label_1 = patches.Patch(color='blue', label='Sparse-Connectivity Graph Sets')
    label_2 = patches.Patch(color='red', label='Middle-Connectivity Graph Sets')
    label_3 = patches.Patch(color='green', label='Dense-Connectivity Graph Sets')
    pyplot.legend(handles=[label_1, label_2, label_3])
    pyplot.show()

def plot_sparse_node_matches_vs_node_count(set_0100, set_0200, set_0300, set_0400, set_0500):
    pyplot.plot(
        [
            set_0100[2]['nodes_handled'],
            set_0200[2]['nodes_handled'],
            set_0300[2]['nodes_handled'],
            set_0400[2]['nodes_handled'],
            set_0500[2]['nodes_handled'],
        ],
        [
            set_0100[2]['node_matches'],
            set_0200[2]['node_matches'],
            set_0300[2]['node_matches'],
            set_0400[2]['node_matches'],
            set_0500[2]['node_matches'],
        ]
    )
    pyplot.plot(
        [
            set_0100[4]['nodes_handled'],
            set_0200[4]['nodes_handled'],
            set_0300[4]['nodes_handled'],
            set_0400[4]['nodes_handled'],
            set_0500[4]['nodes_handled'],
        ],
        [
            set_0100[4]['node_matches'],
            set_0200[4]['node_matches'],
            set_0300[4]['node_matches'],
            set_0400[4]['node_matches'],
            set_0500[4]['node_matches'],
        ],
        'r',
    )
    pyplot.plot(
        [
            set_0100[6]['nodes_handled'],
            set_0200[6]['nodes_handled'],
            set_0300[6]['nodes_handled'],
            set_0400[6]['nodes_handled'],
            set_0500[6]['nodes_handled'],
        ],
        [
            set_0100[6]['node_matches'],
            set_0200[6]['node_matches'],
            set_0300[6]['node_matches'],
            set_0400[6]['node_matches'],
            set_0500[6]['node_matches'],
        ],
        'g',
    )
    pyplot.title('Sparse-Connectivity Graph\nNode Count Vs Average Matches Found')
    pyplot.xlabel('Average Node Count')
    pyplot.ylabel('Average Pairs of Matches Found')
    label_1 = patches.Patch(color='blue', label='Less than 33% Node Removal')
    label_2 = patches.Patch(color='red', label='Between 33% and 66% Node Removal')
    label_3 = patches.Patch(color='green', label='Above 66% Node Removal')
    pyplot.legend(handles=[label_1, label_2, label_3])
    pyplot.show()

def plot_middle_node_matches_vs_node_count(set_0100, set_0200, set_0300, set_0400, set_0500):
    pyplot.plot(
        [
            set_0100[10]['nodes_handled'],
            set_0200[10]['nodes_handled'],
            set_0300[10]['nodes_handled'],
            set_0400[10]['nodes_handled'],
            set_0500[10]['nodes_handled'],
        ],
        [
            set_0100[10]['node_matches'],
            set_0200[10]['node_matches'],
            set_0300[10]['node_matches'],
            set_0400[10]['node_matches'],
            set_0500[10]['node_matches'],
        ]
    )
    pyplot.plot(
        [
            set_0100[12]['nodes_handled'],
            set_0200[12]['nodes_handled'],
            set_0300[12]['nodes_handled'],
            set_0400[12]['nodes_handled'],
            set_0500[12]['nodes_handled'],
        ],
        [
            set_0100[12]['node_matches'],
            set_0200[12]['node_matches'],
            set_0300[12]['node_matches'],
            set_0400[12]['node_matches'],
            set_0500[12]['node_matches'],
        ],
        'r',
    )
    pyplot.plot(
        [
            set_0100[14]['nodes_handled'],
            set_0200[14]['nodes_handled'],
            set_0300[14]['nodes_handled'],
            set_0400[14]['nodes_handled'],
            set_0500[14]['nodes_handled'],
        ],
        [
            set_0100[14]['node_matches'],
            set_0200[14]['node_matches'],
            set_0300[14]['node_matches'],
            set_0400[14]['node_matches'],
            set_0500[14]['node_matches'],
        ],
        'g',
    )
    pyplot.title('Middle-Connectivity Graph\nNode Count Vs Average Matches Found')
    pyplot.xlabel('Average Node Count')
    pyplot.ylabel('Average Pairs of Matches Found')
    label_1 = patches.Patch(color='blue', label='Less than 33% Node Removal')
    label_2 = patches.Patch(color='red', label='Between 33% and 66% Node Removal')
    label_3 = patches.Patch(color='green', label='Above 66% Node Removal')
    pyplot.legend(handles=[label_1, label_2, label_3])
    pyplot.show()

def plot_dense_node_matches_vs_node_count(set_0100, set_0200, set_0300, set_0400, set_0500):
    pyplot.plot(
        [
            set_0100[18]['nodes_handled'],
            set_0200[18]['nodes_handled'],
            set_0300[18]['nodes_handled'],
            set_0400[18]['nodes_handled'],
            set_0500[18]['nodes_handled'],
        ],
        [
            set_0100[18]['node_matches'],
            set_0200[18]['node_matches'],
            set_0300[18]['node_matches'],
            set_0400[18]['node_matches'],
            set_0500[18]['node_matches'],
        ]
    )
    pyplot.plot(
        [
            set_0100[20]['nodes_handled'],
            set_0200[20]['nodes_handled'],
            set_0300[20]['nodes_handled'],
            set_0400[20]['nodes_handled'],
            set_0500[20]['nodes_handled'],
        ],
        [
            set_0100[20]['node_matches'],
            set_0200[20]['node_matches'],
            set_0300[20]['node_matches'],
            set_0400[20]['node_matches'],
            set_0500[20]['node_matches'],
        ],
        'r',
    )
    pyplot.plot(
        [
            set_0100[22]['nodes_handled'],
            set_0200[22]['nodes_handled'],
            set_0300[22]['nodes_handled'],
            set_0400[22]['nodes_handled'],
            set_0500[22]['nodes_handled'],
        ],
        [
            set_0100[22]['node_matches'],
            set_0200[22]['node_matches'],
            set_0300[22]['node_matches'],
            set_0400[22]['node_matches'],
            set_0500[22]['node_matches'],
        ],
        'g',
    )
    pyplot.title('Dense-Connectivity Graph\nNode Count Vs Average Matches Found')
    pyplot.xlabel('Average Node Count')
    pyplot.ylabel('Average Pairs of Matches Found')
    label_1 = patches.Patch(color='blue', label='Less than 33% Node Removal')
    label_2 = patches.Patch(color='red', label='Between 33% and 66% Node Removal')
    label_3 = patches.Patch(color='green', label='Above 66% Node Removal')
    pyplot.legend(handles=[label_1, label_2, label_3])
    pyplot.show()


if __name__ == '__main__':
    main()
