from typing import List

from rdflib import Graph, URIRef
from rdflib.namespace import PROV, RDF

from .prov_reporter import ProvReporter
from .agent import Agent


class Entity(ProvReporter):
    def __init__(
        self,
        uri: URIRef = None,
        label: str = None,
        named_graph_uri: URIRef = None,
        was_used_by=None,
        was_generated_by=None,
        was_attributed_to: Agent = None,
    ):
        super().__init__(uri=uri, label=label, named_graph_uri=named_graph_uri)

        if type(was_used_by) != []:
            self.was_used_by = [was_used_by]
        else:
            self.was_used_by = was_used_by
        if type(was_generated_by) != []:
            self.was_generated_by = [was_generated_by]
        else:
            self.was_used_by = was_used_by
        self.was_attributed_to = was_attributed_to

    def prov_to_graph(self, g: Graph = None) -> Graph:
        """Reports self (instance properties and class type) to an in-memory graph using PROV-O

        :param g: rdflib Graph. If given, this function will add its contents to g. If not, it will create new
        :return: rdflib Graph
        """
        g = super().prov_to_graph(g)

        # add in type
        g.add((self.uri, RDF.type, PROV.Entity))

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

            g.add((self.was_attributed_to.uri, PROV.generated, self.uri))

        return g
