from typing import List

from rdflib import URIRef, Graph
from rdflib.namespace import RDF

from .prov_reporter import PROVWF
from .activity import Activity
from .agent import Agent


class Workflow(Activity):
    """A Workflow is a specialised Activity that contains 1+ Blocks (also specialised Activity instances).

    You cannot set the _used_ or _generated_ properties of a Workflow as you can for other Activities as these are
    calculated automatically, based on the _used_ & _generated_ properties of the Blocks the Workflow contains.

    You can either set the (list of) the Workflow's Blocks at creation time or afterwards. The order is unimportant as
    Block ordering is understood using Blocks' startedAtTime property.
    """

    def __init__(
        self,
        uri: URIRef = None,
        label: str = None,
        named_graph_uri: URIRef = None,
        was_associated_with: Agent = None,
        blocks: List[Block] = None,
    ):
        super().__init__(
            uri=uri,
            label=label,
            named_graph_uri=named_graph_uri,
            was_associated_with=was_associated_with,
        )
        self.blocks = blocks
        if self.blocks is None:
            self.blocks = []

    def prov_to_graph(self, g=None):
        if self.blocks is None or len(self.blocks) < 1:
            raise WorkflowException("A Workflow must have at least one Block within it")

        if g is None:
            if self.named_graph_uri is not None:
                g = Graph(identifier=URIRef(self.named_graph_uri))
            else:
                g = Graph()

        # add in type
        g.add((self.uri, RDF.type, PROVWF.Workflow))

        # add the prov graph of each block to this Workflow's prov graph
        for block in self.blocks:
            block.prov_to_graph(g)
            # associate this Block with this Workflow
            g.add((self.uri, self.PROVWF.hadBlock, block.uri))

        # build all the details for the Workflow itself
        g = super().prov_to_graph(g)

        return g


class WorkflowException(Exception):
    pass
