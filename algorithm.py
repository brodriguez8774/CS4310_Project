"""
Attempt at Isomorphism algorithm.
"""

# User Class Imports.
from resources import logging


# Initialize logging.
logger = logging.get_logger(__name__)


class Algorithm():
    def __init__(self):
        self.vis_list = None
        self.neigh_list = None
        self.unv_list = None
        self.iterated_nodes = None

    """
    Attempt at Isomorhpism algorithm.
    """
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
        self.neig_list = []
        self.unv_list = []
        ranking = None

        # Iterate through all remaining nodes and get score values.
        for current_node in copy_list:

            relationship_determined = False

            if not relationship_determined:
                relationship_determined = self.check_constraints_vis(current_node)

            if not relationship_determined:
                relationship_determined = self.check_constraints_neigh(current_node)

            # Did not meet criteria for above checks. Append to "unvisited" list.
            if not relationship_determined:
                self.unv_list.append(current_node)

            # self.iterated_nodes.append(current_node)

            # logger.info('Node: {0}'.format(current_node))
            # logger.info('vis_list: {0}'.format(self.vis_list))
            # logger.info('neig_list: {0}'.format(self.neig_list))
            # logger.info('unv_list: {0}'.format(self.unv_list))
            ranking = [self.vis_list, self.neig_list, self.unv_list]
            # logger.info('Rank: {0}'.format(current_node.rank))

            # Get parent of current node. Defined as node with smallest "index" and valid connection to current node.
            # TODO: Is "index" defined as index in edge_count list, or index of overall graph?? Does it even matter?
            if current_node.edges_in is not None and current_node.edges_in != []:
                current_node.parent = current_node.edges_in[0]  # First node should have the lowest respective index.

        # Return node rank list.
        return ranking

    def check_constraints_vis(self, current_node):
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

            # Look through all outward edges.
            for edge in current_node.edges_out:
                # Check if edge and iterated the same. If so, append current to vis_list and skip other checks.
                if edge == iterated_node:
                    self.vis_list.append(current_node)
                    relationship_determined = True
                    break

        return relationship_determined


    def check_constraints_neigh(self, current_node):
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
                        self.neig_list.append(current_node)
                        relationship_determined = True
                        break
                # Iterate through all neighbor edges out.
                for neigh_edge in edge.edges_out:
                    if neigh_edge == iterated_node:
                        self.neig_list.append(current_node)
                        relationship_determined = True
                        break

            # Look through all outward edges.
            for edge in current_node.edges_out:
                # Iterate through all neighbor edges in.
                for neigh_edge in edge.edges_in:
                    if neigh_edge == iterated_node:
                        self.neig_list.append(current_node)
                        relationship_determined = True
                        break
                # Iterate through all neighbor edges out.
                for neigh_edge in edge.edges_out:
                    if neigh_edge == iterated_node:
                        self.neig_list.append(current_node)
                        relationship_determined = True
                        break

        return relationship_determined

    def Matching(self, orig_node_list, parent_list, target_list):
        """
        Attempts to match nodes against target list.
        :return: List of node matches. Each match is a pair of (orig_node, matching_target_node)
        """
        # TODO: What are parent nodes ever used for?
        matched_nodes = []

        copy_list = list(orig_node_list)

        # Iterate through nodes in orig node list.
        for orig_node in copy_list:

            # Iterate through nodes in target node list.
            for target_node in target_list:

                # Note: Modified from original algorithm.
                # Check edge count number first. Due to list ordering, if this fails, then all further comparisons in
                # target_list will also fail. Thus, break to move onto next node in orig_list.
                if len(target_node.edges_in) < len(orig_node.edges_in) or len(target_node.edges_out) < len(orig_node.edges_out):
                    break

                # Check that "verticies are compatible".
                # TODO: Not sure what to do here. Does this just mean "check if nodes are identical"?

                # Check that "constraints from topology of pattern graph to this point are met."
                # TODO: Not sure what to do here. Again, does it mean "check if nodes are identical"...?

                # If it got this far, then is a valid match. Add to list of matches.
                matched_nodes.append([orig_node, target_node])

                # Note: Modified from algorithm. Does not check if nodes were "already matched in current path."
                # If orig_node is already matched, then it will have been iterated, so it's irrelevant.
                # If target_node is matched, then it is removed from target_list so it won't be checked anymore.
                # Saves up to O(n) where n is the size of the target list.

        return matched_nodes
