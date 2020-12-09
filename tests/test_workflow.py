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

    print(g.serialize(format="turtle").decode())
    assert count == 2, "This Workflow must contain 2 Blocks"


def test_persist_to_graphdb():
    """
    Test persisting to graphdb
    """

    w = Workflow(named_graph_uri='http://example.com/test')
    b1 = Block()
    w.blocks.append(b1)
    w.persist('GraphDB')


def test_persist_to_SOP():
    """
    Test persisting to SOP
    """

    w = Workflow(named_graph_uri='urn:x-evn-master:test_datagraph')
    b1 = Block()
    w.blocks.append(b1)
    w.persist('SOP')


if __name__ == "__main__":
    test_Workflow_prov_to_graph()
    test_persist_to_graphdb()
    test_persist_to_SOP()
