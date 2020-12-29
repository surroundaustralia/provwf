from provworkflow import Block, PROVWF
from rdflib.namespace import RDF, PROV


def test_prov_to_graph():
    """A basic Block should prov_to_graph an Activity which is specialised as provwf:Block

    :return: None
    """

    b = Block()
    g = b.prov_to_graph()

    # check both generic and specific typing
    assert (None, RDF.type, PROV.Activity) in g, "g must contain a prov:Activity"
    assert (None, RDF.type, PROVWF.Block) in g, "g must contain a provwf:Block"


if __name__ == "__main__":
    test_prov_to_graph()
