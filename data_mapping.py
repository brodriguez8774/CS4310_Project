"""
Maps graphs data to visual representation.
"""

# System Imports.
from matplotlib import pyplot
import networkx

# User Class Imports.
from resources import graph, logging
import algorithm as alg


# Initialize logging.
logger = logging.get_logger(__name__)


class DataMapping():
    """
    Data mapping class.
    """
    def __init__(self, graph_1, graph_2):
        self.nx_graph_1 = networkx.DiGraph()
        self.nx_graph_2 = networkx.DiGraph()
        self.nx_graph_1_position = None
        self.nx_graph_2_position = None
        self.backend_graph_1 = graph_1
        self.backend_graph_2 = graph_2

        self.initialize_graphs()

    def initialize_graphs(self):
        """
        Initializes visual graph object.
        """
        # Graph 1.
        # Add all nodes to graph.
        for key, value in self.backend_graph_1.nodes.items():
            node = self.backend_graph_1.get_node(key)
            self.nx_graph_1.add_node(
                node.identifier,
                attr_dict={
                    'node': node,
                }
            )

        # Establish edge connections between nodes.
        for key, value in self.backend_graph_1.nodes.items():
            for edge_link in value.edges_out:
                node = self.backend_graph_1.get_node(key)
                self.nx_graph_1.add_edge(
                    node.identifier,
                    edge_link.identifier,
                    attr_dict={
                        'node': node,
                    }
                )

        # Set position so graph nodes aren't randomly placed.
        self.nx_graph_1_position = networkx.spring_layout(self.nx_graph_1)

        # Graph 2.
        if self.backend_graph_2 is not None:
            # Add all nodes to graph.
            for key, value in self.backend_graph_2.nodes.items():
                node = self.backend_graph_2.get_node(key)
                self.nx_graph_2.add_node(
                    node.identifier,
                    attr_dict={
                        'node': node,
                    }
                )

            # Establish edge connections between nodes.
            for key, value in self.backend_graph_2.nodes.items():
                for edge_link in value.edges_out:
                    node = self.backend_graph_2.get_node(key)
                    self.nx_graph_2.add_edge(
                        node.identifier,
                        edge_link.identifier,
                        attr_dict={
                            'node': node,
                        }
                    )

            # Set position so graph nodes aren't randomly placed.
            self.nx_graph_2_position = networkx.spring_layout(self.nx_graph_2)
        else:
            self.nx_graph_2 = None

    #region Graph Initialization Methods

    def create_edge_count_color_mapping(self, nx_graph):
        """
        Creates a color mapping list (for drawing the provided graph).
        Index of each mapping should equate the the equivalent index in the graph.
        :return: Color mapping list of decimal values between 0 and 1.
        """
        value_map = []
        max_edges = 0

        # First find highest node edge count.
        for node_data in nx_graph.nodes().values():
            if node_data != {}:
                node_edge_count = len(node_data['attr_dict']['node'].edges_in) + len(node_data['attr_dict']['node'].edges_out)
                if max_edges == 0:
                    max_edges = node_edge_count
                elif max_edges < node_edge_count:
                    max_edges = node_edge_count

        # Double check that max_edges was properly set. If not, default to 10.
        # if max_edges <= 0:
        #     max_edges = 10

        # Iterate through nodes again and get actual mapping.
        for node_data in nx_graph.nodes().values():
            if node_data != {}:
                node_edge_count = len(node_data['attr_dict']['node'].edges_in) + len(node_data['attr_dict']['node'].edges_out)
                # while node_edge_count > 1:
                #     node_edge_count = (node_edge_count / max_edges)
                value_map.append(node_edge_count)

        return value_map

    def create_node_match_mapping(self):
        """
        Creates a color mapping list based off node matching.
        :return: Color mapping lists of integer values. 0 for miss or 1 for match.
        """
        # logger.info('Starting match color mapping.')
        value_map_1 = []
        for node in self.nx_graph_1.nodes():
            # logger.info(self.backend_graph_1.get_node(node).graph_match)

            if self.backend_graph_1.get_node(node).graph_match:
                value_map_1.append(1)
            else:
                value_map_1.append(0)

        value_map_2 = []
        for node in self.nx_graph_2.nodes():
            # logger.info(self.backend_graph_2.get_node(node).graph_match)

            if self.backend_graph_2.get_node(node).graph_match:
                value_map_2.append(1)
            else:
                value_map_2.append(0)

        return [value_map_1, value_map_2]


    def create_vis_labels(self, graph_number):
        """
        Creates vis/neigh/unvis labels for graph.
        :return: The created labels.
        """
        if graph_number == 1:
            nx_graph = self.nx_graph_1
            backend_graph = self.backend_graph_1
        elif graph_number == 2:
            nx_graph = self.nx_graph_2
            backend_graph = self.backend_graph_2
        else:
            return None

        algorithm = alg.Algorithm()
        node_ranking = algorithm.greatest_constraints_first(backend_graph.edge_count_list)

        # Set graph labels based off of associated ranking type.
        # Label all vis.
        if isinstance(node_ranking[0], graph.Node):
            nx_graph.nodes[node_ranking[0].identifier]['attr_dict']['node'].graph_label = 'vis'
        else:
            for visitor in node_ranking[0]:
                nx_graph.nodes[visitor.identifier]['attr_dict']['node'].graph_label = 'vis'

        # Label all neigh.
        try:
            if isinstance(node_ranking[1], graph.Node):
                nx_graph.nodes[node_ranking[1].identifier]['attr_dict']['node'].graph_label = 'neigh'
            else:
                for neighbor in node_ranking[1]:
                    nx_graph.nodes[neighbor.identifier]['attr_dict']['node'].graph_label = 'neigh'
        except IndexError:
            pass

        # Label all unvis.
        try:
            if isinstance(node_ranking[2], graph.Node):
                nx_graph.nodes[node_ranking[2].identifier]['attr_dict']['node'].graph_label = 'unvis'
            else:
                for unvisited in node_ranking[2]:
                    nx_graph.nodes[unvisited.identifier]['attr_dict']['node'].graph_label = 'unvis'
        except IndexError:
            pass

        # Actually set label dict based on data value.
        label_dict = {}
        backend_graph.edge_count_list[0].graph_label = 'root'
        for node in nx_graph.nodes().values():
            # logger.info('Node Value: {0}'.format(node))
            if node is not {}:
                label_dict[node['attr_dict']['node'].identifier] = node['attr_dict']['node'].graph_label

        return label_dict

    def create_match_labels(self, match_list):
        """
        Creates node match labels for graph.
        :return: The created labels and color mapping, in a [graph_1_labels, graph_2_labels] list.
        """
        # logger.info('Creating match labels.')
        index = 0
        label_set_1 = {}
        label_set_2 = {}
        graph_node_set_1 = list(self.backend_graph_1.nodes.values())
        graph_node_set_2 = list(self.backend_graph_2.nodes.values())

        # logger.info('Iterating matched pairs.')

        # Iterate through all match pairs. For each, split the pair and do the following:
        #   Add to the appropriate label set. Matching nodes should have identical labeling numbers.
        #   Set the associated backend node "graph_match" value to true. Used later for color_mapping.
        for match_pair in match_list:
            label_set_1[match_pair[0].identifier] = index
            self.backend_graph_1.nodes[match_pair[0].identifier].graph_match = True
            graph_node_set_1.remove(self.backend_graph_1.nodes[match_pair[0].identifier])

            label_set_2[match_pair[1].identifier] = index
            self.backend_graph_2.nodes[match_pair[1].identifier].graph_match = True
            graph_node_set_2.remove(self.backend_graph_2.nodes[match_pair[1].identifier])

            index += 1

        # logger.info('Iterating unmatched pairs.')

        # Iterate through all remaining nodes. These were non-matches.
        # Add arbitrary index labels starting from value the matches ended at.
        temp_index = index
        for node in graph_node_set_1:
            # label_set_1[node.identifier] = 'NM'
            label_set_1[node.identifier] = temp_index
            temp_index += 1

        temp_index = index
        for node in graph_node_set_2:
            # label_set_2[node.identifier] = 'NM'
            label_set_2[node.identifier] = temp_index
            temp_index += 1

        # logger.info('Match labels created.')

        return [label_set_1, label_set_2]


    def log_graph_info(self, graph_number):
        """
        Prints indicated graph info to console.
        """
        if graph_number == 1:
            graph = self.nx_graph_1
        elif graph_number == 2:
            graph = self.nx_graph_2
        else:
            return None

        logger.info(str(networkx.info(graph)))

    #endregion Graph Initialization Methods

    #region General Graph Mappings

    def draw_bw_map(self, graph_number, labels=None, value_map=None, vis_labels=False, vmin=0, vmax=1.2, show=False, key=False):
        """
        Draws single network map, in greyscale.
        """
        # Set up graph info or return on invalid graph number.
        if graph_number == 1:
            nx_graph = self.nx_graph_1
            graph_position = self.nx_graph_1_position
        elif graph_number == 2:
            nx_graph = self.nx_graph_2
            graph_position = self.nx_graph_2_position
        else:
            return None

        # Get labels.
        if labels is None:
            if vis_labels:
                label_dict = self.create_vis_labels(graph_number)
            else:
                label_dict = None
        else:
            label_dict = labels

        # Get value map.
        if value_map is None:
            value_map = self.create_edge_count_color_mapping(nx_graph)

        map_max = max(value_map)
        vmax = map_max * 1.1
        vmax = round(vmax)
        if vmax == map_max:
            vmax += 1

        # Create graph with new labels.
        networkx.draw_networkx_edges(
            nx_graph,
            graph_position,

            # Edge settings.
            edge_color='#303030',
            alpha=0.5,
            arrows=True,
            width=1.0,
            # width=2.0,
        )
        node_drawing = networkx.draw_networkx_nodes(
            nx_graph,
            graph_position,

            # Node settings.
            cmap=pyplot.get_cmap('gray'),
            # cmap=pyplot.get_cmap('RdGy'),
            node_color=value_map,
            node_size=1500,
            # node_size=3000,
            alpha=0.6,
            linewidths=4,

            vmin=vmin,
            vmax=vmax,
        )
        networkx.draw_networkx_labels(
            nx_graph,
            graph_position,

            # Font settings.
            with_labels=True,
            font_weight='bold',
            font_color='black',
            font_size=12,
            # font_size=24,
            labels=label_dict,
        )
        pyplot.axis('off')

        if key:
            # pyplot.subplot(123)
            pyplot.colorbar(node_drawing)

        if show:
            pyplot.show()

        return node_drawing

    def draw_color_map(self, graph_number, labels=None, value_map=None, vis_labels=False, vmin=0, vmax=1, show=False, key=False):
        """
        Draws single network map, in color.
        """
        # Set up graph info or return on invalid graph number.
        if graph_number == 1:
            nx_graph = self.nx_graph_1
            graph_position = self.nx_graph_1_position
        elif graph_number == 2:
            nx_graph = self.nx_graph_2
            graph_position = self.nx_graph_2_position
        else:
            return None

        # Get labels.
        if labels is None:
            if vis_labels:
                label_dict = self.create_vis_labels(graph_number)
            else:
                label_dict = None
        else:
            label_dict = labels

        # Get value map.
        if value_map is None:
            value_map = self.create_edge_count_color_mapping(nx_graph)

        map_max = max(value_map)
        vmax = map_max * 1.1
        vmax = round(vmax)
        if vmax == map_max:
            vmax += 1

        # Create graph with new labels.
        networkx.draw_networkx_edges(
            nx_graph,
            graph_position,

            # Edge settings.
            edge_color='#303030',
            alpha=0.5,
            arrows=True,
            width=1.0,
            # width=2.0,
        )
        node_drawing = networkx.draw_networkx_nodes(
            nx_graph,
            graph_position,

            # Node settings.
            cmap=pyplot.get_cmap('plasma'),
            node_color=value_map,
            node_size=1500,
            # node_size=3000,
            alpha=0.6,
            linewidths=2,

            vmin=vmin,
            vmax=vmax,
        )
        networkx.draw_networkx_labels(
            nx_graph,
            graph_position,

            # Font settings.
            with_labels=True,
            font_weight='bold',
            font_color='black',
            font_size=12,
            # font_size=24,
            labels=label_dict,
        )
        pyplot.axis('off')

        if key:
            # pyplot.subplot(123)
            pyplot.colorbar(node_drawing)

        if show:
            pyplot.show()

        return node_drawing

    def draw_side_by_side_bw_maps(self, vis_labels=False, key=False):
        """
        Draws network maps side by side, in greyscale.
        """
        # Create graph 1.
        pyplot.subplot(121)
        self.draw_bw_map(1, vis_labels=vis_labels)

        # Create graph 2.
        pyplot.subplot(122)
        node_drawing = self.draw_bw_map(2, vis_labels=vis_labels)

        # Show created graph(s).
        if key:
            pyplot.colorbar(node_drawing)
        pyplot.show()

    def draw_side_by_side_color_maps(self, vis_labels, key=False):
        """
        Draws network maps side by side, with color.
        """
        # Create graph 1.
        pyplot.subplot(121)
        self.draw_color_map(1, vis_labels=vis_labels)

        # Create graph 2.
        pyplot.subplot(122)
        node_drawing =  self.draw_color_map(2, vis_labels=vis_labels)

        # Show created graph(s).
        if key:
            pyplot.colorbar(node_drawing)
        pyplot.show()

    #endregion General Graph Mappings

    def draw_matching_comparison(self, match_list):
        """
        Draws network maps side by side, with color.
        """
        # logger.info('Graph 1 Info:')
        # self.log_graph_info(1)
        # logger.info('Graph 2 Info:')
        # self.log_graph_info(2)
        # logger.info('Drawing match comparison...')
        match_labels = self.create_match_labels(match_list)

        match_label_1 = match_labels[0]
        match_label_2 = match_labels[1]
        value_maps = self.create_node_match_mapping()
        value_map_1 = value_maps[0]
        value_map_2 = value_maps[1]

        # Create graph 1.
        # logger.info('Displaying graph 1.')
        pyplot.subplot(121)
        # logger.info(match_label_1)
        self.draw_color_map(1, labels=match_label_1, value_map=value_map_1, vmax=2)

        # Create graph 2.
        pyplot.subplot(122)
        self.draw_color_map(2, labels=match_label_2, value_map=value_map_2, vmax=2)

        # Show created graph(s).
        # pyplot.colorbar(node_drawing)
        pyplot.show()
