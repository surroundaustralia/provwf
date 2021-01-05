from provworkflow import Block, PROVWF
from rdflib import Literal
from rdflib.namespace import OWL, RDF, PROV, XSD


def test_prov_to_graph():
    """A basic Block should prov_to_graph an Activity which is specialised as provwf:Block

    :return: None
    """

    b = Block()
    g = b.prov_to_graph()

    # check both generic and specific typing
    assert (b.uri, RDF.type, PROV.Activity) in g, "g must contain a prov:Activity"
    assert (b.uri, RDF.type, PROVWF.Block) in g, "g must contain a provwf:Block"

    assert (
        b.uri,
        OWL.versionIRI,
        Literal(b.version_uri, datatype=XSD.anyURI),
    ) in g, "g must contain an owl:versionIRI property for a provwf:Block instance"


if __name__ == "__main__":
    test_prov_to_graph()
