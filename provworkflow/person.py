from typing import Union
from rdflib import Graph, URIRef
from rdflib.namespace import PROV, RDF, SDO

from .agent import Agent


class Person(Agent):
    """prov:Person

    :param uri: A URI you assign to the Person instance. If None, a UUID-based URI will be created,
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
        acted_on_behalf_of: Union[Agent, URIRef] = None,
        email: URIRef = None,
    ):
        self.email = email
        super().__init__(
            uri=uri,
            label=label,
            named_graph_uri=named_graph_uri,
            acted_on_behalf_of=acted_on_behalf_of,
        )

    def prov_to_graph(self, g: Graph = None) -> Graph:
        g = super().prov_to_graph(g)

        # add in type
        g.add((self.uri, RDF.type, PROV.Person))
        g.remove((self.uri, RDF.type, PROV.Agent))

        # special person properties
        if self.email is not None:
            g.add((self.uri, SDO.email, self.email))

        return g
