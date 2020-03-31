from provworkflow import Workflow, Block
from rdflib import Namespace
from rdflib.namespace import RDF


def test_Workflow_prov_to_graph():
    """A basic Workflow should prov_to_graph an Activity which is specialised as provwf:Workflow and has at least
    1 Block within it

    :return: None
    """

    PROV = Namespace("http://www.w3.org/ns/prov#")
    PROVWF = Namespace("https://data.surroundaustralia.com/def/profworkflow#")

    w = Workflow()
    b1 = Block()
    b2 = Block()
    w.blocks.append(b1)
    w.blocks.append(b2)
    g = w.prov_to_graph()

    # check both generic and specific typing
    assert (None, RDF.type, PROV.Activity) in g, "g must contain a prov:Activity"
    assert (None, RDF.type, PROVWF.Workflow) in g, "g must contain a provwf:Workflow"

    # check it contains 2 Blocks
    count = 0
    for o in g.subject_objects(PROVWF.hadBlock):
        count += 1

    assert count == 2, "This Workflow must contain 2 Blocks"


if __name__ == "__main__":
    test_Workflow_prov_to_graph()
