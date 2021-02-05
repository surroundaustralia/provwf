from __future__ import annotations
from datetime import datetime
from typing import List, Union

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import PROV, RDF, XSD

# from franz.openrdf.connect import ag_connect
# from franz.openrdf.rio.rdfformat import RDFFormat
from .prov_reporter import ProvReporter, PROVWF
from .entity import Entity
from .agent import Agent


class Activity(ProvReporter):
    """prov:Activity

    :param uri: A URI you assign to the Activity instance. If None, a UUID-based URI will be created,
    defaults to None
    :type uri: Union[URIRef, str], optional

    :param label: A text label you assign, defaults to None
    :type label: str, optional

    :param named_graph_uri: A Named Graph URI you assign
    :type named_graph_uri: Union[URIRef, str], optional

    :param used: A list of Entities used (prov:used) by this Block
    :type used: List[Block], optional

    :param generated: A list of Entities used (prov:generated) by this Block
    :type generated: List[Block], optional

    :param was_associated_with: An Agent that ran this Block (prov:wasAssociatedWith), may or may not be the same as
        the one associated with the Workflow
    :type was_associated_with: Agent, optional

    :param informed: Another Activity that this Activity triggered the creation of
    :type informed: Activity, optional

    :param was_informed_by: Another Activity that triggered the creation of this Activity
    :type was_informed_by: Activity, optional
    """

    def __init__(
        self,
        uri: URIRef = None,
        label: str = None,
        named_graph_uri: URIRef = None,
        used: List[Entity] = None,
        generated: List[Entity] = None,
        was_associated_with: Agent = None,
        informed: List[Activity] = None,
        class_uri: Union[URIRef, str] = None,
    ):
        super().__init__(
            uri=uri, label=label, named_graph_uri=named_graph_uri, class_uri=class_uri
        )

        self.started_at_time = datetime.now()
        self.ended_at_time = None

        self.used = used if used is not None else []
        self.generated = generated if generated is not None else []
        self.was_associated_with = was_associated_with
        self.informed = informed if informed is not None else []

    def prov_to_graph(self, g: Graph = None) -> Graph:
        g = super().prov_to_graph(g)

        # add in type
        g.add((self.uri, RDF.type, PROV.Activity))
        g.remove((self.uri, RDF.type, PROVWF.ProvReporter))

        # all Activities have a startedAtTime
        # made at __init__() time
        g.add(
            (
                self.uri,
                PROV.startedAtTime,
                Literal(
                    datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z"),
                    datatype=XSD.dateTimeStamp,
                ),
            )
        )

        if self.used is not None:
            for e in self.used:
                e.prov_to_graph(g)
                g.add((self.uri, PROV.used, e.uri))

        if self.generated is not None:
            for e in self.generated:
                e.prov_to_graph(g)
                g.add((self.uri, PROV.generated, e.uri))

        if self.was_associated_with is not None:
            self.was_associated_with.prov_to_graph(g)
            g.add((self.uri, PROV.wasAssociatedWith, self.was_associated_with.uri))

        if self.informed is not None:
            for i in self.informed:
                i.prov_to_graph(g)
                # g.add((self.uri, PROV.informed, i.uri))
                g.add((i.uri, PROV.wasInformedBy, self.uri))

        # if we don't yet have an endedAtTime recorded, make it now
        if self.ended_at_time is None:
            self.ended_at_time = datetime.now()

        # all Activities have a endedAtTime
        g.add(
            (
                self.uri,
                PROV.endedAtTime,
                Literal(
                    datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z"),
                    datatype=XSD.dateTimeStamp,
                ),
            )
        )

        return g
