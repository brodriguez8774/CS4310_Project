"""
Graph/Node classes.
Will be used as core data representation for program.
"""

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
        self.nodes = {}        # Dict object of all nodes within graph.
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
        node_list = self.nodes.keys()
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
            return self.nodes[key]
        except KeyError:
            logger.warning('Invalid key passed. Cannot locate node in graph.')
            return None

    def add_node(self, name=None, edges_in=None, edges_out=None):
        """
        Adds new node to graph.
        """
        new_node = Node(name=name)
        if edges_in is not None or edges_out is not None:
            new_node.add_edge(edges_in, edges_out)
        if new_node.name is None:
            count_value = self.auto_count()
            new_node.identifier = count_value
        self.nodes[new_node.identifier] = new_node

        return new_node

    def remove_node(self, key):
        """
        Removes node with given key from graph dict.
        :param key: Dict key to find node at.
        :return: Removed node.
        """
        try:
            # Find and remove node from graph.
            removed_node = self.nodes[key]
            del self.nodes[key]

            # Find and remove node from all associated "edges_in" lists.
            # First check if removed node even has "edges out".
            if removed_node.edges_out:
                temp_list = list(removed_node.edges_out)
                for edge_node in temp_list:
                    # Find in "edges_in" list and remove.
                    edge_node.remove_edge(edges_in=[removed_node, ])

            # Find and remove node from all associated "edges_out" lists.
            # First check if removed node even has "edges in".
            if removed_node.edges_in:
                temp_list = list(removed_node.edges_in)
                for edge_node in temp_list:
                    # Find in "edges_out" list and remove.
                    edge_node.remove_edge(edges_out=[removed_node, ])

            return removed_node
        except KeyError:
            logger.warning('Invalid key passed. Cannot remove node from graph.')

    def drop_all_edges(self):
        """
        Clears all edges associated with graph's nodes
        """
        for key, value in self.nodes.items():
            node = self.get_node(key)
            node.edges_in = []
            node.edges_out = []

    def drop_all_nodes(self):
        """
        Removes all nodes and associated edges from graph.
        """
        temp_dict = dict(self.nodes)
        for key, value in temp_dict.items():
            del self.nodes[key]

    def info_string(self, only_name=False, only_edges_in=False, only_edges_out=False):
        """
        Returns information about graph.
        Can set any arg to True to only return info for the related value.
        """
        return_string = ''
        for node in self.nodes:
            node = self.get_node(node)  # Convert from String object to actual object by calling get_node function.
            return_string += ' { '
            return_string += node.info_string(
                only_name=only_name,
                only_edges_in=only_edges_in,
                only_edges_out=only_edges_out)
            return_string += ' } '
        return return_string


