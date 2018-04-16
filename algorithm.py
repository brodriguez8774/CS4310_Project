"""
Attempt at Isomorphism algorithm.
"""

# User Class Imports.
from resources import graph, logging


# Initialize logging.
logger = logging.get_logger(__name__)


class Algorithm():
    """
    Attempt at Isomorhpism algorithm.
    """
    def __init__(self):
        self.vis_list = None
        self.neigh_list = None
        self.unv_list = None
        self.iterated_nodes = None

    def greatest_constraints_first(self, node_list_by_edge_count):
        """
        Attempts to define the "greatest constraints" for passed node list.
        :param node_list_by_edge_count: List of all nodes, sorted by number of edges per node.
        :return: Ranking list.
        """
        # Ensure list has at least 2 node values. Otherwise nothing to compare.
        if len(node_list_by_edge_count) < 2:
            return node_list_by_edge_count

        self.iterated_nodes = []
        self.iterated_nodes.append(node_list_by_edge_count[0])

        copy_list = list(node_list_by_edge_count)
        copy_list.pop(0)

        self.vis_list = []
        self.neigh_list = []
        self.unv_list = []
        ranking = None
        self.vis_list.append(node_list_by_edge_count[0])

        # Iterate through all remaining nodes and get score values.
        for current_node in copy_list:

            relationship_determined = False

            if not relationship_determined:
                relationship_determined = self._check_constraints_vis(current_node)

            if not relationship_determined:
                relationship_determined = self._check_constraints_neigh(current_node)

            # Did not meet criteria for above checks. Append to "unvisited" list.
            if not relationship_determined:
                self.unv_list.append(current_node)

            # self.iterated_nodes.append(current_node)

            # logger.info('Node: {0}'.format(current_node))
            # logger.info('vis_list: {0}'.format(self.vis_list))
            # logger.info('neig_list: {0}'.format(self.neigh_list))
            # logger.info('unv_list: {0}'.format(self.unv_list))
            ranking = [self.vis_list, self.neigh_list, self.unv_list]

            # Get parent of current node. Defined as node with smallest "index" and valid connection to current node.
            # TODO: Is "index" defined as index in edge_count list, or index of overall graph?? Does it even matter?
            if current_node.edges_in is not None and current_node.edges_in != []:
                current_node.parent = current_node.edges_in[0]  # First node should have the lowest respective index.

        # Return node rank list.
        return ranking

    def _check_constraints_vis(self, current_node):
        """
        Iterates through direct edges to check for valid vis relationship.
        :return: True if relationship is found. False if not.
        """
        relationship_determined = False

        # Iterate through all elements in interated_nodes list.
        for iterated_node in self.iterated_nodes:

            # Check that relationship has not been determined.
            if relationship_determined:
                break

            # Look through all inward edges.
            for edge in current_node.edges_in:
                # Check if edge and iterated the same. If so, append current to vis_list and skip other checks.
                if edge == iterated_node:
                    self.vis_list.append(current_node)
                    relationship_determined = True
                    break

            # Check that relationship has not been determined.
            if relationship_determined:
                break

            # Look through all outward edges.
            for edge in current_node.edges_out:
                # Check if edge and iterated the same. If so, append current to vis_list and skip other checks.
                if edge == iterated_node:
                    self.vis_list.append(current_node)
                    relationship_determined = True
                    break

        return relationship_determined

    def _check_constraints_neigh(self, current_node):
        """
        Iterates through direct edges to check for valid neigh relationship.
        :return: True if relationship is found. False if not.
        """
        relationship_determined = False

        # Iterate through all elements in iterated_nodes list.
        for iterated_node in self.iterated_nodes:

            # Check that relationship has not been determined.
            if relationship_determined:
                break

            # Look through all inward edges.
            for edge in current_node.edges_in:
                # Iterate through all neighbor edges in.
                for neigh_edge in edge.edges_in:
                    if neigh_edge == iterated_node:
                        self.neigh_list.append(current_node)
                        relationship_determined = True
                        break

                # Check that relationship has not been determined.
                if relationship_determined:
                    break

                # Iterate through all neighbor edges out.
                for neigh_edge in edge.edges_out:
                    if neigh_edge == iterated_node:
                        self.neigh_list.append(current_node)
                        relationship_determined = True
                        break

            # Check that relationship has not been determined.
            if relationship_determined:
                break

            # Look through all outward edges.
            for edge in current_node.edges_out:
                # Iterate through all neighbor edges in.
                for neigh_edge in edge.edges_in:
                    if neigh_edge == iterated_node:
                        self.neigh_list.append(current_node)
                        relationship_determined = True
                        break

                # Check that relationship has not been determined.
                if relationship_determined:
                    break

                # Iterate through all neighbor edges out.
                for neigh_edge in edge.edges_out:
                    if neigh_edge == iterated_node:
                        self.neigh_list.append(current_node)
                        relationship_determined = True
                        break

        return relationship_determined

    def condense_list(self, ranking_list):
        """
        Takes a "ranking_list" (created by the greatest constraints method) and converts the sublists to a single list.
        This single list is then passed into matching.
        Adds an additional O(3n) but greatly simplifies matching code (does not need to iterate through multiple sublists).
        :param ranking_list: List created by greatest constraints method.
        :return: Newly formatted list of rank values.
        """
        new_list = []

        if len(ranking_list) > 0:
            if ranking_list[0] is not None and ranking_list[0] is not []:
                if isinstance(ranking_list[0], graph.Node):
                    new_list.append(ranking_list[0])
                else:
                    for vis in ranking_list[0]:
                        new_list.append(vis)

        if len(ranking_list) > 1:
            if ranking_list[1] is not None and ranking_list[1] is not []:
                if isinstance(ranking_list[1], graph.Node):
                    new_list.append(ranking_list[1])
                else:
                    for neigh in ranking_list[1]:
                        new_list.append(neigh)

        if len(ranking_list) > 2:
            if ranking_list[2] is not None and ranking_list[2] is not []:
                if isinstance(ranking_list[2], graph.Node):
                    new_list.append(ranking_list[2])
                else:
                    for unvis in ranking_list[2]:
                        new_list.append(unvis)

        return new_list

    def matching(self, orig_node_list, target_node_list, parent_list=None):
        """
        Attempts to match nodes against target list.
        :return: List of node matches. Each match is a pair of (orig_node, matching_target_node)
        """
        # TODO: What are parent nodes ever used for?
        matched_nodes = []

        orig_node_list_copy = list(orig_node_list)

        # Iterate through nodes in orig node list.
        for orig_node in orig_node_list_copy:

            target_node_list_copy = list(target_node_list)

            # Iterate through nodes in target node list.
            for target_node in target_node_list_copy:

                match = True

                # Note: Modified from original algorithm.
                # Check edge count number first. Due to list ordering, if this fails, then all further comparisons in
                # target_list will also fail. Thus, break to move onto next node in orig_list.
                if len(target_node.edges_in) < len(orig_node.edges_in) or len(target_node.edges_out) < len(orig_node.edges_out):
                    match = False
                    # logger.info('Failed node edge count check.')

                # Check that "verticies are compatible". Aka, do the are the two nodes contain the same things.
                if match:
                    if not orig_node.name == target_node.name:
                        match = False
                        # logger.info('Failed node name check.')
                if match:
                    if not orig_node.identifier == target_node.identifier:
                        match = False
                        # logger.info('Failed node identifier check.')
                if match:
                    if not orig_node.data == target_node.data:
                        match = False
                        # logger.info('Failed node data check.')

                # Check that "constraints from topology of pattern graph to this point are met."
                # TODO: Basically, iterate through all edge connections and ensure that there is an identical node on
                # TODO: the other side for each graph.
                # TODO: Although, if checking for a subtree, broken/missing connections are to be expected. So is this necessary?

                # If it got this far, then is a valid match. Add to list of matches and remove target from list.
                # Then break current loop to start iterating through next node in "orig list", since current match was found.
                if match:
                    matched_nodes.append([orig_node, target_node])
                    target_node_list.remove(target_node)
                    break

                # Note: Modified from algorithm. Does not check if nodes were "already matched in current path."
                # If orig_node is already matched, then it will have been iterated, so it's irrelevant.
                # If target_node is matched, then it is removed from target_list so it won't be checked anymore.
                # Saves up to O(n * m) where n is the size of the original list and m is the size of the target list.

        return matched_nodes
