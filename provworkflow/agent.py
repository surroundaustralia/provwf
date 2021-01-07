from typing import Union
from rdflib import Graph, URIRef
from rdflib.namespace import PROV, RDF

from .prov_reporter import ProvReporter, PROVWF


class Agent(ProvReporter):
    """prov:Agent

    :param uri: A URI you assign to the Agent instance. If None, a UUID-based URI will be created,
    defaults to None
    :type uri: Union[URIRef, str], optional

    :param label: A text label you assign, defaults to None
    :type label: str, optional

    :param named_graph_uri: A Named Graph URI you assign, defaults to None
    :type named_graph_uri: Union[URIRef, str], optional
    """

    def __init__(
        self,
        uri: URIRef = None,
        label: str = None,
        named_graph_uri: URIRef = None,
        acted_on_behalf_of: Union["Agent", URIRef] = None,
    ):
        # handle URIRef or Agent acted_on_behalf_of
        if acted_on_behalf_of is not None:
            if type(acted_on_behalf_of) == URIRef:
                self.acted_on_behalf_of = Agent(uri=self.acted_on_behalf_of)
            else:
                self.acted_on_behalf_of = acted_on_behalf_of
        super().__init__(uri=uri, label=label, named_graph_uri=named_graph_uri)

    def prov_to_graph(self, g: Graph = None) -> Graph:
        g = super().prov_to_graph(g)

        # add in type
        g.add((self.uri, RDF.type, PROV.Agent))
        g.remove((self.uri, RDF.type, PROVWF.ProvReporter))

        # special Agent properties
        if hasattr(self, "acted_on_behalf_of"):
            self.acted_on_behalf_of.prov_to_graph(g)
            g.add((self.uri, PROV.actedOnBehalfOf, self.acted_on_behalf_of.uri))

        return g
