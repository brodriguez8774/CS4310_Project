"""
Maps graphs data to visual representation.
"""

# System Imports.
# from plotly import plotly
# from plotly.graph_objs import *
from matplotlib import pyplot

import networkx

# User Class Imports.
from resources import logging


# Initialize logging.
logger = logging.get_logger(__name__)


class DataMap():
    """
    Data mapping class.
    """
    def __init__(self, graph):
        self.nx_graph = networkx.DiGraph()
        self.backend_graph = graph

        self.initialize_graph()

    def initialize_graph(self):
        """
        Initializes visual graph object.
        """
        # Add all nodes to graph.
        for key, value in self.backend_graph.nodes.items():
            self.nx_graph.add_node(self.backend_graph.get_node(key))

        # Establish edge connections between nodes.
        for key, value in self.backend_graph.nodes.items():
            for link in value.edges_out:
                self.nx_graph.add_edge(self.backend_graph.get_node(key), link)

    def draw_map(self):
        """
        Draws current network map.
        """
        pyplot.subplot(121)
        networkx.draw(self.nx_graph, with_labels=True, font_weight='bold')
        # pyplot.subplot(122)
        # networkx.draw_shell(test_graph, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
        pyplot.show()
