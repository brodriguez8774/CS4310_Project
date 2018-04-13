"""
Handles randomly generating graphs.
"""

# System Imports.
import random

# User Class Imports.
from resources import graph, logging


# Initialize logging.
logger = logging.get_logger(__name__)


class RandomizedGrapher():
    """
    Handles creation of randomly generated graphs.
    """
    def __init__(self):
        random.seed()

    def create_graph(self, min_nodes=10, max_nodes=100, min_edges=0, max_edges=50, edge_complete=False):
        """
        Creates a random graph, using passed parameters as limits.
        Defaults to between 10 and 100 nodes, each having between 0 and 50 edges.
        """
        logger.info('Creating new random graph.')
        new_graph = graph.Graph()

        # Determine total node count for graph.
        node_count = random.randint(min_nodes, max_nodes)
        logger.info('Selected node count is {0}'.format(node_count))

        # First create all nodes.
        index = 0
        while index < node_count:
            # logger.info('Creating node {0}'.format(index))
            new_graph.add_node()
            index += 1

        # Now create loop through all nodes, randomly creating edges for each node.
        logger.info('Initial node creation complete. Now creating node edges.')
        index = 0
        while index < node_count:
            logger.info('Creating edges for node {0}'.format(index))
            current_node = new_graph.get_node(index)

            # Determine total edge count for current node.
            if min_edges > node_count:
                min_edges = node_count

            if max_edges > node_count:
                max_edges = node_count

            if edge_complete:
                # Create a complete graph. Every node will be connected to every other node.
                edge_counter = node_count
            else:
                edge_counter = random.randint(min_edges, max_edges)

            # Copy any arbitrary node list from graph object.
            node_list = list(new_graph.edge_count_list)

            # Continually add edges until counter hits 0.
            while edge_counter > 0:
                logger.info('\n')

                edge_index = random.randint(0, (edge_counter - 1))

                logger.info('Edges to Add (Edge Counter): {0}'.format(edge_counter))
                logger.info('Total nodes:   {0}'.format(node_count))
                logger.info('Next Edge Index to Add: {0}'.format(edge_index))
                logger.info('Current List Length: {0}'.format(len(node_list)))

                edge_to_add = node_list.pop(edge_index)


                in_or_out = random.randint(0, 1)
                if in_or_out == 0:
                    current_node.add_edge(edges_in=[edge_to_add, ])
                else:
                    current_node.add_edge(edges_out=[edge_to_add, ])

                edge_counter -= 1

            index += 1

        return new_graph