class Node():
    """
    A single node within a graph.
    """
    def __init__(self, *args, **kwargs):

        self.name = None        # Optional name to identify node.
        self.identifier = None  # Identifier to identify node within dict. Same as name if name is present.
        self.edges_in = []      # List of all edges leading in to node.
        self.edges_out = []     # List of all edges leading out from node.
        self.data = None        # Undefined data value for node to hold at a future date.

        # Attempt to set name and identifier.
        try:
            self.name = kwargs['name']
            self.identifier = self.name
        except KeyError:
            pass

    def __str__(self):
        return '{0}'.format(self.identifier)

    def add_edge(self, edges_in=None, edges_out=None):
        """
        Adds a edge(s) to node.
        :param edges_in: New edge(s) leading to node.
        :param edges_out: New edge(s) leading from node.
        """
        edges_found = False

        # Check if edges_in is populated and of type list.
        if edges_in is not None and isinstance(edges_in, list):
            for edge_node in edges_in:
                # Check that list object is of type Node.
                if isinstance(edge_node, Node):
                    # Check that edge_node is not self.
                    if edge_node is not self:
                        # Finally, check that edge does not already exist in list of connecting edges.
                        if not edge_node in self.edges_in:
                            self.edges_in.append(edge_node)
                            logger.info('Appending node {0} to {1}\'s "edges_in" list.'.format(str(edge_node), str(self)))
                        else:
                            logger.info('Node {0} already in "edges_in" list. Skipping add.'.format(str(edge_node)))
                        if not self in edge_node.edges_out:
                            edge_node.edges_out.append(self)
                            logger.info('Appending node {0} to {1}\'s "edges_in" list.'.format(str(self), str(edge_node)))
                        else:
                            logger.info('Node {0} already in "edges_out" list. Skipping add.'.format(str(self)))
                    else:
                        logger.info('Node {0} attempting to add self as "edges_in". Skipping add.'.format(str(self)))
                else:
                    logger.warning('Passed "edges_in" list item {0} is not a Node object. Cannot add.'.format(str(edge_node)))
            edges_found = True

        # Check if edges_out is populated and of type list.
        if edges_out is not None and isinstance(edges_out, list):
            for edge_node in edges_out:
                # Check that list object is of type Node.
                if isinstance(edge_node, Node):
                    # Check that edge_node is not self.
                    if edge_node is not self:
                        # Finally, check that edge does not already exist in connecting edges.
                        if not edge_node in self.edges_out:
                            self.edges_out.append(edge_node)
                            logger.info('Appending node {0} to {1}\'s "edges_in" list.'.format(str(edge_node), str(self)))
                        else:
                            logger.info('Node {0} already in "edges_out" list. Skipping add.'.format(str(edge_node)))
                        if not self in edge_node.edges_in:
                            edge_node.edges_in.append(self)
                            logger.info('Appending node {0} to {1}\'s "edges_in" list.'.format(str(self), str(edge_node)))
                        else:
                            logger.info('Node {0} already in "edges_in" list. Skipping add.'.format(str(self)))
                    else:
                        logger.info('Node {0} attempting to add self as "edges_out". Skipping add.'.format(str(self)))
                else:
                    logger.warning('Passed "edges_out" list item {0} is not a Node object. Cannot add.'.format(str(edge_node)))
            edges_found = True

        # No valid edges passed. Display warning.
        if edges_found is False:
            logger.warning('Add edge function called on {0} but no edges passed.'.format(str(self)))

    def remove_edge(self, edges_in=None, edges_out=None):
        """
        Removes node edge(s).
        :param edges_in: Edge(s) leading to node.
        :param edges_out: Edge(s) leading from node.
        """
        edges_found = False

        # Check if edges_in is populated and of type list.
        if edges_in is not None and isinstance(edges_in, list):
            for edge_node in edges_in:
                # Check that list object is of type Node.
                if isinstance(edge_node, Node):
                    # Check that edge_node is not self.
                    if edge_node is not self:
                        try:
                            self.edges_in.remove(edge_node)
                        except ValueError:
                            logger.info('Node {0} is not connected by edge to {1}.'.format(str(edge_node), str(self)))
                        try:
                            edge_node.edges_out.remove(self)
                        except ValueError:
                            logger.info('Node {0} is not connected by edge to {1}.'.format(str(edge_node), str(self)))
                    else:
                        logger.info('Node {0} attempting to remove self from "edges_in". Skipping add.'.format(str(self)))
                else:
                    logger.warning('Passed "edges_out" list item {0} is not a Node object. Cannot add.'.format(str(edge_node)))
            edges_found = True

        # Check if edge_out is populated and of type list.
        if edges_out is not None and isinstance(edges_out, list):
            for edge_node in edges_out:
                # Check that list object is of type Node.
                if isinstance(edge_node, Node):
                    # Check that edge_node is not self.
                    if edge_node is not self:
                        try:
                            self.edges_out.remove(edge_node)
                        except ValueError:
                            logger.info('Node {0} is not connected by edge to {1}.'.format(str(edge_node), str(self)))
                        try:
                            edge_node.edges_in.remove(self)
                        except ValueError:
                            logger.info('Node {0} is not connected by edge to {1}.'.format(str(edge_node), str(self)))
                    else:
                        logger.info(
                            'Node {0} attempting to remove self from "edges_out". Skipping add.'.format(str(self)))
                else:
                    logger.warning('Passed "edges_out" list item {0} is not a Node object. Cannot add.'.format(str(edge_node)))
            edges_found = True

        # No valid edges passed. Display warning.
        if edges_found is False:
            logger.warning('Remove edge function called on {0} but no edges passed.'.format(str(self)))

    def drop_all_edges(self):
        """
        Dirty way to drop all associated edges.
        Does not affect connected nodes.
        """
        self.edges_in = []
        self.edges_out = []

    def info_string(self, only_name=False, only_edges_in=False, only_edges_out=False):
        """
        Returns information about node.
        Can set any arg to True to only return info for the related value.
        """
        return_string = ''

        if not only_edges_in and not only_edges_out:
            # Get name info. If None, then get identifier instead.
            return_string += 'Node: '
            if self.name is not None:
                return_string += '{0}'.format(str(self.name))
            else:
                return_string += '{0}'.format(str(self.identifier))

        if not only_name and not only_edges_out:
            # Get edges_in list info.
            if self.edges_in:
                if return_string != '':
                    return_string += ' | '

                return_string += 'Edges To: ['
                for edge_node in self.edges_in:
                    return_string += ' {0},'.format(str(edge_node))
                return_string += ' ]'

        if not only_name and not only_edges_in:
            # Get edges_out list info.
            if self.edges_out:
                if return_string != '':
                    return_string += ' | '

                return_string += 'Edges From: ['
                for edge_node in self.edges_out:
                    return_string += ' {0},'.format(str(edge_node))
                return_string += ' ]'

        return str(return_string)
