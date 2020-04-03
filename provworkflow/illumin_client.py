from provworkflow import ProvWorkflowException
from provworkflow import Block
from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, XSD


class IlluminClient(Block):
    def __init__(self):
        super().__init__()

        self.query_result = None
        self.illumin_error = None

    def prov_to_graph(self, g=None):
        g = super().prov_to_graph(g)

        # add in type
        g.add((URIRef(self.uri), RDF.type, self.PROVWF.IlluminClient))

        return g

    def send_query(self, query):
        # validate query is GraphQL
        # send to Illumin (SOP)
        # store result somehow
            # for now, store returned JSON? in an instance var
            # store any error messages too
            # e = IlluminException("This is a custom message")
        pass


class IlluminException(Exception):
    pass
