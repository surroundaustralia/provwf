from __future__ import annotations
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import DCAT, PROV, RDF, XSD

from .namespace import PROVWF
from .prov_reporter import ProvReporter
from .agent import Agent

# from .activity import Activity


class Entity(ProvReporter):
    """prov:Entity

    :param uri: A URI you assign to the Entity instance. If None, a UUID-based URI will be created,
    defaults to None
    :type uri: Union[URIRef, str], optional

    :param label: A text label you assign, defaults to None
    :type label: str, optional

    :param named_graph_uri: A Named Graph URI you assign, defaults to None
    :type named_graph_uri: Union[URIRef, str], optional

    :param value: (prov:value) should be used to contain any Python object - str, fancy class, whatever - so data can
        be exchanged within the workflow. When reported to PROV, this variable is converted to a Literal

    :param was_used_by: The inverse of prov:used: this indicates which Activities prov:used this Entity
    :type was_used_by: Activity, optional

    :param was_generated_by: Generation is the completion of production of a new entity by an activity. This entity
        did not exist before generation and becomes available for usage after this generation.
    :type was_generated_by: Activity, optional

    :param was_attributed_to: An Agent that this Entity is ascribed to (created by)
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
        value=None,
        was_used_by=None,
        was_generated_by=None,
        was_attributed_to: Agent = None,
        was_revision_of: Entity = None,
        external: bool = None,
    ):
        super().__init__(uri=uri, label=label, named_graph_uri=named_graph_uri)

        self.value = value
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
        g.remove((self.uri, RDF.type, PROVWF.ProvReporter))

        if self.value is not None:
            g.add((self.uri, PROV.value, Literal(self.value)))

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

        if self.was_revision_of is not None:
            self.was_revision_of.prov_to_graph(g)
            g.add((self.uri, PROV.wasRevisionOf, self.was_revision_of.uri))

        if self.external:
            # this will be removed if present within a Workflow. The Workflow will create other necessary triples
            g.add((self.uri, PROV.wasAttributedTo, Literal("Workflow")))

        return g
