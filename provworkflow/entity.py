from typing import List, TYPE_CHECKING

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import DCAT, PROV, RDF, XSD

from .namespace import PROVWF
from .prov_reporter import ProvReporter
from .agent import Agent

# from .activity import Activity


class Entity(ProvReporter):
    """prov:Entity

    :param uri: A URI you assign to the ProvReporter instance. If None, a UUID-based URI will be created,
    defaults to None
    :type uri: Union[URIRef, str], optional

    :param label: A text label you assign, defaults to None
    :type label: str, optional

    :param named_graph_uri: A Named Graph URI you assign, defaults to None
    :type named_graph_uri: Union[URIRef, str], optional

    :param value: (prov:value) should be used to contain simple literal values when the Entity is entirely defined
        by that value.
    :type value: Literal, optional

    :param access_uri: (dcat:accessURL) should be used to contain links used to access the content of the Entity, e.g. a
        Google Cloud Services API call or an S2 Bucket link.
    :type access_uri: str, optional

    :param service_parameters: (provwf:serviceParameters) should be used to contain any parameters used for web
        services accessed via access_uri that are not contained within the URI itself.
    :type service_parameters: str, optional

    :param was_used_by: The inverse of prov:used: this indicates which Activities prov:used this Entity
    :type was_used_by: Activity, optional

    :param was_generated_by: Generation is the completion of production of a new entity by an activity. This entity
        did not exist before generation and becomes available for usage after this generation.
    :type was_generated_by: Activity, optional

    :param was_attributed_to: An Agent that this Entitiy is ascribed to (created by)
    :type was_attributed_to: Agent, optional

    :param was_revision_of: An Entity that this Entity is a revised version of. The implication here is that the
        resulting entity contains substantial content from the original. Revision is a particular case of derivation.
    :type was_revision_of: Entity, optional

    :param external: Whether or not this Entity exists outside the workflow
    :type external: bool, optional
    """

    def __init__(
        self,
        uri: URIRef = None,
        label: str = None,
        named_graph_uri: URIRef = None,
        value: str = None,
        access_uri: str = None,
        service_parameters: str = None,
        was_used_by=None,
        was_generated_by=None,
        was_attributed_to: Agent = None,
        was_revision_of=None,  # Entity
        external: bool = None,
    ):
        super().__init__(uri=uri, label=label, named_graph_uri=named_graph_uri)

        self.value = Literal(value) if value is not None else None
        self.access_uri = (
            Literal(access_uri, datatype=XSD.anyURI) if access_uri is not None else None
        )
        self.service_parameters = (
            Literal(service_parameters) if service_parameters is not None else None
        )
        if type(was_used_by) != list:
            self.was_used_by = [was_used_by]
        else:
            self.was_used_by = was_used_by
        if type(was_generated_by) != list:
            self.was_generated_by = [was_generated_by]
        else:
            self.was_used_by = was_used_by
        self.was_attributed_to = was_attributed_to
        self.was_revision_of = was_revision_of
        self.external = external

    def prov_to_graph(self, g: Graph = None) -> Graph:
        g = super().prov_to_graph(g)

        g.bind("dcat", DCAT)

        # add in type
        g.add((self.uri, RDF.type, PROV.Entity))

        if self.value is not None:
            g.add((self.uri, PROV.value, self.value))

        if self.access_uri is not None:
            g.add((self.uri, DCAT.accessURL, self.access_uri))

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

        if self.external:
            # this will be removed if present within a Workflow. The Workflow will create other necessary triples
            g.add((self.uri, PROV.wasAttributedTo, Literal("Workflow")))

        return g
