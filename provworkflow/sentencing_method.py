from .block import Block
from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDFS, XSD


class SentencingMethod(Block):

    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def prov_to_graph(self, g=None):
        g = super().prov_to_graph(g)

        # add in type
        g.add((
            URIRef(self.uri),
            RDFS.type,
            self.PROVWF.Block
        ))

        return g
