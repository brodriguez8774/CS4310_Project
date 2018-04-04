"""
Maps graphs data to visual representation.
"""

# System Imports.
# from plotly import plotly
# from plotly.graph_objs import *
import pylab
from matplotlib import pyplot

import networkx

# User Class Imports.
from resources import logging


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
            self.nx_graph_1.add_node(self.backend_graph_1.get_node(key))

        # Establish edge connections between nodes.
        for key, value in self.backend_graph_1.nodes.items():
            for link in value.edges_out:
                self.nx_graph_1.add_edge(self.backend_graph_1.get_node(key), link)

        # Set position so graph nodes aren't randomly placed.
        self.nx_graph_1_position = networkx.spring_layout(self.nx_graph_1)

        # Graph 2.
        if self.backend_graph_2 is not None:
            # Add all nodes to graph.
            for key, value in self.backend_graph_2.nodes.items():
                self.nx_graph_2.add_node(self.backend_graph_2.get_node(key))

            # Establish edge connections between nodes.
            for key, value in self.backend_graph_2.nodes.items():
                for link in value.edges_out:
                    self.nx_graph_2.add_edge(self.backend_graph_2.get_node(key), link)

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
        for node in nx_graph.nodes():
            node_edge_count = len(node.edges_in) + len(node.edges_out)
            if max_edges == 0:
                max_edges = node_edge_count
            elif max_edges < node_edge_count:
                max_edges = node_edge_count

        # Double check that max_edges was properly set. If not, default to 10.
        if max_edges <= 0:
            max_edges = 10

        # Iterate through nodes again and get actual mapping.
        for node in nx_graph.nodes():
            node_edge_count = len(node.edges_in) + len(node.edges_out)
            while node_edge_count > 1:
                node_edge_count = (node_edge_count / max_edges)
            value_map.append(node_edge_count)

        return value_map

    def draw_map(self):
        """
        Draws current network map.
        """
        value_map_1 = self.create_color_mapping(self.nx_graph_1)

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
            node_color=value_map_1,
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
        )
        pyplot.axis('off')

        # Attempt to create graph 2.
        if self.nx_graph_2 is not None:
            pyplot.subplot(122)
            value_map_2 = self.create_color_mapping(self.nx_graph_2)

            # Create graph 1.
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
                node_color=value_map_2,
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
            )
            pyplot.axis('off')

        # Show created graph(s).
        pyplot.colorbar(node_drawing)
        pyplot.show()
