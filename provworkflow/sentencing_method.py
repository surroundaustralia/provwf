from provworkflow import Block
from rdflib import URIRef
from rdflib.namespace import RDF


class SentencingMethod(Block):
    def __init__(self, id, label=None):
        # TODO: use given ID to look up SM URI form a controlled list
        sm_uri = "http://fake-sm-uri.com"
        if label is not None:
            sm_label = "SM x"
        else:
            sm_label = "Sentencing Method {}".format(id)
        super().__init__(uri_str=sm_uri, label=sm_label)

    def prov_to_graph(self, g=None):
        g = super().prov_to_graph(g)

        # add in type
        g.add((URIRef(self.uri), RDF.type, self.PROVWF.SentencingMethod))

        return g
