from rdflib import Graph, URIRef
from rdflib.namespace import RDF

from provworkflow import ProvReporter, ProvWorkflowException


class Workflow(ProvReporter):
    def __init__(self, uri_str=None, label=None, blocks=None, named_graph_uri=None):
        super().__init__(uri_str=uri_str, label=label, named_graph_uri=named_graph_uri)
        self.blocks = blocks
        if self.blocks is None:
            self.blocks = []

    def prov_to_graph(self, g=None):
        if self.blocks is None or len(self.blocks) < 1:
            raise ProvWorkflowException(
                "A Workflow must have at least one Block within it"
            )

        if g is None:
            if self.named_graph_uri is not None:
                g = Graph(identifier=URIRef(self.named_graph_uri))
            else:
                g = Graph()

        # add in type
        g.add((self.uri, RDF.type, self.PROVWF.Workflow))

        # add the prov graph of each block to this Workflow's prov graph
        for block in self.blocks:
            block.prov_to_graph(g)
            # associate this Block with this Workflow
            g.add((self.uri, self.PROVWF.hadBlock, block.uri))

        # build all the details for the Workflow itself
        g = super().prov_to_graph(g)

        return g
