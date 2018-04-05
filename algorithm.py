"""
Attempt at Isomorphism algorithm.
"""

# User Class Imports.
from resources import logging


# Initialize logging.
logger = logging.get_logger(__name__)


class Algorithm():
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

        iterated_nodes = []
        iterated_nodes.append(node_list_by_edge_count[0])

        copy_list = list(node_list_by_edge_count)
        copy_list.pop(0)
        node_list_by_edge_count[0].rank = [[],[],[]]

        vis_list = []
        neig_list = []
        unv_list = []

        # Iterate through all remaining nodes and get score values.
        for current_node in copy_list:

            relationship_determined = False

            # vis_list = []
            # neig_list = []
            # unv_list = []

            # Iterate through all of node's connections in.
            for edge_in in current_node.edges_in:

                # Check that relationship has not been determined.
                if relationship_determined:
                    break

                # Iterate through all elements in iterated_nodes list.
                for iterated_node in iterated_nodes:

                    # Check that relationship has not been determined.
                    if relationship_determined:
                        break

                    # Check if edge and iterated the same. If so, append current to vis_list and skip other checks.
                    if edge_in == iterated_node:
                        vis_list.append(current_node)
                        relationship_determined = True
                        break
                    else:
                        # Check if edge has connection to iterated. If so, append current to neig_list and skip other checks.

                        # Iterate through all neighbor edges in.
                        for neigh_edge in edge_in.edges_in:
                            if neigh_edge == iterated_node:
                                neig_list.append(current_node)
                                relationship_determined = True
                                break
                        # Iterate through all neighbor edges out.
                        for neigh_edge in edge_in.edges_out:
                            if neigh_edge == iterated_node:
                                neig_list.append(current_node)
                                relationship_determined = True
                                break

            # Iterate through all of node's connections out.
            for edge_out in current_node.edges_out:

                # Check that relationship has not been determined.
                if relationship_determined:
                    break

                # Iterate through all elements in iterated_nodes list.
                for iterated_node in iterated_nodes:

                    # Check that relationship has not been determined.
                    if relationship_determined:
                        break

                    # Check if edge and iterated the same. If so, append current to vis_list and skip other checks.
                    if edge_out == iterated_node:
                        vis_list.append(current_node)
                        relationship_determined = True
                        break
                    else:
                        # Check if edge has connection to iterated. If so, append current to neig_list and skip other checks.

                        # Iterate through all neighbor edges in.
                        for neigh_edge in edge_out.edges_in:
                            if neigh_edge == iterated_node:
                                neig_list.append(current_node)
                                relationship_determined = True
                                break
                        # Iterate through all neighbor edges out.
                        for neigh_edge in edge_out.edges_out:
                            if neigh_edge == iterated_node:
                                neig_list.append(current_node)
                                relationship_determined = True
                                break

            # Did not meet criteria for above checks. Append to "unvisited" list.
            if not relationship_determined:
                unv_list.append(current_node)

            iterated_nodes.append(current_node)

            logger.info('Node: {0}'.format(current_node))
            logger.info('vis_list: {0}'.format(vis_list))
            logger.info('neig_list: {0}'.format(neig_list))
            logger.info('unv_list: {0}'.format(unv_list))
            ranking = [vis_list, neig_list, unv_list]
            # logger.info('Rank: {0}'.format(current_node.rank))

            # Get parent of current node. Defined as node with smallest "index" and valid connection to current node.
            # TODO: Is "index" defined as index in edge_count list, or index of overall graph?? Does it even matter?
            current_node.parent = current_node.edges_in[0]  # First node should have the lowest respective index.

        # Return original nodelist. Each node should now have the associated data as determined by this algorithm.
        return ranking

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
