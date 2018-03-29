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
test_graph = graph.Graph('Test Graph')
node_0 = test_graph.add_node()
node_1 = test_graph.add_node(edges_in=[node_0, ])
node_2 = test_graph.add_node(edges_in=[node_1, ])
node_3 = test_graph.add_node(edges_in=[node_2, ])
node_4 = test_graph.add_node(edges_in=[node_3, ], edges_out=[node_0, ])
logger.info(test_graph.info_string())

# Map graph to visual representation.
mapper = data_mapping.DataMap(test_graph)
mapper.draw_map()


# Reset graph connections.
test_graph.drop_all_nodes()

# Draw new connections.
node_0 = test_graph.add_node()
node_1 = test_graph.add_node(edges_in=[node_0, ])
node_2 = test_graph.add_node(edges_in=[node_1, ])
node_3 = test_graph.add_node(edges_in=[node_1, node_2, ], edges_out=[node_2,])
node_4 = test_graph.add_node(edges_in=[node_3, ], edges_out=[node_0, node_2, ])
mapper = data_mapping.DataMap(test_graph)
mapper.draw_map()


# Program termination and clean up.
logger.info('Terminating program.')
