from typing import List, TYPE_CHECKING

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import DCAT, PROV, RDF, XSD

from .namespace import PROVWF
from .prov_reporter import ProvReporter
from .agent import Agent
# from .activity import Activity


class Entity(ProvReporter):
    """prov:Entity

    property: (prov:value) should be used to contain simple literal values.

    access_uri: (dcat:accessURL) should be used to contain links used to access the content of the Entity, e.g. a
                Google Cloud Services API call or an S2 Bucket link.

    service_parameters: (provwf:serviceParameters) should be used to contain any parameters used for web services
                        accessed via access_uri that are not contained within the URI itself.
    """
    def __init__(
        self,
        uri: URIRef = None,
        label: str = None,
        value: str = None,
        access_uri: str = None,
        service_parameters: str = None,
        named_graph_uri: URIRef = None,
        was_used_by=None,
        was_generated_by=None,
        was_attributed_to: Agent = None,
    ):
        super().__init__(uri=uri, label=label, named_graph_uri=named_graph_uri)

        self.value = Literal(value) if value is not None else None
        self.access_uri = Literal(access_uri, datatype=XSD.anyURI) if access_uri is not None else None
        self.service_parameters = Literal(service_parameters) if service_parameters is not None else None
        if type(was_used_by) != list:
            self.was_used_by = [was_used_by]
        else:
            self.was_used_by = was_used_by
        if type(was_generated_by) != list:
            self.was_generated_by = [was_generated_by]
        else:
            self.was_used_by = was_used_by
        self.was_attributed_to = was_attributed_to

    def prov_to_graph(self, g: Graph = None) -> Graph:
        g = super().prov_to_graph(g)

        g.bind("dcat", DCAT)

        # add in type
        g.add((self.uri, RDF.type, PROV.Entity))

        if self.value is not None:
            g.add((self.uri, PROV.value, self.value))

        if self.access_uri is not None:
            g.add((self.uri, DCAT.accesURL, self.access_uri))

        if self.service_parameters is not None:
            g.add((self.uri, PROVWF.serviceParameters, self.service_parameters))

        if all(self.was_used_by):
            for a in self.was_used_by:
                a.prov_to_graph(g)

                g.add((a.uri, PROV.used, self.uri))

        if all(self.was_generated_by):
            for a in self.was_generated_by:
                a.prov_to_graph(g)

                g.add((a.uri, PROV.generated, self.uri))

        if self.was_attributed_to is not None:
            self.was_attributed_to.prov_to_graph(g)

            g.add((self.uri, PROV.wasAttributedTo, self.was_attributed_to.uri))

        return g
