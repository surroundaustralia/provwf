from .prov_reporter import ProvReporter
from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDFS, XSD


class Workflow(ProvReporter):

    def __init__(self, name, blocks=None):
        super().__init__()
        self.name = name
        self.blocks = blocks

    def prov_to_graph(self, g=None):
        g = super().prov_to_graph(g)

        # add in type
        g.add((
            self.uri,
            RDFS.type,
            self.PROVWF.Workflow
        ))

        # add the prov graph of each block to this Workflow's prov graph
        for block in self.blocks:
            block.prov_to_graph(g)
            # associate this Block with this Workflow
            g.add((
                self.uri,
                self.PROVWF.hadBlock,
                block.uri
            ))

        return g
