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

        # Graph 2.
        if self.backend_graph_2 is not None:
            # Add all nodes to graph.
            for key, value in self.backend_graph_2.nodes.items():
                self.nx_graph_2.add_node(self.backend_graph_2.get_node(key))

            # Establish edge connections between nodes.
            for key, value in self.backend_graph_2.nodes.items():
                for link in value.edges_out:
                    self.nx_graph_2.add_edge(self.backend_graph_2.get_node(key), link)
        else:
            self.nx_graph_2 = None

    def draw_map(self):
        """
        Draws current network map.
        """
        pyplot.subplot(121)
        networkx.draw(self.nx_graph_1, with_labels=True, font_weight='bold')
        if self.nx_graph_2 is not None:
            pyplot.subplot(122)
            networkx.draw_spring(self.nx_graph_2, with_labels=True, font_weight='bold')
        # networkx.draw_shell(test_graph, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
        pyplot.show()
