"""
Maps graphs data to visual representation.
"""

# System Imports.
from matplotlib import pyplot
from matplotlib.axes import Axes
import networkx

# User Class Imports.
from resources import logging
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
            self.nx_graph_1.add_node(
                self.backend_graph_1.get_node(key).identifier,
                attr_dict={
                    'node': self.backend_graph_1.get_node(key),
                }
            )

        # Establish edge connections between nodes.
        for key, value in self.backend_graph_1.nodes.items():
            for edge_link in value.edges_out:
                self.nx_graph_1.add_edge(
                    self.backend_graph_1.get_node(key).identifier,
                    edge_link.identifier,
                    attr_dict={
                        'node': self.backend_graph_1.get_node(key),
                    }
                )

        # Set position so graph nodes aren't randomly placed.
        self.nx_graph_1_position = networkx.spring_layout(self.nx_graph_1)

        # Graph 2.
        if self.backend_graph_2 is not None:
            # Add all nodes to graph.
            for key, value in self.backend_graph_2.nodes.items():
                self.nx_graph_2.add_node(
                    self.backend_graph_2.get_node(key).identifier,
                    attr_dict={
                        'node': self.backend_graph_2.get_node(key),
                    }
                )

            # Establish edge connections between nodes.
            for key, value in self.backend_graph_2.nodes.items():
                for edge_link in value.edges_out:
                    self.nx_graph_2.add_edge(
                        self.backend_graph_2.get_node(key).identifier,
                        edge_link.identifier,
                        attr_dict={
                            'node': self.backend_graph_2.get_node(key),
                        }
                    )

            # Set position so graph nodes aren't randomly placed.
            self.nx_graph_2_position = networkx.spring_layout(self.nx_graph_2)
        else:
            self.nx_graph_2 = None

    def create_color_mapping(self, nx_graph):
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
        if max_edges <= 0:
            max_edges = 10

        # Iterate through nodes again and get actual mapping.
        for node_data in nx_graph.nodes().values():
            if node_data != {}:
                node_edge_count = len(node_data['attr_dict']['node'].edges_in) + len(node_data['attr_dict']['node'].edges_out)
                while node_edge_count > 1:
                    node_edge_count = (node_edge_count / max_edges)
                value_map.append(node_edge_count)

        return value_map

    def create_graph_labels(self, graph_number):
        """
        Creates labels for graph.
        :return:
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
        for visitor in node_ranking[0]:
            nx_graph.nodes[visitor.identifier]['attr_dict']['node'].data = 'vis'

        for neighbor in node_ranking[1]:
            nx_graph.nodes[neighbor.identifier]['attr_dict']['node'].data = 'neigh'

        for unvisited in node_ranking[2]:
            nx_graph.nodes[unvisited.identifier]['attr_dict']['node'].data = 'unvis'

        # Actually set label dict based on data value.
        label_dict = {}
        backend_graph.edge_count_list[0].data = 'root'
        for node in nx_graph.nodes().values():
            label_dict[node['attr_dict']['node'].identifier] = node['attr_dict']['node'].data

        return label_dict

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

    def draw_bw_map(self, graph_number, vis_labels):
        """
        Draws single network map, in greyscale.
        """
        if vis_labels:
            label_dict = self.create_graph_labels(graph_number)
        else:
            label_dict = None
        value_map = []
        if graph_number == 1:
            for node in self.nx_graph_2.nodes:
                value_map.append(1)
            nx_graph = self.nx_graph_1
            graph_position = self.nx_graph_1_position
        elif graph_number == 2:
            for node in self.nx_graph_2.nodes:
                value_map.append(1)
            nx_graph = self.nx_graph_2
            graph_position = self.nx_graph_2_position
        else:
            return None

        # Create graph with new labels.
        networkx.draw_networkx_edges(
            nx_graph,
            graph_position,

            # Edge settings.
            edge_color='black',
            alpha=0.5,
        )
        node_drawing = networkx.draw_networkx_nodes(
            nx_graph,
            graph_position,

            # Node settings.
            cmap=pyplot.get_cmap('gray'),
            node_color=value_map,
            node_size=1500,
            alpha=0.6,
            linewidths=2,
        )
        networkx.draw_networkx_labels(
            nx_graph,
            graph_position,

            # Font settings.
            with_labels=True,
            font_weight='bold',
            font_color='white',
            # font_size=24,
            labels=label_dict,
        )
        pyplot.axis('off')
        pyplot.show()

    def draw_color_map(self, graph_number, vis_labels):
        """
        Draws single network map, in color.
        """
        if vis_labels:
            label_dict = self.create_graph_labels(graph_number)
        else:
            label_dict = None
        if graph_number == 1:
            value_map = self.create_color_mapping(self.nx_graph_1)
            nx_graph = self.nx_graph_1
            graph_position = self.nx_graph_1_position
        elif graph_number == 2:
            value_map = self.create_color_mapping(self.nx_graph_2)
            nx_graph = self.nx_graph_2
            graph_position = self.nx_graph_2_position
        else:
            return None

        # Create graph with new labels.
        networkx.draw_networkx_nodes(
            nx_graph,
            graph_position,

            # Node settings.
            cmap=pyplot.get_cmap('plasma'),
            node_color=value_map,
            node_size=1500,
            alpha=0.6,
            linewidths=2,
        )
        networkx.draw_networkx_edges(
            nx_graph,
            graph_position,

            # Edge settings.
            edge_color='black',
            # width=5,
            alpha=0.5,
            arrows=True,
        )
        networkx.draw_networkx_labels(
            nx_graph,
            graph_position,

            # Font settings.
            with_labels=True,
            font_weight='bold',
            font_color='black',
            # font_size=24,
            labels=label_dict,
        )
        pyplot.axis('off')
        pyplot.show()

    def draw_side_by_side_bw_maps(self, vis_labels):
        """
        Draws network maps side by side, in greyscale.
        """
        if vis_labels:
            label_dict = self.create_graph_labels(1)
        else:
            label_dict = None
        value_map = []
        for node in self.nx_graph_1.nodes:
            value_map.append(1)

        # Create graph 1.
        pyplot.subplot(121)
        # Create graph 2.
        networkx.draw_networkx_edges(
            self.nx_graph_1,
            self.nx_graph_1_position,

            # Edge settings.
            edge_color='black',
            alpha=0.5,
        )
        node_drawing = networkx.draw_networkx_nodes(
            self.nx_graph_1,
            self.nx_graph_1_position,

            # Node settings.
            cmap=pyplot.get_cmap('gray'),
            node_color=value_map,
            node_size=1500,
            alpha=0.6,
            linewidths=2,
        )
        networkx.draw_networkx_labels(
            self.nx_graph_1,
            self.nx_graph_1_position,

            # Font settings.
            with_labels=True,
            font_weight='bold',
            font_color='black',
            labels=label_dict,
        )
        pyplot.axis('off')

        # Attempt to create graph 2.
        if self.nx_graph_2 is not None:
            pyplot.subplot(122)
            if vis_labels:
                label_dict = self.create_graph_labels(2)
            else:
                label_dict = None
            value_map = []
            for node in self.nx_graph_2.nodes:
                value_map.append(1)

            # Create graph 2.
            networkx.draw_networkx_edges(
                self.nx_graph_2,
                self.nx_graph_2_position,

                # Edge settings.
                edge_color='black',
                alpha=0.5,
            )
            networkx.draw_networkx_nodes(
                self.nx_graph_2,
                self.nx_graph_2_position,

                # Node settings.
                cmap=pyplot.get_cmap('gray'),
                node_color=value_map,
                node_size=1500,
                alpha=0.6,
                linewidths=2,
            )
            networkx.draw_networkx_labels(
                self.nx_graph_2,
                self.nx_graph_2_position,

                # Font settings.
                with_labels=True,
                font_weight='bold',
                font_color='black',
                labels=label_dict,
            )
            pyplot.axis('off')

        # logger.info('Graph 1 Info:')
        # logger.info(str(networkx.info(self.nx_graph_1)))
        #
        # if self.nx_graph_2 is not None:
        #     logger.info('Graph 2 Info:')
        #     logger.info(str(networkx.info(self.nx_graph_2)))

        # Show created graph(s).
        pyplot.colorbar(node_drawing)
        pyplot.show()

    def draw_side_by_side_color_maps(self, vis_labels):
        """
        Draws network maps side by side, with color.
        """
        if vis_labels:
            label_dict = self.create_graph_labels(1)
        else:
            label_dict = None
        value_map = self.create_color_mapping(self.nx_graph_1)

        # Create graph 1.
        if self.nx_graph_2 is not None:
            pyplot.subplot(121)
        networkx.draw_networkx_edges(
            self.nx_graph_1,
            self.nx_graph_1_position,

            # Edge settings.
            # edge_color='#606060',
            edge_color='black',
            alpha=0.5,
        )
        node_drawing = networkx.draw_networkx_nodes(
            self.nx_graph_1,
            self.nx_graph_1_position,

            # Node settings.
            cmap=pyplot.get_cmap('plasma'),
            node_color=value_map,
            node_size=1500,
            alpha=0.6,
            linewidths=2,

            vmin=0,
            vmax=0,
        )
        networkx.draw_networkx_labels(
            self.nx_graph_1,
            self.nx_graph_1_position,

            # Font settings.
            with_labels=True,
            font_weight='bold',
            font_color='black',
            labels=label_dict,
        )
        pyplot.axis('off')

        # Attempt to create graph 2.
        if self.nx_graph_2 is not None:
            pyplot.subplot(122)
            if vis_labels:
                label_dict = self.create_graph_labels(2)
            else:
                label_dict = None
            value_map = self.create_color_mapping(self.nx_graph_2)

            # Create graph 2.
            networkx.draw_networkx_edges(
                self.nx_graph_2,
                self.nx_graph_2_position,

                # Edge settings.
                edge_color='black',
                alpha=0.5,
            )
            networkx.draw_networkx_nodes(
                self.nx_graph_2,
                self.nx_graph_2_position,

                # Node settings.
                cmap=pyplot.get_cmap('plasma'),
                node_color=value_map,
                node_size=1500,
                alpha=0.6,
                linewidths=2,
            )
            networkx.draw_networkx_labels(
                self.nx_graph_2,
                self.nx_graph_2_position,

                # Font settings.
                with_labels=True,
                font_weight='bold',
                font_color='black',
                labels=label_dict,
            )
            pyplot.axis('off')

        # Show created graph(s).
        pyplot.colorbar(node_drawing)
        pyplot.show()
