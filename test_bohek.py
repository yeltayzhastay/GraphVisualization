import networkx as nx

from bokeh.io import output_file, show
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool,WheelZoomTool, PanTool, )
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx

import numpy as np

graph = nx.path_graph(5)

pos = nx.spring_layout(graph)

SAME_CLUB_COLOR, DIFFERENT_CLUB_COLOR = "black", "white"
edge_attrs = {}

for start_node, end_node, _ in graph.edges(data=True):
    edge_color = SAME_CLUB_COLOR if graph.nodes[start_node] == graph.nodes[end_node] else DIFFERENT_CLUB_COLOR
    edge_attrs[(start_node, end_node)] = edge_color

nx.set_edge_attributes(graph, edge_attrs, "edge_color")

# Show with Bokeh
plot = Plot(plot_width=800, plot_height=800,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
plot.title.text = "Graph Interaction Demonstration"

node_hover_tool = HoverTool(tooltips=[("index", "@index"), ("club", "@club")])
plot.add_tools(node_hover_tool, WheelZoomTool(), ResetTool(), PanTool())

graph_renderer = from_networkx(graph, pos, scale=1, center=(0, 0))

graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
graph_renderer.edge_renderer.glyph = MultiLine(line_alpha=0.8, line_width=1)
plot.renderers.append(graph_renderer)

output_file("interactive_graphs.html")
show(plot)