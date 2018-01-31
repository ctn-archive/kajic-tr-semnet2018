import networkx as nx
import numpy as np
import pickle


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class SemNet(dotdict):

    def __init__(self, source, directed=False):
        self.edges = self._load_database(source)
        self.directed = directed

        self.graph = self.create_graph(directed)
        self.degrees = np.array(list(dict(self.graph.degree()).values()))

        # populated by the analysis
        self.stats = dotdict()

    def _load_database(self, source):
        with open(source, 'rb+') as f:
            edges = pickle.load(f)

        return edges

    def create_graph(self, directed=False):
        g = nx.Graph()
        if directed:
            g = nx.DiGraph()

        if len(self.edges[0]) < 3:
            g.add_edges_from(self.edges)
        else:
            g.add_weighted_edges_from(self.edges)
        return g

    def do_analyses(self):

        if (nx.number_of_nodes(self.graph) == 0):
            print('Empty graph, skipping')

        if self.directed:        # directed graph
            f_conn_comp = nx.strongly_connected_component_subgraphs
            rnd = nx.DiGraph()
        else:
            f_conn_comp = nx.connected_component_subgraphs
            rnd = nx.Graph()

        self.stats.n_nodes = nx.number_of_nodes(self.graph)
        self.stats.n_edges = nx.number_of_edges(self.graph)
        avg_degree = nx.number_of_edges(self.graph) / \
            nx.number_of_nodes(self.graph)
        avg_degree = avg_degree if self.directed else 2*avg_degree
        self.stats.avg_degree = avg_degree
        self.stats.s = 100*avg_degree/self.stats.n_nodes

        # extract the largest connected component
        # and use in remaining analyses
        largest = max(f_conn_comp(self.graph), key=len)
        self.stats.connectedness = 100*largest.number_of_nodes() / \
            nx.number_of_nodes(self.graph)

        # clustering coefficient
        cc = nx.algorithms.average_clustering(largest.to_undirected())
        self.stats.cc = cc

        # avg shortest path length
        # note: diameter could be computed at the same time as aspl
        # but networkx does not support this
        aspl = nx.average_shortest_path_length(
                largest)
        self.stats.diameter = nx.diameter(largest)
        self.stats.aspl = aspl

        # calculate cc and aspl for a random ER graph with same edge
        # connectivity probability
        p = largest.number_of_edges()/(
                largest.number_of_nodes() * largest.number_of_nodes()-1)
        p = p if self.directed else 2*p  # multiply by 2 for undirected graph

        rnd = nx.random_graphs.erdos_renyi_graph(
                largest.number_of_nodes(), p, directed=self.directed)
        largest_rnd = max(f_conn_comp(rnd), key=len)

        rnd_aspl = nx.average_shortest_path_length(largest_rnd)
        rnd_cc = nx.algorithms.average_clustering(largest_rnd.to_undirected())
        self.stats.rnd_aspl = rnd_aspl
        self.stats.rnd_cc = rnd_cc
