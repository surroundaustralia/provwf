from rdflib import Graph, URIRef
from rdflib.namespace import PROV, RDF

from .prov_reporter import ProvReporter


class Agent(ProvReporter):
    """prov:Agent

    :param uri: A URI you assign to the ProvReporter instance. If None, a UUID-based URI will be created,
    defaults to None
    :type uri: Union[URIRef, str], optional

    :param label: A text label you assign, defaults to None
    :type label: str, optional

    :param named_graph_uri: A Named Graph URI you assign, defaults to None
    :type named_graph_uri: Union[URIRef, str], optional
    """
    def __init__(
        self, uri: URIRef = None,
            label: str = None,
            named_graph_uri: URIRef = None,
    ):
        super().__init__(uri=uri, label=label, named_graph_uri=named_graph_uri)

    def prov_to_graph(self, g: Graph = None) -> Graph:
        g = super().prov_to_graph(g)

        # add in type
        g.add((self.uri, RDF.type, PROV.Agent))

        return g
