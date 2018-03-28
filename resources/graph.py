"""
Graph/Node classes.
Will be used as core data representation for program.
"""

# System Imports.
import types

# User Class Imports.
from resources import logging


# Initialize logging.
logger = logging.get_logger(__name__)


class Graph():
    """
    A standard graph.
    Will be comprised of graph nodes.
    """
    def __init__(self, *args, **kwargs):
        self.name = None        # Optional name to identify graph.
        self._nodes = {}        # Dict object of all nodes within graph.
        self._auto_counter = 0  # Int to count "nameless" nodes added to graph.

        # Attempt to set name.
        try:
            self.name = kwargs['name']
        except KeyError:
            pass

    def auto_count(self):
        """
        Increments the auto_counter var and returns count number for dict key.
        Should only be called if node does not have a real name.
        :return: Counter value to use as dict key for node.
        """
        current = self._auto_counter
        self._auto_counter += 1
        return current

    def get_node_keys(self):
        """
        Returns list of all nodes keys in graph.
        """
        node_list = self._nodes.keys()
        if self.name is not None:
            logger.info('Graph {0}\'s Node List: {1}'.format(str(self.name), str(node_list)))
        else:
            logger.info('Graph\'s Node List: {0}'.format(str(node_list)))
        return node_list

    def get_node(self, key):
        """
        Returns node found at provided key.
        :param key: Dict key to find node at.
        :return: Found node.
        """
        try:
            return self._nodes[key]
        except KeyError:
            logger.warn('Invalid key passed. Cannot locate node in graph.')

    def add_node(self, name=None, edges_to=None, edges_from=None):
        """
        Adds new node to graph.
        """
        new_node = Node(name=name)
        if edges_to is not None or edges_from is not None:
            new_node.add_edge(edges_to, edges_from)
        if new_node.name is not None:
            self._nodes[new_node.name] = new_node
        else:
            count_value = self.auto_count()
            new_node.identifier = count_value
            self._nodes[count_value] = new_node

    def remove_node(self, key):
        """
        Removes node with given key from graph dict.
        :param key: Dict key to find node at.
        :return: Removed node.
        """
        try:
            # Find and remove node from graph.
            removed_node = self._nodes[key]
            del self._nodes[key]

            # Find and remove node from all associated "edge_to" lists.
            # First check if removed node even has "edges from".
            if not removed_node.edges_from:
                for edge_node in removed_node.edges_from:
                    # Find in "edge_to" list and remove.
                    edge_node.edge_to.remove(removed_node)


            # Find and remove node from all associated "edge_from" lists.
            # First check if removed node even has "edges to".
            if not removed_node.edges_to:
                for edge_node in removed_node.edges_to:
                    # Find in "edge_from" list and remove.
                    edge_node.edge_from.remove(removed_node)

            return removed_node
        except KeyError:
            logger.warn('Invalid key passed. Cannot remove node from graph.')

    def info_string(self, only_name=False, only_edges_to=False, only_edges_from=False):
        """
        Returns information about graph.
        Can set any arg to True to only return info for the related value.
        """
        return_string = ''
        for node in self._nodes:
            node = self.get_node(node)  # Convert from String object to actual object by calling get_node function.
            return_string += ' { '
            return_string += node.info_string(
                only_name=only_name,
                only_edges_to=only_edges_to,
                only_edges_from=only_edges_from)
            return_string += ' } '
        return return_string


class Node():
    """
    A single node within a graph.
    """
    def __init__(self, *args, **kwargs):

        self.name = None        # Optional name to identify node.
        self.identifier = None  # Identifier to identify node within dict. Same as name if name is present.
        self.edges_to = []      # List of all edges leading to node.
        self.edges_from = []    # List of all edges leading from node.

        # Attempt to set name and identifier.
        try:
            self.name = kwargs['name']
            self.identifier = self.name
        except KeyError:
            pass

    def __str__(self):
        return '{0}'.format(self._get_name())

    def _get_name(self):
        """
        Returns proper name of node.
        """
        if self.name is not None:
            return self.name
        else:
            return '{ {0} : {1} }'.format(str(self.edges_to), str(self.edges_from))

    def add_edge(self, edges_to=None, edges_from=None):
        """
        Adds a edge(s) to node.
        :param edges_to: New edge(s) leading to node.
        :param edges_from: New edge(s) leading from node.
        """
        edges_found = False

        # Check if edge_to is populated and of type list.
        if edges_to is not None and edges_to is list:
            for edge in edges_to:
                self.edges_to.append(edge)
            edges_found = True

        # Check if edge_from is populated and of type list.
        if edges_from is not None and edges_to is list:
            for edge in edges_from:
                self.edges_from.append(edge)
            edges_found = True

        # No valid edges passed. Display warning.
        if edges_found is False:
            logger.warn('Add edge function called on {0} but no edges passed.'.format(self._get_name()))

    def info_string(self, only_name=False, only_edges_to=False, only_edges_from=False):
        """
        Returns information about node.
        Can set any arg to True to only return info for the related value.
        """
        return_string = ''

        if not only_edges_to and not only_edges_from:
            # Get name info. If None, then get identifier instead.
            return_string += 'Node: '
            if self.name is not None:
                return_string += '{0}'.format(str(self.name))
            else:
                return_string += '{0}'.format(str(self.identifier))

        elif not only_name and not only_edges_from:
            # Get edges_to list info.
            if return_string != '':
                return_string += ' | '
                return_string += 'Edges To: '
            return_string += '{0}'.format(str(self.edges_to))

        elif not only_name and not only_edges_to:
            # Get edges_from list info.
            if return_string != '':
                return_string += ' | '
            return_string += 'Edges From: '
            return_string += '{0}'.format(str(self.edges_from))

        return str(return_string)

