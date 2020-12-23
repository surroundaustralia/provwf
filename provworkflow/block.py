from typing import List

from rdflib import URIRef
from rdflib.namespace import RDF

from .activity import Activity
from .agent import Agent
from .entity import Entity
from .namespace import PROVWF


class Block(Activity):
    """A specialised type of prov:Activity that must live within a Workflow.

    For its Semantic Web definition, see https://data.surroundaustralia.com/def/provworkflow/Block (not available yet)
    """
    def __init__(
        self,
        uri: URIRef = None,
        label: str = None,
        named_graph_uri: URIRef = None,
        used: List[Entity] = None,
        generated: List[Entity] = None,
        was_associated_with: Agent = None,
    ):
        super().__init__(
            uri=uri,
            label=label,
            named_graph_uri=named_graph_uri,
            used=used,
            generated=generated,
            was_associated_with=was_associated_with,
        )

    def prov_to_graph(self, g=None):
        g = super().prov_to_graph(g)

        # add in type
        g.add((self.uri, RDF.type, PROVWF.Block))

        return g
