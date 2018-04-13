"""
Core/Start of program.
"""

# System Imports.


# User Class Imports.
from resources import graph, logging
import data_mapping


# Initialize logging.
logger = logging.get_logger(__name__)


# Core program here.
logger.info('Starting program.')

# Create test graph.
test_graph_1 = graph.Graph('Test Graph')
node_0 = test_graph_1.add_node()
node_1 = test_graph_1.add_node(edges_in=[node_0, ])
node_2 = test_graph_1.add_node(edges_in=[node_1, ])
node_3 = test_graph_1.add_node(edges_in=[node_2, ])
node_4 = test_graph_1.add_node(edges_in=[node_3, ], edges_out=[node_0, ])
test_graph_1.sort_node_edge_lists()

# Map graph to visual representation.
# mapper = data_mapping.DataMapping(test_graph_1, None)
# mapper.draw_map()


# Reset graph connections.
# test_graph.drop_all_nodes()
test_graph_2 = graph.Graph()

# Draw new connections.
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
mapper.draw_bw_map(1, False)
mapper.draw_color_map(1, False)
mapper.draw_bw_map(2, False)
mapper.draw_color_map(2, False)

# Side by side maps.
mapper.draw_side_by_side_bw_maps(False)
mapper.draw_side_by_side_color_maps(False)


# Program termination and clean up.
logger.info('Terminating program.')
