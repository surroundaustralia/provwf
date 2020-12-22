from provworkflow import Workflow, Block
from rdflib import Namespace

def test_Workflow_prov_to_allegro():
    """Testing that a workflow can write to allegro
    1 Block within it

    :return: None
    """

    w = Workflow()
    b1 = Block()
    w.blocks.append(b1)
    w._persist_to_allegro()

if __name__ == "__main__":
    test_Workflow_prov_to_allegro()