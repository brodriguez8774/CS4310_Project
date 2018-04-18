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
        # logger.info('Creating new random graph.')
        new_graph = graph.Graph()

        # Determine total node count for graph.
        node_count = random.randint(min_nodes, max_nodes)
        # logger.info('Selected node count is {0}'.format(node_count))

        # First create all nodes.
        index = 0
        while index < node_count:
            # logger.info('Creating node {0}'.format(index))
            new_graph.add_node()
            index += 1

        # Now create loop through all nodes, randomly creating edges for each node.
        # logger.info('Initial node creation complete. Now creating node edges.')
        index = 0
        while index < node_count:
            # logger.info('Creating edges for node {0}'.format(index))
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
                # logger.info('\n')

                edge_index = random.randint(0, (edge_counter - 1))

                # logger.info('Edges to Add (Edge Counter): {0}'.format(edge_counter))
                # logger.info('Total nodes:   {0}'.format(node_count))
                # logger.info('Next Edge Index to Add: {0}'.format(edge_index))
                # logger.info('Current List Length: {0}'.format(len(node_list)))

                edge_to_add = node_list.pop(edge_index)


                in_or_out = random.randint(0, 1)
                if in_or_out == 0:
                    current_node.add_edge(edges_in=[edge_to_add, ])
                else:
                    current_node.add_edge(edges_out=[edge_to_add, ])

                edge_counter -= 1

            index += 1

        # logger.info('Randomized graph created.')
        return new_graph

    def copy_graph(self, initial_graph, remove_nodes=False, min_percent_removal=10, max_percent_removal=90):
        """
        Copies provided graph nodes into new graph.
        Optionally removes a random number of nodes, based on min and max values.
        Note that these values are simply used to generate random removal values. There is no gaurantee that
        an exact percentage of nodes will actually be removed. It's just statistically likely.
        :param initial_graph:
        :param remove_nodes: Bool to determine if nodes shall be randomly removed or not.
        :param min_percent_removal: Minimum possible percent to remove.
        :param max_percent_removal: Maximum possible percent to remove.
        :return: Newly created graph.
        """
        # logger.info('Copying graph with node removal set to {0}'.format(remove_nodes))

        # First create new graph.
        new_graph = graph.Graph()
        removal_list = []
        random.seed()
        if min_percent_removal > 90:
            min_percent_removal = 90
        if min_percent_removal > max_percent_removal:
            max_percent_removal = min_percent_removal
        percent_to_remove = random.randint(min_percent_removal, max_percent_removal)
        # if remove_nodes:
            # logger.info('{0}% chance to remove a node.'.format(percent_to_remove))

        # Iterate through all initial_graph values, creating an equivalent node for each one.
        # Only adding nodes initially helps prevent errors with edge handling.
        for key, value in initial_graph.nodes.items():
            new_graph.add_node(name=value.name, data=value.data)

            if remove_nodes:
                # Chance to remove node. If this value is less than "percent_to_remove", then node is to be removed.
                random_chance = random.randint(0, 100)
                if random_chance < percent_to_remove:
                    # Node is chosen for removal. Add to list.
                    removal_list.append(value)

        # Now add edges, since all nodes are now present. Done after node adding to help prevent errors.
        for key, value in initial_graph.nodes.items():
            edges_in = []
            edges_out = []

            node = new_graph.get_node(value.identifier)
            for edge in initial_graph.get_node(value.identifier).edges_in:
                edges_in.append(new_graph.get_node(edge.identifier))
            for edge in initial_graph.get_node(value.identifier).edges_out:
                edges_out.append(new_graph.get_node(edge.identifier))

            node.add_edge(edges_in=edges_in, edges_out=edges_out)

        # Graph is created. Now remove all items in removal list. Done here so all edges should stay intact.
        removal_count = 0
        for removal_node in removal_list:
            # Gaurantee that, at worse case scenario, at least one node will remain in the new graph.
            if len(new_graph.edge_count_list) > 1:
                new_graph.remove_node(removal_node.identifier)
                removal_count += 1

        # logger.info('Graph copied with {0} nodes removed.'.format(removal_count))

        return new_graph
