from provworkflow import ProvWorkflowException
from provworkflow import Block
from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, XSD


class SentencingMethod(Block):
    def __init__(self, id):
        # TODO: use given ID to look up SM URI
        sm_uri = "http://fake-sm-uri.com"
        sm_label = "SM x"
        super().__init__(uri=sm_uri, label=sm_label)

    def prov_to_graph(self, g=None):
        g = super().prov_to_graph(g)

        # add in type
        g.add((URIRef(self.uri), RDF.type, self.PROVWF.SentencingMethod))

        return g
