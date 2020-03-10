from .prov_reporter import ProvReporter
from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF


class Block(ProvReporter):

    def __init__(self, label=None):
        super().__init__(label=label)
        self.label = label

    def prov_to_graph(self, g=None):
        g = super().prov_to_graph(g)

        # add in type
        g.add((
            URIRef(self.uri),
            RDF.type,
            self.PROVWF.Block
        ))

        return g
