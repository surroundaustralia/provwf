from rdflib import Graph, URIRef
from rdflib.namespace import PROV, RDF

from .prov_reporter import ProvReporter


class Agent(ProvReporter):
    """prov:Agent"""
    def __init__(
        self, uri: URIRef = None, label: str = None, named_graph_uri: URIRef = None,
    ):
        super().__init__(uri=uri, label=label, named_graph_uri=named_graph_uri)

    def prov_to_graph(self, g: Graph = None) -> Graph:
        g = super().prov_to_graph(g)

        # add in type
        g.add((self.uri, RDF.type, PROV.Agent))

        return g
