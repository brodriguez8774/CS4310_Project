"""
Core/Start of program.
"""

# System Imports.


# User Class Imports.
from resources import graph, logging, randomized_grapher
import algorithm as alg
import data_mapping


# Initialize logging.
logger = logging.get_logger(__name__)


# Core program here.
logger.info('Starting program.')


# # Test randomly generated graph.
# random_grapher = randomized_grapher.RandomizedGrapher()
#
# a_graph = random_grapher.create_graph()
# # a_graph = random_grapher.create_graph(min_nodes=2, max_nodes=10, min_edges=0, max_edges=3)
# # a_graph = random_grapher.create_graph(min_nodes=2, max_nodes=10, edge_complete=True)
#
# mapper = data_mapping.DataMapping(a_graph, None)
# mapper.draw_color_map(1, True)



# # Test randomly generated graph that was copied from an original.
# random_grapher = randomized_grapher.RandomizedGrapher()
#
# a_graph_1 = random_grapher.create_graph(min_nodes=2, max_nodes=10, min_edges=0, max_edges=3)
# a_graph_2 = graph.Graph()
# for key, value in a_graph_1.nodes.items():
#     a_graph_2.append_node(value)
#
# mapper = data_mapping.DataMapping(a_graph_2, None)
# mapper.draw_color_map(1, True)



# # Create test graph.
# test_graph_1 = graph.Graph('Test Graph')
# node_0 = test_graph_1.add_node()
# node_1 = test_graph_1.add_node(edges_in=[node_0, ])
# node_2 = test_graph_1.add_node(edges_in=[node_1, ])
# node_3 = test_graph_1.add_node(edges_in=[node_2, ])
# node_4 = test_graph_1.add_node(edges_in=[node_3, ], edges_out=[node_0, ])
# test_graph_1.sort_node_edge_lists()
#
# # Map graph to visual representation.
# # mapper = data_mapping.DataMapping(test_graph_1, None)
# # mapper.draw_map()
#
#
# # Reset graph connections.
# # test_graph.drop_all_nodes()
# test_graph_2 = graph.Graph()
#
# # Draw new connections.
# node_0 = test_graph_2.add_node()
# node_1 = test_graph_2.add_node(edges_in=[node_0, ])
# node_2 = test_graph_2.add_node(edges_in=[node_1, ])
# node_3 = test_graph_2.add_node(edges_in=[node_1, node_2, ], edges_out=[node_2, ])
# node_4 = test_graph_2.add_node(edges_in=[node_3, ], edges_out=[node_0, node_2, ])
#
# # node_5 = test_graph_2.add_node(edges_in=[node_4], edges_out=[node_0, node_3], )
# # node_6 = test_graph_2.add_node(edges_in=[node_4, node_5], edges_out=[node_1], )
#
# # node_5 = test_graph_2.add_node(edges_in=[node_4, ], )
# # node_6 = test_graph_2.add_node(edges_in=[node_5, ], )
# # node_7 = test_graph_2.add_node(edges_in=[node_6, ], )
#
# # node_7 = test_graph_2.add_node()
#
# # Map graph to visual representation.
# test_graph_2.sort_node_edge_lists()
# mapper = data_mapping.DataMapping(test_graph_1, test_graph_2)
#
# # Single maps.
# mapper.draw_bw_map(1, False)
# mapper.draw_color_map(1, False)
# mapper.draw_bw_map(2, False)
# mapper.draw_color_map(2, False)
#
# # Side by side maps.
# mapper.draw_side_by_side_bw_maps(False)
# mapper.draw_side_by_side_color_maps(False)






# Full Algorithm Test.
random_grapher = randomized_grapher.RandomizedGrapher()
algorithm = alg.Algorithm()

# Create graph 1.
graph_1 = random_grapher.create_graph(min_nodes=2, max_nodes=8, min_edges=1, max_edges=3)

# Create graph 2.
graph_2 = graph.Graph()
for key, value in graph_1.nodes.items():
    graph_2.add_node(node=value)

# Extra values for graph 2.
a_node = graph_2.get_node(0)
graph_2.add_node(edges_in=[a_node, ])
graph_2.add_node()

# Compute first half of algorithm.
graph_1_ranking = algorithm.greatest_constraints_first(graph_1.edge_count_list)
graph_2_ranking = algorithm.greatest_constraints_first(graph_2.edge_count_list)

# Format list values.
graph_1_ranking = algorithm.condense_list(graph_1_ranking)
graph_2_ranking = algorithm.condense_list(graph_2_ranking)

logger.info('Formatted Graph 1 Ranking: {0}'.format(graph_1_ranking))
logger.info('Formatted Graph 2 Ranking: {0}'.format(graph_2_ranking))

# Compute second half of algorithm.
match_list = algorithm.matching(graph_1_ranking, graph_2_ranking)

logger.info('Match List: {0}'.format(match_list))

# Draw data.
mapper = data_mapping.DataMapping(graph_1, graph_2)

# mapper.draw_side_by_side_color_maps(True)
mapper.draw_matching_comparison(match_list)

# mapper = data_mapping.DataMapping(a_graph_2, None)
# mapper.draw_color_map(1, True)





# Program termination and clean up.
logger.info('Terminating program.')
