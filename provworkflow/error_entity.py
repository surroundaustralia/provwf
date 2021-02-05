from .entity import Entity
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import PROV, RDF
from .prov_reporter import PROVWF


class ErrorEntity(Entity):
    """A prov:Entity specialised to communicate an error

    :param uri: A URI you assign to the Entity instance. If None, a UUID-based URI will be created,
    defaults to None
    :type uri: Union[URIRef, str], optional

    :param label: A text label you assign, defaults to ERROR
    :type label: str, optional

    :param named_graph_uri: A Named Graph URI you assign, defaults to None
    :type named_graph_uri: Union[URIRef, str], optional

    :param value: (prov:value) should be used to contain simple literal values when the Entity is entirely defined
        by that value.
    :type value: Literal, optional
    """

    def __init__(
        self,
        label: str = None,
        named_graph_uri: URIRef = None,
        value: str = None,
    ):
        super().__init__(label=label, named_graph_uri=named_graph_uri)

        self.label = Literal(label) if label is not None else "ERROR"
        self.value = Literal(value) if value is not None else "ERROR"

    def prov_to_graph(self, g: Graph = None) -> Graph:
        g = super().prov_to_graph(g)

        # add in type
        g.add((self.uri, RDF.type, PROVWF.ErrorEntity))
        g.remove((self.uri, RDF.type, PROV.Entity))

        return g
