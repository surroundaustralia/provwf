from provworkflow import ProvReporter, ProvWorkflowException
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


if __name__ == '__main__':
    from os.path import dirname, join, abspath
    EXAMPLES_DIR = join(dirname(dirname(abspath(__file__))), 'examples')
    from provworkflow import Block
    w = Workflow()
    b1 = Block()
    w.blocks.append(b1)
    b2 = Block(uri="http://example.com/block/1")
    w.blocks.append(b2)
    b3 = Block()
    w.blocks.append(b3)
    g = w.prov_to_graph()

    # print(w.serialize(g))
    w.serialize(g, join(EXAMPLES_DIR, 'basic_workflow.ttl'))
