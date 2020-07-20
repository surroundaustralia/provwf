from .prov_reporter import ProvReporter
from rdflib.namespace import RDF


class Block(ProvReporter):
    def __init__(self, uri_str=None, label=None):
        super().__init__(uri_str=uri_str, label=label)

    def prov_to_graph(self, g=None):
        g = super().prov_to_graph(g)

        # add in type
        g.add((self.uri, RDF.type, self.PROVWF.Block))

        return g
