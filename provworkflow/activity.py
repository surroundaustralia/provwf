from datetime import datetime
from typing import List

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import PROV, RDF, XSD

# from franz.openrdf.connect import ag_connect
# from franz.openrdf.rio.rdfformat import RDFFormat
from .prov_reporter import ProvReporter, ProvReporterException
from .entity import Entity
from .agent import Agent


class Activity(ProvReporter):
    """prov:Activity

    was_associated_with: prov:wasAssociatedWith
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
        super().__init__(uri=uri, label=label, named_graph_uri=named_graph_uri)

        self.started_at_time = datetime.now()
        self.ended_at_time = None

        self.used = used if used is not None else []
        self.generated = generated if generated is not None else []
        self.was_associated_with = was_associated_with

    def prov_to_graph(self, g: Graph = None) -> Graph:
        g = super().prov_to_graph(g)

        # add in type
        g.add((self.uri, RDF.type, PROV.Activity))

        # all Activities have a startedAtTime
        # made at __init__() time
        g.add(
            (
                self.uri,
                PROV.startedAtTime,
                Literal(self.started_at_time.isoformat(), datatype=XSD.dateTime),
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

        # if we don't yet have an endedAtTime recorded, make it now
        if self.ended_at_time is None:
            self.ended_at_time = datetime.now()

        # all Activities have a endedAtTime
        g.add(
            (
                self.uri,
                PROV.endedAtTime,
                Literal(self.ended_at_time.isoformat(), datatype=XSD.dateTime),
            )
        )

        return g


class ActivityException(ProvReporterException):
    pass
