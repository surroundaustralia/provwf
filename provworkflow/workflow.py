from .prov_reporter import ProvReporter
from rdflib.namespace import RDF


class Workflow(ProvReporter):

    def __init__(self, uri=None, label=None, blocks=None):
        super().__init__(uri=uri, label=label)
        self.blocks = blocks
        if self.blocks is None:
            self.blocks = []

    def prov_to_graph(self, g=None):
        if self.blocks is None or len(self.blocks) < 1:
            raise ProvWorkflowException("A Workflow must have at least one Block within it")

        g = super().prov_to_graph(g)

        # add in type
        g.add((
            self.uri,
            RDF.type,
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


class ProvWorkflowException(Exception):
    pass
