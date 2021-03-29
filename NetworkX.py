import networkx as nx
import matplotlib.pyplot as plt
import numpy
import parse as prs
import parse_request as prs_rq

from bokeh.io import output_file, show
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                        MultiLine, Plot, Range1d, WheelZoomTool, PanTool, )
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx

# https://oauth.vk.com/authorize?client_id=7651557&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,groups&response_type=token&v=5.65

class NGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def make_graph(self, groups_out):
        for i_group in range(len(groups_out)):
            self.graph.add_node(groups_out[i_group][0], size=groups_out[i_group][1]['count'])
            for k_group in range(i_group+1, len(groups_out)):
                intersection = set(groups_out[i_group][1]['users']).intersection(set(groups_out[k_group][1]['users']))
                if len(intersection) > 0:
                    self.graph.add_edge(groups_out[i_group][0],
                    groups_out[k_group][0], weight=len(intersection)**2)

    def plot_graph(self, adjust_nodesize):
        pos = nx.spring_layout(self.graph)

        nodesize = [self.graph.nodes[i]['size']/adjust_nodesize for i in self.graph.nodes()]

        edge_mean = numpy.mean([self.graph.edges[(i[0], i[1])]['weight'] for i in self.graph.edges()])
        edge_std_dev = numpy.std([self.graph.edges[(i[0], i[1])]['weight'] for i in self.graph.edges()])
        edgewidth = [((self.graph.edges[(i[0], i[1])]['weight'] - edge_mean)/edge_std_dev) for i in self.graph.edges()]

        nx.draw_networkx_nodes(self.graph, pos,node_size=nodesize, node_color='r', alpha=0.6)
        nx.draw_networkx_edges(self.graph, pos,width=edgewidth,edge_color='b')
        nx.draw_networkx_labels(self.graph, pos)

        plt.savefig('figure.jpg')
        plt.show()

    def bohek_plot_graph(self, adjust_nodesize):
        pos = nx.spring_layout(self.graph)

        



        nodesize = [self.graph.nodes[i]['size']/adjust_nodesize for i in self.graph.nodes()]

        edge_mean = numpy.mean([self.graph.edges[(i[0], i[1])]['weight'] for i in self.graph.edges()])
        edge_std_dev = numpy.std([self.graph.edges[(i[0], i[1])]['weight'] for i in self.graph.edges()])
        edgewidth = [((self.graph.edges[(i[0], i[1])]['weight'] + edge_mean)/edge_std_dev) for i in self.graph.edges()]

        adjusted_node_size = dict([(node[0], nsize) for node, nsize in zip(nx.degree(self.graph), nodesize)])
        nx.set_node_attributes(self.graph, name='adjusted_node_size', values=adjusted_node_size)

        adjusted_edge_size = dict([((i[0], i[1]), j)  for i, j in zip(self.graph.edges(), edgewidth)])
        nx.set_edge_attributes(self.graph, name='adjusted_edge_size', values=adjusted_edge_size)



        plot = Plot(plot_width=800, plot_height=800,
                    x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1), toolbar_location="below")
                    
        plot.title.text = "Graph Interaction Demonstration"

        node_hover_tool = HoverTool(tooltips=[("index", "@index"), ("size", "@size")])
        plot.add_tools(node_hover_tool, PanTool(), WheelZoomTool())
        plot.toolbar.active_scroll = plot.select_one(WheelZoomTool)

        graph_renderer = from_networkx(self.graph, pos, scale=1, center=(0, 0))

        graph_renderer.node_renderer.glyph = Circle(size='adjusted_node_size', fill_color=Spectral4[0])
        graph_renderer.edge_renderer.glyph = MultiLine(line_alpha=0.8, line_width='adjusted_edge_size')
        plot.renderers.append(graph_renderer)

        output_file("interactive_graphs.html")
        show(plot)

if __name__ == '__main__':

    token = '8bbb4daf8bbb4daf8bbb4daf0c8bcf8d4a88bbb8bbb4dafebb491b8847b23c3736b59f0'
    parser = prs_rq.parse_request(token)

    user_list = ['nurboliskakov', 'moldir07', 177618094, 351711814, 242804539, 282323139, 208549, 'muhin', 235476811, 'idzh0ni', 236879826, 'abdream']

    ngraph = NGraph()
    ngraph.make_graph(parser.get_users(user_list))
    ngraph.bohek_plot_graph(10)